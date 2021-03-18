import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
import json

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

@app.route("/") 
def home_view(): 
        return "<h1>Bot Running</h1>"


slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call('auth.test')['user_id']





def SBIR(keyword):
    json_file_path = "sbir-search-results.json"
    f = open(json_file_path)
    data = json.load(f)
    grants = ''
    for item in data:
        if keyword in item['Description']:
            grants =  grants + '\n----------------------------------------------\n' + item['TopicTitle'] + '\n' + item['SBIRTopicLink']
    if not grants:
        grants = 'Keyword was not found'
    return grants

@slack_event_adapter.on('message')
def message(payload):

    event = payload.get('event', {})
    channel_id = event.get('channel')
    text = event.get('text')

    if text[0:8] == '!keyword':
        client.chat_postMessage(channel=channel_id, text=SBIR(str(text[9:])))

if __name__ == "__main__":
    app.run(debug=True)