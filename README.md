## VoiceMed IVR: EUvsVirus Hackathon 2020

The code in this repositiory builds an end to end **Interactive Voice Reponse System (IVR)** for **[VoiceMed](https://www.voicemed.io/)** product during the 48hrs [EuVsVirus](https://euvsvirus.org/) Hackathon. [[DevPost](https://devpost.com/software/voicemed-1z3b0r) of the project]

#### IVR Workflows

- The **workflow for the IVR** is created using [Twilio](https://www.twilio.com/) and  [Studio](https://www.twilio.com/docs/studio) feature. [Twilio](https://www.twilio.com/) was decided for our use-case after doing research on other IVR providers such as Speechly, Vonyage, Voximplant, and Plivo.
- The static JSON format of the IVR workflow [CollectVoiceSamples](https://www.twilio.com/console/studio/flows/FWa396c402ec28276a2d800876d4f241ff) exists in `src/voicemed_script.json`.
- The IVR workflow [CollectVoiceSamples](https://www.twilio.com/console/studio/flows/FWa396c402ec28276a2d800876d4f241ff) is triggered by **inbound calls** from a [certain set of phone numbers](https://www.twilio.com/console/phone-numbers/incoming) we purchased from [Twilio](https://www.twilio.com/). You can use Hangout to call the US numbers on the [list](https://www.twilio.com/console/phone-numbers/incoming) for free.

#### Data Collection and Storage

- As and when the voice is recorded in workflow [CollectVoiceSamples](https://www.twilio.com/console/studio/flows/FWa396c402ec28276a2d800876d4f241ff), the **recorded data** is pulled using `src/process_recordings.py` for different categories of such as consent, health, cough, breath, speech. This runs on a Python server by deploying this repository using [Heroku](https://www.heroku.com/) explained later.
- The **data is organized** as per the category for every call in `src/process_recordings.py` and stored in [GCP Firebase](https://console.cloud.google.com/storage/browser/voicemedcalls-78bd8.appspot.com/CAd21d5f42c6225900dcdbe599b114dc5e/?forceOnBucketsSortingFiltering=false&authuser=2&project=voicemedcalls-78bd8) for which the authentication lies at `voicemed_storage.json`. For every call, a single folder is created with the call_id. Each of these folder has a `.txt` file of metadata per category, a `.wav` file of recording per category, resulting in total 10 files from 5 categories for a complete IVR call.

#### Production Deployment

-  On **production**, we use the [free version of Heroku](https://www.heroku.com/pricing) for hosting the app. We use the [Heroku Command Line](https://devcenter.heroku.com/categories/command-line) manually to **build and deploy** the [VoiceMed app](https://dashboard.heroku.com/apps/voice-med). CI/CD is not yet integrated. Once we **create the app** using `heroku create voice-med` in the [Heroku Command Line](https://devcenter.heroku.com/categories/command-line), we include the `Procfile` file before pushing the code in this repository with `git push heroku master`. More information in [this tutorial](https://medium.com/better-programming/how-to-get-your-flask-app-running-on-heroku-892030811c0f).
- You can **manually run the script** using `heroku run -a voice-med python src/process_recordings.py`. Once the application is running, you can **view logs** using `heroku logs --tail` while phone calls are being made or the application is broken.

#### Extra for Dev

- If you want to play around with **[Programmable Voice features of Twilio](https://www.twilio.com/docs/voice)**, a good starting point is using the scripts `src/trigger_studio_from_call.py` and `src/answer_call.py`. We could not use it because [Twilio](https://www.twilio.com/) doesn't allow HTTP Post requests for inbound-calls. It only allows REST API for inbound-calls. So we directly hook the [phone numbers](https://www.twilio.com/console/phone-numbers/incoming) to the workflow [CollectVoiceSamples](https://www.twilio.com/console/studio/flows/FWa396c402ec28276a2d800876d4f241ff). The  [Heroku](https://www.heroku.com/) server explained later is used only for collection and storage of data.
- If you want to **run this on local**, make sure to port your `localhost` to [Ngrok](https://ngrok.com/) as explained in this [tutorial](https://www.twilio.com/docs/voice/tutorials/how-to-respond-to-incoming-phone-calls-python).