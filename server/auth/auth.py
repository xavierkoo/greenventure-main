from flask import Flask, Response, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
import facebook

app = Flask(__name__)
CORS(app)

# Setting up the database connection.
# TODO - (COMMENT OUT IF RUNNING LOCALLY)
app.secret_key = os.environ.get("APP_SECRET")
client_id = os.environ.get("FACEBOOK_OAUTH_ID")
client_secret = os.environ.get("FACEBOOK_OAUTH_SECRET")

# Setting up the database connection.
# # TODO - (COMMENT OUT IF RUNNING DOCKER)
# app.secret_key = "W10_ESD_Breakdowns"
# client_id = "207392055310912"
# client_secret = "85f92b197a5c9b7cad6cdeb19809e86a"

# App Routes


@app.route("/login", methods=["GET"])
def login():
    """
    > The function redirects the user to a Facebook URL where they can login and grant the app access to
    their email and public profile
    :return: A redirect to the Facebook login page.
    """

    print("----------- [1] START RETRIEVING FACEBOOK AUTH CODE ------------")
    app_id = client_id
    redirect_uri = "http://localhost:5207/get_access_token"
    scope = "email,public_profile"

    return redirect(
        f"https://www.facebook.com/v11.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope={scope}"
    )


@app.route("/get_access_token", methods=["GET"])
def get_access_token():
    """
    The function gets the auth code from the URL, exchanges it for an access token, then uses the access
    token to get the user's info
    :return: The user info is being returned.
    """

    print("----------- [2] SUCCESS - RETRIEVED FACEBOOK AUTH CODE ------------")
    app_id = client_id
    app_secret = client_secret
    code = request.args.get("code")
    redirect_uri = f"http://localhost:5207/get_access_token"

    print("----------- [3] START EXCHANGING AUTH CODE FOR ACCESS TOKEN------------")
    graph = facebook.GraphAPI()
    access_token = graph.get_access_token_from_code(
        code, redirect_uri, app_id, app_secret
    )
    token = access_token["access_token"]

    print("----------- [4] SUCCESS - EXCHANGED FOR ACCESS TOKEN------------")

    print("----------- [5] EXCHANGING USER INFO USING ACCESS TOKEN------------")
    userInfo = get_info(token)
    aId = userInfo["aId"]
    email = userInfo["email"]
    name = userInfo["name"]
    print(
        "----------- [6] SUCCESS - SUCCESSFUL EXCHANGE USER INFO USING ACCESS TOKEN----------"
    )
    return redirect(
        f"http://localhost:5173/login_post?aId={aId}&email={email}&name={name}"
    )


@app.route("/get_info/<string:token>", methods=["GET"])
def get_info(token):
    """
    It takes in a token, and returns a dictionary containing the user's id, email, and name.

    :param token: the access token that we got from the previous step
    :return: A dictionary with the user's id, email, and name.
    """

    print("----------- [5-1] START RETRIEVING USER INFORMATION ------------")

    graph = facebook.GraphAPI(access_token=token)
    me = graph.get_object("me", fields="id, email, name")
    aId = me["id"]
    email = me["email"]
    name = me["name"]

    print("----------- [5-2] PACKAGING USER INFORMATION ------------")
    return {"aId": aId, "email": email, "name": name}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5207, debug=True)
