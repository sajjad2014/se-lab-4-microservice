from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
import jwt


class ShowProf(Resource):
    def __init__(self):
        self._secret = "sercert_password_asdfhn12234@#"

    def get(self):
        token = request.headers.get('token')
        username = jwt.decode(token, self._secret, "HS256")["username"]
        resp = requests.get("http://127.0.0.1:5003/getuser/" + username)
        return Response(resp.content, resp.status_code)


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
        resp = requests.post("http://127.0.0.1:5003/updateprof", json=args)
        return Response(resp.content, resp.status_code)


app = Flask(__name__)
api = Api(app)
api.add_resource(ShowProf, '/showprof')
api.add_resource(UpdateProf, '/updateprof')

if __name__ == '__main__':
    app.run(port=5002, debug=True)