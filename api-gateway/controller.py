from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
from requests.exceptions import Timeout
from api_gateway_logic import APILogic
import time

apiLogic = APILogic()


auth_fail_count = 0
prof_fail_count = 0
tweet_fail_count = 0
pac_fail_count = 0      # pac stands for profile API composition

auth_available = True
prof_available = True
tweet_available = True
pac_available = True

auth_start_fail = None
prof_start_fail = None
tweet_start_fail = None
pac_start_fail = None

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

def increase_tweet_fail():
    global tweet_fail_count, tweet_available, tweet_start_fail
    tweet_fail_count += 1
    if tweet_fail_count == 3:
        tweet_available = False
        tweet_fail_count = 0
        tweet_start_fail = current_seconds()

def increase_pac_fail():
    global pac_fail_count, pac_available, pac_start_fail
    pac_fail_count += 1
    if pac_fail_count == 3:
        pac_available = False
        pac_fail_count = 0
        pac_start_fail = current_seconds()

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

def check_tweet_valid():
    global tweet_available, tweet_fail_count
    if tweet_start_fail is None or current_seconds() - tweet_start_fail > 30:
        tweet_available = True
        return True
    return False

def check_pac_valid():
    global pac_available, pac_fail_count
    if pac_start_fail is None or current_seconds() - pac_start_fail > 30:
        pac_available = True
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
    def get(self, username):
        if not check_pac_valid():
            return Response('{"error": "Profile-api-composition service is down"}', 503)
        if not apiLogic.is_valid(request.headers.get('token')):
            return Response('{"error": "invalid token"}', 401)
        try:
            resp = requests.get("http://127.0.0.1:5005/showprof/" + username,
                                headers={'token': request.headers.get('token')}, timeout=5)
        except Timeout:
            increase_pac_fail()
            return Response(json.dumps({"error": "Connection Timed Out"}), 408)
        if resp.status_code >= 500:
            increase_pac_fail()
        return Response(resp.content, resp.status_code)



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
        if not apiLogic.is_valid(request.headers.get('token')):
            return Response('{"error": "invalid token"}', 401)
        try:
            resp = requests.post("http://127.0.0.1:5002/updateprof", json=args,
                                 headers={'token': request.headers.get('token')}, timeout=5)
        except Timeout:
            increase_prof_fail()
            return Response(json.dumps({"error": "Connection Timed Out"}), 408)
        if resp.status_code >= 500:
            increase_prof_fail()
        return Response(resp.content, resp.status_code)


class AddTweet(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "tweet", type=str, required=True, help="The tweet must be provided", location="json"
        )

    def post(self):
        if not check_tweet_valid():
            return Response('{"error": "Tweet service is down"}', 503)
        args = self.reqparse.parse_args()
        if not apiLogic.is_valid(request.headers.get('token')):
            return Response('{"error": "invalid token"}', 401)
        try:
            resp = requests.post("http://127.0.0.1:5004/addtweet", json=args,
                                 headers={'token': request.headers.get('token')}, timeout=5)
        except Timeout:
            increase_tweet_fail()
            return Response(json.dumps({"error": "Connection Timed Out"}), 408)
        if resp.status_code >= 500:
            increase_tweet_fail()
        return Response(resp.content, resp.status_code)


class DeleteTweet(Resource):
    def delete(self, id):
        if not check_tweet_valid():
            return Response('{"error": "Tweet service is down"}', 503)
        if not apiLogic.is_valid(request.headers.get('token')):
            return Response('{"error": "invalid token"}', 401)
        try:
            resp = requests.delete("http://127.0.0.1:5004/deletetweet/" + str(id),
                                 headers={'token': request.headers.get('token')}, timeout=5)
        except Timeout:
            increase_tweet_fail()
            return Response(json.dumps({"error": "Connection Timed Out"}), 408)
        if resp.status_code >= 500:
            increase_tweet_fail()
        return Response(resp.content, resp.status_code)


class Dashboard(Resource):
    def get(self):
        if not check_tweet_valid():
            return Response('{"error": "Tweet service is down"}', 503)
        if not apiLogic.is_valid(request.headers.get('token')):
            return Response('{"error": "invalid token"}', 401)
        try:
            resp = requests.get("http://127.0.0.1:5004/dashboard",
                                 headers={'token': request.headers.get('token')}, timeout=5)
        except Timeout:
            increase_tweet_fail()
            return Response(json.dumps({"error": "Connection Timed Out"}), 408)
        if resp.status_code >= 500:
            increase_tweet_fail()
        return Response(resp.content, resp.status_code)


app = Flask(__name__)
api = Api(app)
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(ShowProf, '/showprof/<string:username>')
api.add_resource(UpdateProf, '/updateprof')
api.add_resource(AddTweet, '/addtweet')
api.add_resource(DeleteTweet, '/deletetweet/<int:id>')
api.add_resource(Dashboard, '/dashboard')

if __name__ == '__main__':
    app.run(port=5000, debug=True)