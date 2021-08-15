from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests


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
        resp = requests.post("http://localhost:5001/signup", json=args)
        return Response(resp.content, resp.status_code)  # todo header needed?


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
        resp = requests.post("http://localhost:5001/login", json=args)
        return Response(resp.content, resp.status_code)


class ShowProf(Resource):
    def get(self):
        resp = requests.get("http://localhost:5002/showprof", headers={'token': request.headers.get('token')})
        return Response(resp.content, resp.status_code)


app = Flask(__name__)
api = Api(app)
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(ShowProf, '/showprof')

if __name__ == '__main__':
    app.run(port=5000, debug=True)