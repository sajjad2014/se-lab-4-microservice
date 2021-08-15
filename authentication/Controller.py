from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests

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


    def post(self):
        args = self.reqparse.parse_args()
        resp = requests.post("http://localhost:5003/signup", json=args)
        if resp.status_code >= 400:
            return Response(resp.content, resp.status_code)
        # todo create jwt token in logic and set as header
        return Response(resp.content, resp.status_code) # todo header


class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username", type=str, required=True, help="The username must be provided", location="json"
        )
        self.reqparse.add_argument(
            "password", type=str, required=True, help="The password must be provided", location="json"
        )


    def post(self):
        args = self.reqparse.parse_args()
        user_resp = requests.get("http://localhost:5003/getuser/" + args["username"])
        if user_resp.status_code >= 400:
            return Response('{"error": "user does not exist"}', 400)
        if json.loads(user_resp.content)["password"] != args["password"]:
            return Response('{"error": "incorrect username or password"}', 400)
        # todo create jwt token
        return Response('{"token": }', 200)  #todo


api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5001, debug=True)