from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests

from tweet.logic import TweetLogic

tweet_logic = TweetLogic()


class AddTweet(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "tweet", type=str, required=True, help="The tweet must be provided", location="json"
        )

    def post(self):
        args = self.reqparse.parse_args()
        token = request.headers.get('token')
        if tweet_logic.is_token_valid(token):
            decode_token = tweet_logic.get_token(token)
            user_name = decode_token["username"]
            status = decode_token["status"]
            if status == "admin":
                return Response(json.dumps({"error": "Admins can not tweet"}), 403)
            tweet = args["tweet"]
            tweet_logic.add_tweet(user_name, tweet)
            return Response(json.dumps({"msg": "Tweet was saved"}), 200)


app = Flask(__name__)
api = Api(app)
api.add_resource(AddTweet, '/addtweet')

if __name__ == '__main__':
    app.run(port=5004, debug=True)