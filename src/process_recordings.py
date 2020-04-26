from flask import Flask, request
from google.cloud import storage
import requests
import os

app = Flask(__name__)

FIREBASE_CREDENTIAL = './voicemed_storage.json'
FIREBASE_BUCKET = 'voicemedcalls-78bd8.appspot.com'

storage_client = storage.Client.from_service_account_json(FIREBASE_CREDENTIAL)

def _write_record_data(data, data_type, call_sid, rec_sid, rec_url):
    """Writes data on Firebase storage """

    bucket = storage_client.get_bucket(FIREBASE_BUCKET)

    # TODO: Add headers for the CSV from _fetch_record_data
    filename = str(call_sid) + "_" + data_type + '.txt'
    blob = bucket.blob(filename)
    blob.upload_from_string(data)

    # Downloading the recording URL and storing it on Firebase
    wav_filename = str(call_sid) + '_' + rec_sid + "_" + data_type + '.wav'
    blob = bucket.blob(wav_filename)
    r = requests.get(rec_url)
    with open(wav_filename, 'wb') as f:
        f.write(r.content)
    with open(wav_filename, 'rb') as f:
        blob.upload_from_file(f)
    if os.path.exists(wav_filename):
        os.remove(wav_filename)


def _fetch_record_data(request):
    """Fetches voice recordings data from Studio request """

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
        return rec_sid, call_sid, rec_url, recorded_data

    return rec_sid, None, None, None


# TODO: Instead of storing a separate file for each category, combine them in a csv and store one file per call_id

@app.route("/fetch-consent-recording", methods=['GET', 'POST'])
def fetch_consent_recording():
    """Fetches consent recordings from Studio and stores in Firebase Storage"""

    data_type = 'consent'
    rec_sid, call_sid, rec_url, consent_data = _fetch_record_data(request)
    if rec_sid:
        _write_record_data(consent_data, data_type, call_sid, rec_sid, rec_url)
        return "Successfully stored " + data_type + " recording in firebase storage"

    return "No recordings processed"


@app.route("/fetch-health-recording", methods=['GET', 'POST'])
def fetch_health_recording():
    """Fetches health recordings from Studio and stores in Firebase Storage"""

    data_type = 'health'
    rec_sid, call_sid, rec_url, consent_data = _fetch_record_data(request)
    if rec_sid:
        _write_record_data(consent_data, data_type, call_sid, rec_sid, rec_url)
        return "Successfully stored " + data_type + " recording in firebase storage"

    return "No recordings processed"


@app.route("/fetch-cough-recording", methods=['GET', 'POST'])
def fetch_cough_recording():
    """Fetches cough recordings from Studio and stores in Firebase Storage"""

    data_type = 'cough'
    rec_sid, call_sid, rec_url, consent_data = _fetch_record_data(request)
    if rec_sid:
        _write_record_data(consent_data, data_type, call_sid, rec_sid, rec_url)
        return "Successfully stored " + data_type + " recording in firebase storage"

    return "No recordings processed"


@app.route("/fetch-breath-recording", methods=['GET', 'POST'])
def fetch_breath_recording():
    """Fetches breath recordings from Studio and stores in Firebase Storage"""

    data_type = 'breath'
    rec_sid, call_sid, rec_url, consent_data = _fetch_record_data(request)
    if rec_sid:
        _write_record_data(consent_data, data_type, call_sid, rec_sid, rec_url)
        return "Successfully stored " + data_type + " recording in firebase storage"

    return "No recordings processed"


@app.route("/fetch-speech-recording", methods=['GET', 'POST'])
def fetch_speech_recording():
    """Fetches speech recordings from Studio and stores in Firebase Storage"""

    data_type = 'speech'
    rec_sid, call_sid, rec_url, consent_data = _fetch_record_data(request)
    if rec_sid:
        _write_record_data(consent_data, data_type, call_sid, rec_sid, rec_url)
        return "Successfully stored " + data_type + " recording in firebase storage"

    return "No recordings processed"


# app.run(host = 'localhost', port = 5002, debug = True)
# Threaded option to enable multiple instances for multiple user access support
app.run(threaded=True, port=5002)
