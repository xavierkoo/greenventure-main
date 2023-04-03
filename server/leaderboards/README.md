# greenventure-leaderboards

### Add `.env` file and configure database connection
```
MONGODB_URI=mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
PORT=5103
```
### Docker Command
```
docker-compose up --build
```
Client - PORT:3000 <br>
Server - PORT:5103

# API Documentation

## Base API URL
http://localhost:5103/api/leaderboards

## User Related APIs

#### Get all users
**GET:** /<br>
**Send:** NIL <br>
**Receive:** All Users, Response Code - 200 OK || Response Code - 404 || Response Code - 404, unknown endpoint

#### Get specific user
**GET:** /:userId <br>
**Send:** NIL <br>
**Receive:** Specific User, Response Code - 200 OK || Response Code - 404 || Response Code - 404, unknown endpoint

#### Add a user
**POST:** / <br>
**Send:** userId (String), name (String), points (Number)<br>
**Receive:**  User Object, Response Code - 201 || Exception || Response Code - 404, unknown endpoint

#### Update a user's points
**PATCH:** /:userId <br>
**Send:** points (Number) <br>
**Receive:** Response Code - 204, No Content || Respose Code - 404 ||Respose Code - 404, unknown endpoint
