from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
import pika

from invokes import invoke_http

from os import environ


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    environ.get("dbURL") or "mysql+mysqlconnector://root:root@localhost:3306/missionDB"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

recyclingbin_URL = environ.get("recyclingbinURL") or "http://localhost:5105/"

wallet_URL = environ.get("walletURL") or "http://localhost:5102/"
addpoints_URL = wallet_URL + "wallet/addpoints"

leaderboard_URL = (
    environ.get("leaderboardURL") or "http://localhost:5103/api/leaderboards/"
)


class Mission(db.Model):
    __tablename__ = "MISSION"

    missionID = db.Column(db.Integer, primary_key=True)
    reward = db.Column(db.Integer, nullable=False)
    mission_category = db.Column(db.String(20), nullable=False)
    required_count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100))

    usermissions = db.relationship("UserMission", backref="Mission", lazy=True)

    def __init__(
        self, missionID, reward, required_count, mission_category, description
    ):
        self.missionID = missionID
        self.mission_category = mission_category
        self.reward = reward
        self.required_count = required_count
        self.description = description

    def json(self):
        return {
            "missionID": self.missionID,
            "reward": self.reward,
            "required_count": self.required_count,
            "mission_category": self.mission_category,
            "description": self.description,
        }


class UserMission(db.Model):
    __tablename__ = "USERMISSION"

    missionID = db.Column(
        db.Integer, db.ForeignKey("MISSION.missionID"), primary_key=True
    )
    userID = db.Column(db.Integer, primary_key=True)
    completed_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20))

    def __init__(self, missionID, userID, completed_count, status):
        self.missionID = missionID
        self.completed_count = completed_count
        self.userID = userID
        self.status = status

    def json(self):
        return {
            "missionID": self.missionID,
            "userID": self.userID,
            "completed_count": self.completed_count,
            "status": self.status,
        }


@app.route("/mission/<string:userid>")
def get_all_available_mission(userid):
    """This function gets all missions that has yet to be taken up by user"""

    # get all mission that has yet to be taken up by user

    usermissionlist = (
        db.session.query(UserMission.missionID)
        .filter(UserMission.userID == userid)
        .subquery()
    )
    missionlist = (
        db.session.query(Mission).filter(~Mission.missionID.in_(usermissionlist)).all()
    )

    if len(missionlist):
        return jsonify(
            {
                "code": 200,
                "data": {"missions": [mission.json() for mission in missionlist]},
                "message": "Successfully obtained all available mission(s)",
            }
        )
    return (
        jsonify(
            {
                "query_userid": userid,
                "code": 404,
                "message": "There are no available missions.",
            }
        ),
        404,
    )


@app.route("/in_progress_mission/<string:userid>")
def get_all_in_progress_mission(userid):
    """This function gets all missions that has been taken up by user"""

    # get all mission that has yet to be taken up by user

    results = (
        db.session.query(
            Mission.missionID,
            Mission.reward,
            Mission.required_count,
            Mission.mission_category,
            Mission.description,
            UserMission.completed_count,
        )
        .join(UserMission)
        .filter(Mission.missionID == UserMission.missionID)
        .filter(UserMission.userID == userid)
        .filter(UserMission.status != "completed")
        .all()
    )

    if len(results) >= 0:

        missionlist = []

        for mission in results:
            mission_dict = {
                "missionID": mission[0],
                "reward": mission[1],
                "required_count": mission[2],
                "mission_category": mission[3],
                "description": mission[4],
                "completed_count": mission[5],
            }
            missionlist.append(mission_dict)

        return jsonify({"code": 200, "data": {"missions": missionlist}, "message": "Successfully obtained all in-progress mission(s)."})
    return jsonify({"code": 404, "message": "There are no in-progress missions."}), 404


@app.route("/accept_mission", methods=["POST"])
def accept_mission():
    """This function gets creates the usermission record when user clicks accept mission"""

    data = request.get_json()

    query_userid = data["userid"]
    query_missionid = data["missionid"]

    new_usermission = UserMission(
        missionID=query_missionid,
        userID=query_userid,
        completed_count=0,
        status="in_progress",
    )

    try:
        db.session.add(new_usermission)
        db.session.commit()

    # failure case
    except Exception as e:
        return (
            jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while creating the user mission record. "
                    + str(e),
                }
            ),
            500,
        )

    # success case
    return jsonify({"code": 201, "data": new_usermission.json(), "message": "Successfully accepted mission"}), 201


