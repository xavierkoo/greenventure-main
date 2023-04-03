from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import string
from datetime import datetime, timedelta

from os import environ


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL")
    or "mysql+mysqlconnector://root:root@localhost:3306/recyclingbinDB"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)


class MissionCode(db.Model):
    __tablename__ = "MISSIONCODE"

    mission_category = db.Column(db.String(20), primary_key=True)
    verification_code = db.Column(db.String(6), primary_key=True)
    datetime_expire = db.Column(db.DateTime)
    redeemed = db.Column(db.Boolean)

    def __init__(self, mission_category, verification_code, datetime_expire, redeemed):
        self.mission_category = mission_category
        self.verification_code = verification_code
        self.datetime_expire = datetime_expire
        self.redeemed = redeemed

    def json(self):
        return {
            "mission_category": self.mission_category,
            "verification_code": self.verification_code,
            "datetime_expire": self.datetime_expire,
            "redeemed": self.redeemed,
        }


@app.route("/verificationcode/<string:verification_code>")
def get_verification_code(verification_code):
    """This function checks if verification code exists"""

    verification = (
        db.session.query(MissionCode)
        .filter(MissionCode.verification_code == verification_code)
        .first()
    )

    if verification:
        return jsonify({"code": 200, "data": verification.json()})
    return jsonify({"code": 404, "message": "Verification code not found."}), 404


@app.route("/generate_code", methods=["POST"])
def generate_code():
    """This function generate code based on category"""

    # json to request for missioncategory

    # create MissionCode record based on missioncategory

    data = request.get_json()

    query_mission_category = data["mission_category"]
    characters = string.digits
    length = 6

    # Generate a random string of the given length using the possible characters
    random_string = "".join(random.choice(characters) for _ in range(length))

    new_verification_code = MissionCode(
        mission_category=query_mission_category,
        verification_code=random_string,
        datetime_expire=datetime.now() + timedelta(minutes=15),
        redeemed=0,
    )

    try:
        db.session.add(new_verification_code)
        db.session.commit()

    # failure case
    except Exception as e:
        return (
            jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while inserting verification code."
                    + str(e),
                }
            ),
            500,
        )

    # success case
    return jsonify({"code": 201, "data": new_verification_code.json()}), 201


@app.route("/redeem_code", methods=["POST"])
def redeem_code():
    """This function generate code based on category"""

    # json to request for missioncategory

    # create MissionCode record based on missioncategory

    data = request.get_json()

    query_verification_code = data["verification_code"]

    verification_code = (
        db.session.query(MissionCode)
        .filter(MissionCode.verification_code == query_verification_code)
        .first()
    )

    verification_code.redeemed = 1

    try:
        db.session.commit()

    # failure case
    except Exception as e:
        return (
            jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while updating verification code redemption status."
                    + str(e),
                }
            ),
            500,
        )

    # success case
    return jsonify({"code": 201, "data": verification_code.json()}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5105, debug=True)

# docker build -f recyclingbin.Dockerfile -t limrenkee/recyclingbin:1.0 ./
# docker run -p 5105:5105 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/recyclingbinDB limrenkee/recyclingbin:1.0
