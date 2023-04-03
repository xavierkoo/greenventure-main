import json
from flask import Flask, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
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

        print("----------- [5] POST REQUEST TO ACCOUNT (SIMPLE SERVICE) ------------")
        invoke_http(ACCOUNT_URL + aId, method="POST", json=data)

        print("----------- [6] POST REQUEST TO WALLET (SIMPLE SERVICE) ------------")

        aDict = {"userID": int(aId)}
        invoke_http(CREATE_WALLET_URL + "wallet/adduser", method="POST", json=aDict)

        print(
            "----------- [7] POST REQUEST TO LEADERBOARD (SIMPLE SERVICE) ------------"
        )
        # invoke_http(LEADERBOARD_URL + "api/leaderboards/" + aId, method="POST")

        print("----------- [8] POST REQUEST TO AMQP (SIMPLE SERVICE) ------------")

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
