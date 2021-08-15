from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
from requests.exceptions import Timeout
from api_gateway_logic import APILogic

apiLogic = APILogic()


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
        self.fail_count = 0

    def post(self):
        args = self.reqparse.parse_args()
        try:
            resp = requests.post("http://localhost:5001/signup", json=args, timeout=0.5)
        except Timeout:
            self.fail_count += 1
            #todo disable if needed
            return Response(json.dumps({"error": "Connection Timed Out"}), 408)
        if resp.content >= 500:
            self.fail_count += 1
            #todo disable if needed
        return Response(resp.content, resp.status_code)


class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username", type=str, required=True, help="The username must be provided", location="json"
        )
        self.reqparse.add_argument(
            "password", type=str, required=True, help="The password must be provided", location="json"
        )
        self.fail_count = 0

    def post(self):
        args = self.reqparse.parse_args()
        try:
            resp = requests.post("http://localhost:5001/login", json=args, timeout=0.5)
        except Timeout:
            self.fail_count += 1
            #todo disable if needed
            return Response(json.dumps({"error": "Connection Timed Out"}), 408)
        if resp.content >= 500:
            self.fail_count += 1
            #todo disable if needed
        return Response(resp.content, resp.status_code)


class ShowProf(Resource):
    def __init__(self):
        self.fail_count = 0

    def get(self):
        if apiLogic.is_valid(request.headers.get('token')):
            try:
                resp = requests.get("http://localhost:5002/showprof", headers={'token': request.headers.get('token')}, timeout=0.5)
            except Timeout:
                self.fail_count += 1
                # todo disable if needed
                return Response(json.dumps({"error": "Connection Timed Out"}), 408)
            if resp.content >= 500:
                self.fail_count += 1
                # todo disable if needed
            return Response(resp.content, resp.status_code)
        Response('{"error": "invalid token"}', 401)


class UpdateProf(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "password", type=str, required=True, help="The password must be provided", location="json"
        )
        self.reqparse.add_argument(
            "email", type=str, required=True, help="The email must be provided", location="json"
        )
        self.reqparse.add_argument(
            "mobile", type=str, required=True, help="The mobile number must be provided", location="json"
        )
        self.fail_count = 0

    def post(self):
        args = self.reqparse.parse_args()
        if apiLogic.is_valid(request.headers.get('token')):
            try:
                resp = requests.post("http://localhost:5002/updateprof", json=args,
                                     headers={'token': request.headers.get('token')}, timeout=0.5)
            except Timeout:
                self.fail_count += 1
                # todo disable if needed
                return Response(json.dumps({"error": "Connection Timed Out"}), 408)
            if resp.content >= 500:
                self.fail_count += 1
                # todo disable if needed
            return Response(resp.content, resp.status_code)
        Response('{"error": "invalid token"}', 401)


app = Flask(__name__)
api = Api(app)
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(ShowProf, '/showprof')
api.add_resource(UpdateProf, '/updateprof')

if __name__ == '__main__':
    app.run(port=5000, debug=True)