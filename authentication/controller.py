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
        if json.loads(prof)["password"] != args["password"]:
            return Response('{"error": "incorrect username or password"}', 400)
        token = self.auth.create_token(args["username"])
        return Response(json.dumps({"token": token}), 200)


api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5001, debug=True)