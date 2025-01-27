import jwt
from database import TweetDatabase


class TweetLogic:
    def __init__(self):
        self._secret = "sercert_password_asdfhn12234@#"
        self.db = TweetDatabase()

    def add_tweet(self, username, tweet):
        self.db.insert(username, tweet)

    def delete_tweet(self, tweet_id):
        self.db.delete(tweet_id)

    def get_user_tweets(self, user_name):
        return self.db.fetch_user(user_name)

    def get_all_tweets(self):
        return self.db.fetch_all()

    def is_token_valid(self, token):
        try:
            jwt.decode(token, self._secret, "HS256")
            return True
        except:
            return False

    def get_token(self, token):
        return jwt.decode(token, self._secret, "HS256")
