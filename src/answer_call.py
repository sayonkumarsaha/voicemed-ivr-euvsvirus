from flask import Flask
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

HOST = 'localhost'
PORT = 5002

@app.route("/answer-call", methods=['GET', 'POST'])
def answer_call():
    """Respond to incoming phone calls."""

    # Start TwiML response
    resp = VoiceResponse()
    # Read a message aloud to the caller
    resp.say("Welcome to VoiceMed Dev. Redirecting you the Flow!", voice='alice')
    # Record the message if needed
    # resp.record(timeout=10, transcribe=True)

    return str(resp)


if __name__ == "__main__":
    app.run(host = HOST, port = PORT, debug = True)
