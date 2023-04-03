from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys
from os import environ

from invokes import invoke_http

import pika
import json


app = Flask(__name__)
CORS(app)


wallet_URL = environ.get("wallet_URL") or "http://localhost:5102/wallet"
walletVoucher_URL = (
    environ.get("walletVoucher") or "http://localhost:5102/walletVoucher"
)


@app.route("/useVoucher", methods=["POST"])
def use_voucher():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            use = request.get_json()

            # do the actual work
            result = processUseVoucher(use)
            print("\n------------------------")

            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = (
                str(e)
                + " at "
                + str(exc_type)
                + ": "
                + fname
                + ": line "
                + str(exc_tb.tb_lineno)
            )
            print(ex_str)

            return (
                jsonify(
                    {
                        "code": 500,
                        "message": "useVoucher.py internal error: " + ex_str,
                    }
                ),
                500,
            )

    # if reached here, not a JSON request.
    return (
        jsonify(
            {"code": 400, "message": "Invalid JSON input: " +
                str(request.get_data())}
        ),
        400,
    )


def processUseVoucher(use):
    # Invoke the wallet microservice
    print("\n-----Invoking order microservice-----")
    useVoucher_result = invoke_http(
        wallet_URL + "/use/" +
        str(use["walletID"]) + "/" + use["voucher_code"],
        method="PATCH",
    )
    print("useVoucher_result:", useVoucher_result)

    code = useVoucher_result["code"]
    message = json.dumps(useVoucher_result["message"])

    # if an error occurs when consuming the voucher.
    if code not in range(200, 300):
        return {
            "code": 500,
            "data": {"usage_result": useVoucher_result},
            "message": "Voucher can't be use. Something went wrong",
        }

    else:
        # Craft message to send to AMQP
        returnMessage = (
            "Dear valued GreenVenture customer, \n\nWe are pleased to inform you that your voucher with the code '"
            + use["voucher_code"]
            + "' has been successfully redeemed. \n\nWe greatly appreciate your commitment to cycling and reducing your carbon footprint. Your effort is truly commendable and we encourage you to continue your sustainable practices."
        )
        # Craft message to return back to front end
        frontEndMessage = (
            "Voucher '" + use["voucher_code"] +
            "' has been successfully redeemed."
        )

        # Send a message to LavinMQ to notify user by email that voucher is consumed.
        def send_to_lavinmq(message):
            channel.basic_publish(
                exchange="", routing_key=queue_name, body=message)

        url = "amqps://pjfowojn:hi7ZiPRdS6bEQDHZo-_CKeLH7vbINRCn@possum.lmq.cloudamqp.com/pjfowojn"
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        queue_name = "notifications"
        my_object = {
            "email": use["email"],
            "message": returnMessage,
            "subject": "Voucher Usage",
        }
        message = json.dumps(my_object)
        send_to_lavinmq(message)
        # Close the connection
        connection.close()

    return {
        "code": 201,
        "data": {
            "useVoucher_result": useVoucher_result,
            "returnMessage": frontEndMessage,
        },
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5205, debug=True)
