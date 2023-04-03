import json
from flask import Flask, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pika
from invokes import invoke_http
import os

app = Flask(__name__)
CORS(app)

CREATE_WALLET_URL = os.environ.get("CREATE_WALLET_URL")
ACCOUNT_URL = os.environ.get("ACCOUNT_URL")
AUTH_ACCOUNT_URL = os.environ.get("AUTH_ACCOUNT_URL")
LEADERBOARD_URL = os.environ.get("LEADERBOARD_URL")


# App Routes
@app.route("/", methods=["POST"])
def createAccount():

    print("----------- INVOKING OF CREATE_ACCOUNT (COMPLEX SERVICE) ------------")

    print("----------- [1] START RETRIEVING REQUEST BODY DATA ------------")
    data = request.get_json()
    aId = data["aId"]
    name = data["name"]
    email = data["email"]
    print(f"AID = {aId}")
    print("----------- [2] SUCCESS - RETRIEVED REQUEST BODY DATA ------------")

    print("----------- [3] CHECK IF ID IN SYSTEM ------------")
    try:
        response = invoke_http(ACCOUNT_URL + aId, method="GET")
        response[0]["code"]
    except:
        print(
            "An error has occur with the database again! Try to refresh and login again"
        )
        redirect("http://localhost:5173/login")

    response = invoke_http(ACCOUNT_URL + aId, method="GET")

    if response[0]["code"] == 404:
        print("----------- [4] ID NOT IN SYSTEM ------------")

        print(
            "----------- [5] POST REQUEST TO ACCOUNT (SIMPLE SERVICE) ------------")
        invoke_http(ACCOUNT_URL + aId, method="POST", json=data)

        print(
            "----------- [6] POST REQUEST TO WALLET (SIMPLE SERVICE) ------------")

        createWalletBody = {"userID": int(aId)}
        invoke_http(
            CREATE_WALLET_URL + "wallet/adduser", method="POST", json=createWalletBody
        )

        print(
            "----------- [7] POST REQUEST TO LEADERBOARD (SIMPLE SERVICE) ------------"
        )
        leaderboardBody = {"userId": aId, "name": name}
        invoke_http(LEADERBOARD_URL, method="POST", json=leaderboardBody)

        print(
            "----------- [8] POST REQUEST TO AMQP (SIMPLE SERVICE) ------------")

        def send_to_lavinmq(message):
            channel.basic_publish(
                exchange="", routing_key=queue_name, body=message)

        url = "amqps://pjfowojn:hi7ZiPRdS6bEQDHZo-_CKeLH7vbINRCn@possum.lmq.cloudamqp.com/pjfowojn"
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        queue_name = "notifications"

        my_object = {
            "email": email,
            "message": "You have successfully created an account with greenVenture!",
            "subject": "Account Registration!",
        }
        message = json.dumps(my_object)
        send_to_lavinmq(message)
        # Close the connection
        connection.close()

        print("----------- [9] SUCCESS - ALL SERVICES UPDATED ------------")

        return jsonify(
            {
                "code": 201,
                "message": "All Creation Done",
            },
            201,
        )
    else:
        return jsonify(
            {
                "code": 201,
                "message": "Account already in system",
            },
            201,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5208, debug=True)
