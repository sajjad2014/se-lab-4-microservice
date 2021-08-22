from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
import jwt

from profile_logic import ProfileLogic

profile_logic = ProfileLogic()


class ShowProf(Resource):

    def get(self, username):
        prof = profile_logic.get_profile(username)
        prof = profile_logic.decode_prof(prof)  # dict
        prof['password'] = len(prof['password']) * '*'
        return Response(json.dumps(prof), 200)


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
        args = self.reqparse.parse_args()
        token = request.headers.get('token')
        decode_token = profile_logic.decode_token(token)
        username = decode_token["username"]
        args["username"] = username
        prof = profile_logic.update_profile(args["username"], args["password"], args["email"], args["mobile"])
        print(self.get_json(args, decode_token))
        requests.post("http://127.0.0.1:5006/submitevent", json=self.get_json(args, decode_token))
        prof['password'] = len(prof['password']) * '*'
        return Response(json.dumps(prof), 200)

    def get_json(self, args, decode_token):
        return {'type': 'updateprof',
                'data': json.dumps({
                    'header': decode_token,
                    'payload': args})}


class EventHandler(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "type", type=str, required=True, help="The event type must be provided", location="json"
        )
        self.reqparse.add_argument(
            "data", type=str, required=True, help="The event data must be provided", location="json"
        )

    def post(self):
        args = self.reqparse.parse_args()
        data = args["data"]
        payload = json.loads(data)["payload"]
        profile_logic.add_new_user(payload['username'], payload['password'], payload['email'], payload['mobile'])
        return Response(json.dumps({"msg": "New user signed up"}), 200)


app = Flask(__name__)
api = Api(app)
api.add_resource(ShowProf, '/showprof/<string:username>')
api.add_resource(UpdateProf, '/updateprof')
api.add_resource(EventHandler, '/eventhandler')

if __name__ == '__main__':
    app.run(port=5002, debug=True)
