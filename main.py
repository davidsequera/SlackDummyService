from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)


SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')

def verify_slack_request(req):
    # You can add verification logic here using Slack's signature
    pass

@app.route('/slack/events', methods=['POST'])
def slack_events():
    # Verify request from Slack
    if not verify_slack_request(request):
        return "Unauthorized", 403

    data = request.json
    event = data.get('event', {})
    
    # Check if this is a message event
    if event.get('type') == 'message' and 'subtype' not in event:
        user = event.get('user')
        text = event.get('text')

        # Greet the user if their name is mentioned in the message
        if text:
            # Check if the message contains a name
            greeting = f"Hello {text}!"  # Simple greeting logic

            # Respond with a greeting
            send_message(user, greeting)

    return '', 200

def send_message(user, text):
    # Send a message back to the user via Slack API
    slack_api_url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
        'Content-Type': 'application/json',
    }
    payload = {
        'channel': user,  # Sending direct message to the user
        'text': text,
    }
    response = requests.post(slack_api_url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")

if __name__ == '__main__':
    app.run(port=5000)
