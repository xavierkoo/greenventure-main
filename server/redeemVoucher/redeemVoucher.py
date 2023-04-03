from flask import Flask, request, jsonify
import pika
from flask_cors import CORS

import os
import sys
from os import environ

from invokes import invoke_http

import pika
import json


app = Flask(__name__)
CORS(app)


voucher_URL = environ.get('voucher_URL') or "http://localhost:5101/voucher"
wallet_URL = environ.get('wallet_URL') or "http://localhost:5102/wallet"
walletVoucher_URL = environ.get(
    'walletVoucher') or "http://localhost:5102/walletVoucher"


@app.route("/redeemVoucher", methods=['POST'])
def redeem_voucher():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            redemption = request.get_json()
            print("\nReceived an order in JSON:", redemption)

            # do the actual work
            result = processRedeemVoucher(redemption)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "redeemVoucher.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processRedeemVoucher(redemption):
    # Invoke the wallet microservice
    print('\n-----Invoking wallet microservice-----')
    redemption_result = invoke_http(wallet_URL, method='POST', json=redemption)
    print('voucherRedemption_result:', redemption_result)

    code = redemption_result["code"]
    message = json.dumps(redemption_result["message"])

    if code not in range(200, 300):
        # Return error
        return {
            "code": 500,
            "data": {"order_result": redemption_result},
            "message": "Voucher redemption failure"
        }

    else:

        # Invoke the voucher microservice
        print('\n-----Invoking order microservice-----')
        redemption_voucher_result = invoke_http(
            voucher_URL+"/"+redemption["voucher_code"], method='PATCH')
        print('voucherRedemption_result:', redemption_voucher_result)

        code = redemption_voucher_result["code"]
        message = json.dumps(redemption_voucher_result["message"])

        if code not in range(200, 300):
            # Return error
            return {
                "code": 500,
                "data": {"order_result": redemption_voucher_result},
                "message": "Voucher redemption failure."
            }

        returnMessage = "Dear valued GreenVenture customer,\n We would like to inform you that the voucher with the code \'" + \
            redemption["voucher_code"] + "\' has been added into the wallet.\n Please note that " + str(
                redemption["voucher_amount"]) + " points have been deducted from your wallet as part of the redemption process."
        frontEndMessage = "Voucher with the code \'" + redemption["voucher_code"] + "\' has been added into the wallet. " + str(
            redemption["voucher_amount"]) + " points have been deducted from your wallet as part of the redemption process."

        def send_to_lavinmq(message):
            channel.basic_publish(
                exchange="", routing_key=queue_name, body=message)

        # Send a message to LavinMQ
        url = "amqps://pjfowojn:hi7ZiPRdS6bEQDHZo-_CKeLH7vbINRCn@possum.lmq.cloudamqp.com/pjfowojn"
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        queue_name = "notifications"
        my_object = {"message": returnMessage,
                     "email": redemption["email"], "subject": "Voucher Redemption"}
        message = json.dumps(my_object)
        send_to_lavinmq(message)
        # Close the connection
        connection.close()

    return {
        "code": 201,
        "data": {
            "redemption_result": redemption_result,
            "redemption_voucher_result": redemption_voucher_result,
            "returnMessage": frontEndMessage
        }
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5204, debug=True)
