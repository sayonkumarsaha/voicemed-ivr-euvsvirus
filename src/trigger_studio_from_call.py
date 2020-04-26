from flask import Flask, request
from twilio.rest import Client
from authentication_data import ACCOUNT_SID, AUTH_TOKEN

app = Flask(__name__)

HOST = 'localhost'
PORT = 5002
FLOW_SID = 'FWac25b1a484074aa61f890ab06e5a97b2'


@app.route("/trigger-studio-from-call", methods=['GET', 'POST'])
def trigger_studio_from_call():
    """Respond to incoming phone calls."""

    # Getting caller information
    caller_number = request.values.get('From')
    twilio_number = request.values.get('To')

    voicemed_client = Client(ACCOUNT_SID, AUTH_TOKEN)
    # Issue: Twilio allows POST request to Studio for Outbound Calls but doesn't allow for Inbound Calls
    # TODO: Contract with Twilio to get the service for our use-case
    execution = voicemed_client.studio \
        .v1 \
        .flows(FLOW_SID) \
        .executions \
        .create(to=twilio_number, from_=caller_number)

    return "Successfully made POST request"


if __name__ == "__main__":
    app.run(host = HOST, port = PORT, debug = True)
