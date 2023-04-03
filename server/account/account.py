from flask import Flask, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Setting up the database connection.
# TODO - (COMMENT OUT IF RUNNING LOCALLY)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("dbURL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Setting up the database connection.
# # TODO - (COMMENT OUT IF RUNNING DOCKER)
# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "mysql+mysqlconnector://root:root@localhost:3306/accountDB"

db = SQLAlchemy(app)

# The Account class is a model that represents the ACCOUNT table in the database
class Account(db.Model):
    __tablename__ = "ACCOUNT"

    userID = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=True)

    def __init__(self, userID, name, email):
        self.userID = userID
        self.name = name
        self.email = email

    def json(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "email": self.email,
        }


# App Routes
@app.route("/<aId>", methods=["GET", "POST"])
def account(aId):

    print("----------- INVOKING OF ACCOUNT (SIMPLE SERVICE) ------------")

    print("----------- [4] START RETRIEVING USER BASED ON ID------------")
    record = Account.query.filter_by(userID=aId).first()

    if record is not None:
        print("----------- [5] RECORD IS PRESENT------------")
        if request.method == "GET":
            print("----------- [6] REPACKAGE RECORD------------")
            recordJson = record.json()
            return jsonify(
                {
                    "code": 201,
                    "data": recordJson,
                },
                201,
            )

    else:
        print("----------- [5] RECORD IS NOT FOUND------------")
        if request.method == "POST":
            print("----------- [6] SET NEW RECORD------------")
            newRecord = request.get_json()
            newAccountRecord = Account(
                userID=newRecord["aId"],
                email=newRecord["email"],
                name=newRecord["name"],
            )
            db.session.add(newAccountRecord)
            db.session.commit()
            print("----------- [7] SUCCESS - CREATION OF NEW RECORD------------")
            return jsonify(
                {
                    "code": 201,
                    "message": "The account has been created successfully",
                },
                201,
            )

        if request.method == "GET":
            print("----------- [6] THERE IS NO RECORD------------")
            return jsonify(
                {
                    "code": 404,
                    "data": None,
                },
                404,
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
