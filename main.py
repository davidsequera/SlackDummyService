from flask import Flask, Response, jsonify
from slackeventsapi import SlackEventAdapter
import os
from threading import Thread
from slack_sdk import WebClient


# This `app` represents your existing Flask app
app = Flask(__name__)

greetings = ["hi", "hello", "hello there", "hey"]

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
slack_token = os.environ['SLACK_BOT_TOKEN']
VERIFICATION_TOKEN = os.environ['VERIFICATION_TOKEN']

#instantiating slack client
slack_client = WebClient(slack_token)

# An example of one of your Flask app's routes

@app.route("/", methods=['GET'])
def hello():
    return "Hello I am Slack Server"


@app.route("/", methods=['POST'])
def event_hook():
    json_dict = request.json # json.loads(request.body.decode("utf-8"))
    if json_dict["token"] != VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
    return {"status": 500}
    return


slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app
)  


@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    def send_reply(value):
        event_data = value
        message = event_data["event"]
        if message.get("subtype") is None:
            command = message.get("text")
            channel_id = message["channel"]
            if any(item in command.lower() for item in greetings):
                message = (
                    "Hello <@%s>! :tada:"
                    % message["user"]  # noqa
                )
                slack_client.chat_postMessage(channel=channel_id, text=message)
    thread = Thread(target=send_reply, kwargs={"value": event_data})
    thread.start()
    return Response(status=200)


# Start the server on port 3000
if __name__ == "__main__":
  app.run(port=3000)



# from flask import Flask, request, jsonify
# import requests
# import os

# app = Flask(__name__)


# SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

# def verify_slack_request(req):
#     # You can add verification logic here using Slack's signature
#     pass



# @app.route('/slack/events', methods=['POST'])
# def slack_events():
#     data = request.json
#     # If the request is a challenge request, return the challenge value
#     if 'challenge' in data:
#         return jsonify({'challenge': data['challenge']})
#     # Verify request from Slack
#     if not verify_slack_request(request):
#         return "Unauthorized", 403

#     event = data.get('event', {})
    
#     # Check if this is a message event
#     if event.get('type') == 'message' and 'subtype' not in event:
#         user = event.get('user')
#         text = event.get('text')

#         # Greet the user if their name is mentioned in the message
#         if text:
#             # Check if the message contains a name
#             greeting = f"Hello {text}!"  # Simple greeting logic

#             # Respond with a greeting
#             send_message(user, greeting)

#     return '', 200

# def send_message(user, text):
#     # Send a message back to the user via Slack API
#     slack_api_url = 'https://slack.com/api/chat.postMessage'
#     headers = {
#         'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
#         'Content-Type': 'application/json',
#     }
#     payload = {
#         'channel': user,  # Sending direct message to the user
#         'text': text,
#     }
#     response = requests.post(slack_api_url, headers=headers, json=payload)
#     if response.status_code != 200:
#         print(f"Error sending message: {response.text}")

# if __name__ == '__main__':
#     app.run(port=5000)
