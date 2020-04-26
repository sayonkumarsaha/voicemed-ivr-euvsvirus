from flask import Flask, request
from google.cloud import storage
import urllib.request

app = Flask(__name__)

HOST = 'localhost'
PORT = 5002

#CREDENTIAL_FILE = './VoiceMed-4b6f991d26a8.json.json'
#BUCKET = 'voicemed-9f3f6.appspot.com'

STORAGE_CREDENTIAL = './voicemed_storage_credentials.json'
BUCKET= 'voicemedcalls-78bd8.appspot.com'


def _fetch_record_data(request):
    """Fetches voice recordings from Studio given the request """

    rec_sid = request.values.get('RecordingSid')

    if rec_sid:
        acc_sid = request.values.get('AccountSid')
        call_sid = request.values.get('CallSid')
        rec_url = request.values.get('RecordingUrl')
        rec_status = request.values.get('RecordingStatus')
        rec_duration = request.values.get('RecordingDuration')
        rec_channels = request.values.get('RecordingChannels')
        rec_start_time = request.values.get('RecordingStartTime')
        rec_source = request.values.get('RecordingSource')

        separator = ','
        recorded_data = str(acc_sid) + separator \
                        + str(call_sid) + separator \
                        + str(rec_sid) + separator \
                        + str(rec_url) + separator \
                        + str(rec_status) + separator \
                        + str(rec_duration) + separator \
                        + str(rec_channels) + separator \
                        + str(rec_start_time) + separator \
                        + str(rec_source)
        return rec_sid, call_sid, recorded_data

    return rec_sid, None, None


@app.route("/fetch-consent-recording", methods=['GET', 'POST'])
def fetch_consent_recording():
    """Fetches consent recordings from Studio and stores in Firebase Storage."""

    TYPE = 'consent'
    rec_sid, call_sid, consent_data = _fetch_record_data(request)

    if rec_sid:
        filename = TYPE + '_call_sid_' + str(call_sid) + '_rec_sid_' + str(rec_sid) + '.txt'
        storage_client = storage.Client.from_service_account_json(STORAGE_CREDENTIAL)
        bucket = storage_client.get_bucket(BUCKET)
        blob = bucket.blob(filename)
        blob.upload_from_string(consent_data)

        return "Successfully stored Consent Recording in Firebase Storage"

    return "No recordings processed"


@app.route("/fetch-health-recording", methods=['GET', 'POST'])
def fetch_health_recording():
    """Fetches consent recordings from Studio and stores in Firebase Storage."""

    TYPE = 'health'
    rec_sid, call_sid, health_data = _fetch_record_data(request)

    if rec_sid:
        filename = TYPE + '_call_sid_' + str(call_sid) + '_rec_sid_' + str(rec_sid) + '.txt'
        storage_client = storage.Client.from_service_account_json(STORAGE_CREDENTIAL)
        bucket = storage_client.get_bucket(BUCKET)
        blob = bucket.blob(filename)
        blob.upload_from_string(health_data)

        return "Successfully stored Health Recording in Firebase Storage"

    return "No recordings processed"


if __name__ == "__main__":
    app.run(host = HOST, port = PORT, debug = True)