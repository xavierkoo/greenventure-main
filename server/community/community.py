from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
# Setting up the database connection.
# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "mysql+mysqlconnector://root:root@localhost:3306/communityDB"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("dbURL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)


class Userpost(db.Model):
    __tablename__ = "USERPOST"
    postID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    post_datetime = db.Column(db.DateTime, nullable=False)
    post = db.Column(db.String(255), nullable=False)

    def __init__(self, userID, username, post_datetime, post):
        self.userID = userID
        self.username = username
        self.post_datetime = post_datetime
        self.post = post

    def json(self):
        return {
            "userID": self.userID,
            "username": self.username,
            "postID": self.postID,
            "post_datetime": self.post_datetime,
            "post": self.post,
        }


class Postactivity(db.Model):
    __tablename__ = "POSTACTIVITY"
    postID = db.Column(db.Integer, primary_key=True)
    activity_datetime = db.Column(db.DateTime, primary_key=True)
    action_user = db.Column(db.String(50), primary_key=True)
    action_username = db.Column(db.String(50), nullable=True)
    activity = db.Column(db.String(20), nullable=True)
    comment = db.Column(db.String(50), nullable=True)

    def __init__(
        self, postID, activity_datetime, action_user, action_username, activity, comment
    ):
        self.postID = postID
        self.activity_datetime = activity_datetime
        self.action_user = action_user
        self.action_username = action_username
        self.activity = activity
        self.comment = comment

    def json(self):
        return {
            "postID": self.postID,
            "activity_datetime": self.activity_datetime,
            "action_user": self.action_user,
            "action_username": self.action_username,
            "activity": self.activity,
            "comment": self.comment,
        }


@app.route("/all", methods=["GET"])
def getAllPost():

    """
    It returns a jsonified response of all the posts in the database
    :return: A list of all the posts in the database
    """

    allPost = db.session.query(Userpost).all()
    if len(allPost):
        return (
            jsonify(
                {"code": 200, "data": {"posts": [post.json() for post in allPost]}}
            ),
            200,
        )
    else:
        return (
            jsonify({"code": 404, "message": "There is no post currently available"}),
            404,
        )


@app.route("/<userID>", methods=["GET"])
def getAllPostByUser(userID):

    """
    It returns all the posts of a user

    :param userID: The userID of the user whose posts you want to retrieve
    :return: a json object with the code 200 and the data of all the posts of the user.
    """

    allPostOfUser = db.session.query(Userpost).filter_by(userID=userID).all()
    if len(allPostOfUser):
        return (
            jsonify(
                {
                    "code": 200,
                    "data": {"posts": [post.json() for post in allPostOfUser]},
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"code": 404, "message": "There is no post currently available"}),
            404,
        )


@app.route("/user/<postID>", methods=["GET"])
def getUserEmailByPostId(postID):
    """
    It takes a postID as an argument and returns the userID of the user who posted it

    :param postID: The ID of the post you want to get the user's email for
    :return: The userID of the user who posted the postID
    """

    post = db.session.query(Userpost).filter_by(postID=postID).first()
    post = post.json()

    if post is not None:
        return (
            jsonify(
                {
                    "code": 200,
                    "data": {"posterID": post["userID"]},
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"code": 404, "message": "There is no post currently available"}),
            404,
        )


@app.route("/<userID>", methods=["POST"])
def addNewPost(userID):
    """
    It takes a userID as an argument, gets the post from the request body, formats the current date and
    time, creates a new Userpost object, and then adds it to the database

    :param userID: The userID of the user who is posting the post
    :return: a jsonified object with a code and data.
    """

    aRequest = request.get_json()
    post = str(aRequest["post"])
    username = str(aRequest["name"])
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    newPost = Userpost(
        userID=userID, username=username, post_datetime=formatted_date, post=post
    )
    try:
        db.session.add(newPost)
        db.session.commit()
    except Exception as e:
        return (
            jsonify(
                {
                    "code": 400,
                    "message": "An error occurred while creating the Post record. "
                    + str(e),
                }
            ),
            400,
        )
    return jsonify({"code": 201, "data": newPost.json()}), 201


@app.route("/<postID>", methods=["DELETE"])
def deleteAPost(postID):
    """
    It deletes a post from the database

    :param postID: The ID of the post to be deleted
    :return: a json object with the code and message.
    """
    record_to_delete = Userpost.query.filter_by(postID=postID).first()

    if record_to_delete is not None:
        try:
            db.session.delete(record_to_delete)
            db.session.commit()
        except Exception as e:
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": "An error occurred while creating the Post record. "
                        + str(e),
                    }
                ),
                400,
            )
        return (
            jsonify({"code": 201, "message": "The post has been deleted successfully"}),
            201,
        )
    else:
        return (
            jsonify(
                {
                    "code": 404,
                    "message": "There is no post detail by the id found!",
                }
            ),
            404,
        )


@app.route("/post/<postID>", methods=["GET"])
def getPostDetail(postID):
    """
    It returns a jsonified response of all the post details for a given postID

    :param postID: The ID of the post you want to get the details for
    :return: A list of all the post details for a given postID
    """
    allPostDetail = db.session.query(Postactivity).filter_by(postID=postID).all()
    if len(allPostDetail):
        return (
            jsonify(
                {
                    "code": 200,
                    "data": {
                        "postDetails": [
                            postDetail.json() for postDetail in allPostDetail
                        ]
                    },
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"code": 404, "message": "There is no post details for this post"}),
            404,
        )


@app.route("/post/<postID>", methods=["POST"])
def addPostDetail(postID):
    """
    It takes a postID, and then creates a new Postactivity record in the database

    :param postID: The ID of the post that the activity is being added to
    :return: a jsonified object with a code and data.
    """
    aRequest = request.get_json()
    action_user = str(aRequest["action_user"])
    action_username = str(aRequest["name"])
    activity = str(aRequest["activity"])
    comment = str(aRequest["comment"])
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    newPostDetail = Postactivity(
        postID=postID,
        action_user=action_user,
        action_username=action_username,
        activity=activity,
        comment=comment,
        activity_datetime=formatted_date,
    )
    try:
        db.session.add(newPostDetail)
        db.session.commit()
    except Exception as e:
        return (
            jsonify(
                {
                    "code": 400,
                    "message": "An error occurred while creating the Post Detail record. "
                    + str(e),
                }
            ),
            400,
        )
    return jsonify({"code": 201, "data": newPostDetail.json()}), 201


@app.route("/post/<postID>", methods=["DELETE"])
def deletePostDetail(postID):
    """
    Delete a post detail record from the database

    :param postID: The ID of the post
    :return: The post detail has been deleted successfully
    """
    aRequest = request.get_json()
    activity_datetime = str(aRequest["activity_datetime"])
    action_user = aRequest["action_user"]
    record_to_delete = Postactivity.query.filter_by(
        postID=postID, activity_datetime=activity_datetime, action_user=action_user
    ).first()
    if record_to_delete is not None:
        try:
            db.session.delete(record_to_delete)
            db.session.commit()
        except Exception as e:
            return (
                jsonify(
                    {
                        "code": 400,
                        "message": "An error occurred while creating the PostDetail record. "
                        + str(e),
                    }
                ),
                400,
            )

        return (
            jsonify(
                {
                    "code": 201,
                    "message": "The post detail has been deleted successfully",
                }
            ),
            201,
        )
    else:
        return (
            jsonify(
                {
                    "code": 404,
                    "message": "There is no post detail by the id found!",
                }
            ),
            404,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5104, debug=True)
