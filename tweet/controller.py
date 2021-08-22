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


class DeleteTweet(Resource):
    def delete(self, tweet_id):
        token = request.headers.get('token')
        if tweet_logic.is_token_valid(token):
            decode_token = tweet_logic.get_token(token)
            status = decode_token["status"]
            if status == "user":
                return Response(json.dumps({"error": "Users can not remove tweets"}), 403)
            tweet_logic.delete_tweet(tweet_id)
            return Response(json.dumps({"msg": "Tweet was deleted"}), 200)


class GetUserTweets(Resource):
    def get(self, user_name):
        token = request.headers.get('token')
        if tweet_logic.is_token_valid(token):
            user_tweets = tweet_logic.get_user_tweets(user_name)
            return user_tweets


class GetAllTweets(Resource):
    def get(self):
        token = request.headers.get('token')
        if tweet_logic.is_token_valid(token):
            user_tweets = tweet_logic.get_all_tweets()
            return user_tweets


app = Flask(__name__)
api = Api(app)
api.add_resource(AddTweet, '/addtweet/')
api.add_resource(DeleteTweet, '/deletetweet/<int:tweet_id>')
api.add_resource(GetAllTweets, '/gettweets/')
api.add_resource(GetUserTweets, '/gettweets/<string:user_name>')


if __name__ == '__main__':
    app.run(port=5004, debug=True)