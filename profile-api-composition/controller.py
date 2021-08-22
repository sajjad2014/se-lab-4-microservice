from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests


class ShowProf(Resource):
    def __init__(self):
        self._secret = "sercert_password_asdfhn12234@#"

    def get(self, username):
        # user profile
        profile_req = requests.get("http://127.0.0.1:5002/showprof/" + username,
                            headers={'token': request.headers.get('token')})
        # user tweets
        tweets_req = requests.get("http://127.0.0.1:5004/gettweets/" + username,
                              headers={'token': request.headers.get('token')})
        return Response('{"body": ' + profile_req.content + ', "tweets": ' + tweets_req.content + '}', 200)

app = Flask(__name__)
api = Api(app)
api.add_resource(ShowProf, '/showprof/<string:username>')

if __name__ == '__main__':
    app.run(port=5005, debug=True)