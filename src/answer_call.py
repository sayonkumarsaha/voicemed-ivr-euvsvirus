from flask import Flask, request
import requests

from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

from authentication_data import ACCOUNT_SID, AUTH_TOKEN

app = Flask(__name__)

HOST = 'localhost'
PORT = 5002
FLOW_SID = 'FWac25b1a484074aa61f890ab06e5a97b2'

@app.route("/answer-voicemed", methods=['GET', 'POST'])
def answer_call():

    """Respond to incoming phone calls with a brief message."""

    # Start our TwiML response
    # resp = VoiceResponse()
    # Read a message aloud to the caller
    # resp.say("Welcome to VoiceMed Dev. Redirecting you the Flow!", voice='alice')
    # resp.record(timeout=10, transcribe=True)

    # Getting caller information
    caller = request.values.get('From')
    twilio_number = request.values.get('To')

    voicemed_client = Client(ACCOUNT_SID, AUTH_TOKEN)

    execution = voicemed_client.studio \
        .v1 \
        .flows(FLOW_SID) \
        .executions \
        .create(to=twilio_number, from_=caller)

    # return str(resp)
    return "Successfully made POST request"


if __name__ == "__main__":
    app.run(host = HOST, port = PORT, debug = True)
