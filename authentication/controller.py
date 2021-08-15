from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
import json
from auth_logic import AuthLogic

app = Flask(__name__)
api = Api(app)


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
        resp = requests.post("http://127.0.0.1:5003/signup", json=args)
        if resp.status_code >= 400:
            return Response(resp.content, resp.status_code)
        token = self.auth.create_token(args["username"])
        return Response(json.dumps({"token": token}), resp.status_code)


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
        user_resp = requests.get("http://127.0.0.1:5003/getuser/" + args["username"])
        if user_resp.status_code >= 500:
            return Response('{"error": "server unavailable"}', user_resp.status_code)
        if user_resp.status_code >= 400:
            return Response('{"error": "user does not exist"}', 400)
        if json.loads(user_resp.content)["password"] != args["password"]:
            return Response('{"error": "incorrect username or password"}', 400)
        token = self.auth.create_token(args["username"])
        return Response(json.dumps({"token": token}), 200)


api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5001, debug=True)