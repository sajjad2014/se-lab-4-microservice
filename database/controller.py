from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
from database_logic import DatabaseLogic

database_logic = DatabaseLogic()

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
        try:
            database_logic.add_new_user(args["username"], args["password"], args["email"], args["mobile"])
        except:
            database_logic.refresh()
            return Response(json.dumps({"error": "query failed"}), 400)
        return "New user signed up"


class UpdateProfile(Resource):
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
        return database_logic.update_profile(args["username"], args["password"], args["email"], args["mobile"])


class GetUser(Resource):
    def get(self, username):
        prof = database_logic.get_profile(username)
        prof_dict = database_logic.decode_prof(prof)
        return prof_dict


app = Flask(__name__)
api = Api(app)
api.add_resource(Signup, '/signup')
api.add_resource(GetUser, '/getuser/<string:username>')
api.add_resource(UpdateProfile, '/updateprof')

if __name__ == '__main__':
    app.run(port=5003, debug=True)