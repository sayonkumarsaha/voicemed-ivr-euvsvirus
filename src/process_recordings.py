from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)

HOST = 'localhost'
PORT = 5002

CREDENTIAL_FILE = './VoiceMed-4b6f991d26a8.json'
BUCKET = 'voicemed-9f3f6.appspot.com'


@app.route("/fetch-call-recording", methods=['GET', 'POST'])
def fetch_call_recording():
    """Fetches voice recordings from Studio and stores in Firebase Storage."""

    acc_sid = request.values.get('AccountSid')
    call_sid = request.values.get('CallSid')
    rec_sid = request.values.get('RecordingSid')
    rec_url = request.values.get('RecordingUrl')
    rec_status = request.values.get('RecordingStatus')
    rec_duration = request.values.get('RecordingDuration')
    rec_channels = request.values.get('RecordingChannels')
    rec_start_time = request.values.get('RecordingStartTime')
    rec_source = request.values.get('RecordingSource')

    recording_data = (acc_sid, call_sid, rec_sid, rec_url, rec_status, rec_duration, rec_channels, rec_start_time,
                      rec_source)

    print(recording_data)

    # Explicitly use service account credentials by specifying the private key file.
    storage_client = storage.Client.from_service_account_json(CREDENTIAL_FILE)
    print(storage_client)

    bucket = storage_client.get_bucket(BUCKET)
    blob = bucket.blob('rec_id_'+str(rec_sid)+'.txt')
    blob.upload_from_string(''.join(recording_data))

    return "Successfully stored in Firebase Storage"


if __name__ == "__main__":
    app.run(host = HOST, port = PORT, debug = True)