@app.route("/complete_mission", methods=["POST"])
def complete_mission():
    """This function verifies the 6-digit code,
    If verified, proceed with processing
    Else, return failure"""

    data = request.get_json()

    query_userid = data["userid"]
    query_missionid = data["missionid"]
    query_verification_code = data["verification_code"]

    # expected mission category based on mission id that came in
    veri_mission_cat = (
        db.session.query(Mission.mission_category)
        .filter(Mission.missionID == query_missionid)
        .scalar()
    )

    # verify if the verification code exists
    verification_details = check_verification_exist(query_verification_code)
    code = verification_details["code"]

    if code not in range(200, 300):
        # verification code does not exist

        return {
            "code": 400,
            "message": verification_details["message"],
        }

    # code exists, check if code is valid category

    category = verification_details["data"]["mission_category"]
    is_redeemed = verification_details["data"]["redeemed"]
    datetime_expiry = verification_details["data"]["datetime_expire"]

    datetime_expiry = datetime.strptime(datetime_expiry, "%a, %d %b %Y %H:%M:%S %Z")

    if category == veri_mission_cat and not is_redeemed:
        # valid verification code, proceed with updating

        missionrequired = (
            db.session.query(Mission.required_count)
            .filter(Mission.missionID == query_missionid)
            .scalar()
        )
        completedcount = (
            db.session.query(UserMission.completed_count)
            .filter(UserMission.userID == query_userid)
            .filter(UserMission.missionID == query_missionid)
            .scalar()
        )
        usermission = (
            db.session.query(UserMission)
            .filter(UserMission.userID == query_userid)
            .filter(UserMission.missionID == query_missionid)
            .first()
        )
        points_earnt = (
            db.session.query(Mission.reward)
            .filter(Mission.missionID == query_missionid)
            .scalar()
        )

        # update verification code at rubbish bin to redeemed
        redemption_status = redeem_code(query_verification_code)
        code = redemption_status["code"]
        if code not in range(200, 300):
            # verification code is not redeemed properly

            return {"code": code, "message": redemption_status["message"]}

        # verification code redeem, proceed with updating

        # update fields
        usermission.completed_count = completedcount + 1

        if completedcount + 1 >= missionrequired:

            usermission.status = "completed"

        try:
            db.session.commit()

            if usermission.status == "completed":

                # trigger all completed mission procedure, includes adding points to wallet,
                # updating leaderboard, as well as sending email to user

                data["points"] = points_earnt

                update_wallet_status = update_wallet(data)

                code = update_wallet_status["code"]

                if code not in range(200, 300):

                    return {
                        "code": code,
                        # assuming the update wallet function returns error in message key
                        "message": update_wallet_status["message"],
                    }

                update_leaderboard(data)

                def send_to_lavinmq(message):

                    channel.basic_publish(
                        exchange="", routing_key=queue_name, body=message
                    )

                url = "amqps://pjfowojn:hi7ZiPRdS6bEQDHZo-_CKeLH7vbINRCn@possum.lmq.cloudamqp.com/pjfowojn"
                params = pika.URLParameters(url)
                connection = pika.BlockingConnection(params)
                channel = connection.channel()
                queue_name = "notifications"
                my_object = {
                    "email": "limrenkee123@gmail.com",
                    "message": "You have earnt {} from the mission!".format(
                        points_earnt
                    ),
                    "subject": "Mission Completed!",
                }
                message = json.dumps(my_object)
                send_to_lavinmq(message)
                # Close the connection
                connection.close()

                return {"code": 200, "message": "Task executed successfully"}

            return jsonify({"code": 200, "data": usermission.json(),"message": "Successfully completed an additional task."}), 200

        except Exception as e:

            return (
                jsonify(
                    {
                        "code": 500,
                        "data": {
                            "userid": query_userid,
                            "missionid": query_missionid,
                        },
                        "message": "An error occurred while updating the user mission. "
                        + str(e),
                    }
                ),
                500,
            )

    return {"code": 400, "message": "Verification Code is invalid"}


def check_verification_exist(verification_code):

    # check if verifcation code exists in the recycling bin microservice
    verification_details = invoke_http(
        recyclingbin_URL + "verificationcode/" + str(verification_code), method="GET"
    )

    return verification_details


# def process_completion(data):

#     completion_process_details = invoke_http(process_completion_URL, json=data, method="POST")

#     return completion_process_details


def redeem_code(verification_code):

    passed_json = {"verification_code": verification_code}
    redemption_details = invoke_http(
        recyclingbin_URL + "redeem_code", json=passed_json, method="POST"
    )

    return redemption_details


def update_wallet(data):

    # check if verifcation code exists in the recycling bin microservice
    wallet_info = invoke_http(addpoints_URL, json=data, method="PATCH")

    return wallet_info


def update_leaderboard(data):
    # check if verifcation code exists in the recycling bin microservice
    leaderboard_info = invoke_http(
        leaderboard_URL + data["userid"], json=data, method="PATCH"
    )

    return leaderboard_info


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5201, debug=True)


# docker build -f mission.Dockerfile -t limrenkee/mission:1.0 ./
# docker run -p 5201:5201 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/missionDB limrenkee/mission:1.0
