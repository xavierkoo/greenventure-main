from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)


voucher_URL = environ.get('voucher_URL') or "http://localhost:5101/voucher" 
wallet_URL = environ.get('wallet_URL') or "http://localhost:5102/wallet" 
walletVoucher_URL = environ.get('walletVoucher_URL') or "http://localhost:5102/walletVoucher" 

# docker build -t mauriceho/displaypointsvouchers:1.0 ./
# docker run -p 5107:5107 mauriceho/displaypointsvouchers:1.0


@app.route("/get_wallet_details", methods=['POST'])
def get__wallet_details():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            person = request.get_json()
            print("\nReceived an person in JSON:", person)
            # do the actual work
            # 1. Send order info {cart items}
            voucher_result = user_get_vouchers(person['id']) # have to replace
            print('\n------------------------')
            print('\nresult: ', voucher_result)
            return jsonify(voucher_result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "displayPointsVoucher.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def user_get_vouchers(userId):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    to_return = {}
    print('\n-----Invoking order walletmicroservice-----')
    userwallet_result = invoke_http(wallet_URL+"/"+userId, method='GET')
    print('order_result:', userwallet_result)
  
    # Check the order result; if a failure, send it to the error microservice.
    # code = userwallet_result["code"]
    # message = json.dumps(userwallet_result)

    to_return['points'] = userwallet_result['points_remaining'] # adding points to the object


    uservoucher_result = invoke_http(walletVoucher_URL+"/"+str(userwallet_result['walletID']), method='GET')

    notused = []

    for voucher in uservoucher_result['voucher']:
        if (voucher['used'] == False):
            notused.append(voucher)


    to_return['user_vouchers'] = notused# adding uservouchers


    print('\n-----Invoking order vouchermicroservice-----')
    available_vouchers = invoke_http(voucher_URL, method='GET')
    to_show_vouchers = [] 

    userowned = [] 
    for voucher in uservoucher_result['voucher']:
        userowned.append(int(voucher['voucherID']))

    print("userowen",userowned)

    for availvoucher in available_vouchers['data']['vouchers']:
        availvoucherID = availvoucher['voucherID']
        print(availvoucherID)
        if (availvoucherID not in userowned):
            print(availvoucherID,userowned)
            to_show_vouchers.append(availvoucher)

    to_return['available_vouchers'] = to_show_vouchers

    return to_return


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5203, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
