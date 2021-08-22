from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
import json
from auth_logic import AuthLogic

app = Flask(__name__)
api = Api(app)

from auth_logic import AuthLogic
auth_logic = AuthLogic()

class Signup(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username", type=str, required=True, help="The username must be provided", location="json"
        )
        self.reqparse.add_argument(
            "password", type=str, required=True, help="The password must be provided", location="json"
        )
        self.reqparse.add_argument(
            "email", type=str, required=True, help="The email must be provided", location="json"
        )
        self.reqparse.add_argument(
            "mobile", type=str, required=True, help="The mobile number must be provided", location="json"
        )
        self.auth = AuthLogic()

    def post(self):
        args = self.reqparse.parse_args()
        try:
            auth_logic.add_new_user(args["username"], args["password"])
        except:
            auth_logic.refresh()
            return Response(json.dumps({"error": "query failed"}), 400)
        token = self.auth.create_token(args["username"])
        # send event
        decode_token = auth_logic.get_token(token)
        requests.post("http://127.0.0.1:5006/submitevent",
                      json={"type": "signup", "data": json.dumps({"header": decode_token, "payload": args})})
        return Response(json.dumps({"token": token}), 200)


class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username", type=str, required=True, help="The username must be provided", location="json"
        )
        self.reqparse.add_argument(
            "password", type=str, required=True, help="The password must be provided", location="json"
        )
        self.auth = AuthLogic()

    def post(self):
        args = self.reqparse.parse_args()
        username = args["username"]
        try:
            prof = auth_logic.get_profile(username)
            prof = auth_logic.decode_prof(prof)
        except:
            return Response('{"error": "user does not exist"}', 400)
        if prof["password"] != args["password"]:
            return Response('{"error": "incorrect username or password"}', 400)
        token = self.auth.create_token(args["username"])
        return Response(json.dumps({"token": token}), 200)


class EventHandler(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "type", type=str, required=True, help="The type must be provided", location="json"
        )
        self.reqparse.add_argument(
            "data", type=str, required=True, help="The data must be provided", location="json"
        )

    def post(self):
        args = self.reqparse.parse_args()
        type = args["type"]
        if type != "updateprof":
            return
        data = json.loads(args["data"])
        payload = data["payload"]
        new_prof = auth_logic.update_profile(payload["username"], payload["password"])
        return Response(json.dumps(new_prof), 200)


api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(EventHandler, '/eventhandler')

if __name__ == '__main__':
    app.run(port=5001, debug=True)