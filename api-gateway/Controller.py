from flask import Flask, json, Response
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
        resp = requests.post("http://localhost:5001/signup", json=args)
        return Response(resp.content, resp.status_code)  # todo header needed?


api.add_resource(Signup, '/signup')

if __name__ == '__main__':
    app.run(port=5000, debug=True)