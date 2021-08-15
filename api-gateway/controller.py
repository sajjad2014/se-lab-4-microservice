from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
from requests.exceptions import Timeout
from api_gateway_logic import APILogic
import time

apiLogic = APILogic()


auth_fail_count = 0
prof_fail_count = 0

auth_available = True
prof_available = True

auth_start_fail = None
prof_start_fail = None

def current_seconds():
    return round(time.time())

def increase_auth_fail():
    global auth_fail_count, auth_available, auth_start_fail
    auth_fail_count += 1
    if auth_fail_count == 3:
        auth_available = False
        auth_fail_count = 0
        auth_start_fail = current_seconds()

def increase_prof_fail():
    global prof_fail_count, prof_available, prof_start_fail
    prof_fail_count += 1
    if prof_fail_count == 3:
        prof_available = False
        prof_fail_count = 0
        prof_start_fail = current_seconds()

def check_auth_valid():
    global auth_available, auth_fail_count
    if auth_start_fail is None or current_seconds() - auth_start_fail > 30:
        auth_available = True
        return True
    return False

def check_prof_valid():
    global prof_available, prof_fail_count
    if prof_start_fail is None or current_seconds() - prof_start_fail > 30:
        prof_available = True
        return True
    return False

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
        if not check_auth_valid():
            return Response('{"error": "Authentication service is down"}', 503)
        args = self.reqparse.parse_args()
        try:
            resp = requests.post("http://127.0.0.1:5001/signup", json=args, timeout=5)
        except Timeout:
            increase_auth_fail()
            return Response(json.dumps({"error": "Connection Timed Out"}), 408)
        if resp.status_code >= 500:
            increase_auth_fail()
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

    def post(self):
        if not check_auth_valid():
            return Response('{"error": "Authentication service is down"}', 503)
        args = self.reqparse.parse_args()
        try:
            resp = requests.post("http://127.0.0.1:5001/login", json=args, timeout=5)
        except Timeout:
            increase_auth_fail()
            return Response(json.dumps({"error": "Connection Timed Out"}), 408)
        if resp.status_code >= 500:
            increase_auth_fail()
        return Response(resp.content, resp.status_code)


class ShowProf(Resource):
    def get(self):
        if not check_prof_valid():
            return Response('{"error": "Profile service is down"}', 503)
        if apiLogic.is_valid(request.headers.get('token')):
            try:
                resp = requests.get("http://127.0.0.1:5002/showprof", headers={'token': request.headers.get('token')}, timeout=5)
            except Timeout:
                increase_prof_fail()
                return Response(json.dumps({"error": "Connection Timed Out"}), 408)
            if resp.status_code >= 500:
                increase_prof_fail()
            return Response(resp.content, resp.status_code)
        return Response('{"error": "invalid token"}', 401)


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

    def post(self):
        if not check_prof_valid():
            return Response('{"error": "Profile service is down"}', 503)
        args = self.reqparse.parse_args()
        if apiLogic.is_valid(request.headers.get('token')):
            try:
                resp = requests.post("http://127.0.0.1:5002/updateprof", json=args,
                                     headers={'token': request.headers.get('token')}, timeout=5)
            except Timeout:
                increase_prof_fail()
                return Response(json.dumps({"error": "Connection Timed Out"}), 408)
            if resp.status_code >= 500:
                increase_prof_fail()
            return Response(resp.content, resp.status_code)
        return Response('{"error": "invalid token"}', 401)


app = Flask(__name__)
api = Api(app)
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(ShowProf, '/showprof')
api.add_resource(UpdateProf, '/updateprof')

if __name__ == '__main__':
    app.run(port=5000, debug=True)