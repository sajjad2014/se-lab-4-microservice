from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
import jwt
from profile_logic import ProfileLogic

profile_logic = ProfileLogic()

class ShowProf(Resource):
    def __init__(self):
        self._secret = "sercert_password_asdfhn12234@#"

    def get(self):
        token = request.headers.get('token')
        username = jwt.decode(token, self._secret, "HS256")["username"]
        prof = profile_logic.get_profile(username)
        prof = profile_logic.decode_prof(prof)  # dict
        prof['password'] = len(prof['password']) * '*'
        return Response(json.dumps(prof), 200)


class UpdateProf(Resource):
    def __init__(self):
        self._secret = "sercert_password_asdfhn12234@#"
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
        args = self.reqparse.parse_args()
        token = request.headers.get('token')
        username = jwt.decode(token, self._secret, "HS256")["username"]
        args["username"] = username
        prof = profile_logic.update_profile(args["username"], args["password"], args["email"], args["mobile"])
        prof['password'] = len(prof['password']) * '*'
        return Response(json.dumps(prof), 200)


app = Flask(__name__)
api = Api(app)
api.add_resource(ShowProf, '/showprof')
api.add_resource(UpdateProf, '/updateprof')

if __name__ == '__main__':
    app.run(port=5002, debug=True)