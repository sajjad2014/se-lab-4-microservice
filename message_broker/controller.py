from threading import Thread

from flask import Flask, json, Response, request
from flask_restful import Resource, Api, reqparse, abort, marshal, fields
import requests
import queue

from logic import MsgBrokerLogic

queue = queue.Queue()
msg_logic = MsgBrokerLogic()


class SubmitEvent(Resource):
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
        print(args)
        msg_logic.add_new_event(json.dumps(args))
        queue.put(args)
        return Response(json.dumps({"msg": "event saved"}), 200)


def send_events():
    while True:
        top = queue.get(block=True)
        event_type = top['type']
        if event_type == 'signup':
            requests.post("http://127.0.0.1:5002/eventhandler", json=top)
        elif event_type == 'updateprof':
            requests.post("http://127.0.0.1:5001/eventhandler", json=top)


app = Flask(__name__)
api = Api(app)
api.add_resource(SubmitEvent, '/submitevent')

if __name__ == '__main__':
    thread = Thread(target=send_events)
    thread.start()
    app.run(port=5006, debug=True)