from flask import Flask
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

HOST = 'localhost'
PORT = 5002

@app.route("/answer-voicemed", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("This is Sayon here, developing IVR. Thank you for calling Voice Med! We are testing!", voice='alice')

    return str(resp)

if __name__ == "__main__":
    app.run(host = HOST, port = PORT, debug = True)
