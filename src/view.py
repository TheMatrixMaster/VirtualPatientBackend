from __future__ import division
import functools
import io
import os
import re
import sys
import time

from flask import (
    Blueprint,
    g,
    session,
    abort,
    request,
    Response,
    json
)

import keyboard
from playsound import playsound

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from google.cloud import texttospeech
import watson_developer_cloud


bp = Blueprint('view', __name__)


service = watson_developer_cloud.AssistantV2(
    iam_apikey='d7Gfh-2Zlm0vOGKjz067jZtTx8yM8C6Y0vrMmwH_05VT',
    version='2018-11-08',
    url='https://gateway.watsonplatform.net/assistant/api'
 )


@bp.route('/api/speech_to_text', methods=['GET'])
def speech_to_text():

    print('button pressed')
    os.system('python D:/Hackathons/VirtualPatient/src/record.py')
    file_name = "D:/Hackathons/VirtualPatient/output.wav"

    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')

    try:
        # Detects speech in the audio file
        response = client.recognize(config, audio)
        print(response)

        for result in response.results:
            data = {
                    'msg': result.alternatives[0].transcript,
                    'counter': 1
                    }
            resp = Response(json.dumps(data), status=200, mimetype='application/json')
            resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp

    except:
        data = {   
                'msg': "Your message was not picked up, please try again.",
                'counter': 0
                }
        resp = Response(json.dumps(data), status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'

        
        return resp


@bp.route('/api/text_to_speech/<string:client_prompt>', methods=['GET'])
def text_to_speech(client_prompt):

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    response = service.message(
        assistant_id='f3d20759-dfa8-48ec-8f66-a18ea3d517ec',
        session_id='57dfd18b-ffe8-4bc2-bb4f-9992d1decefc',
        input={
            'message_type': 'text',
            'text': client_prompt
        }
    ).get_result()

    try:
        server_r = json.dumps(response, indent=2)
        server_r = json.loads(server_r)
        server_resp = server_r['output']['generic'][0]['text']
        server_intent = server_r['output']['generic'][0]['intent']
    except:
        server_resp = "I don't know how to answer that question, please elaborate."

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=server_resp)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    #The response's audio_content is binary.
    if os.path.exists('patient.mp3'): os.remove('patient.mp3')
    with open('patient.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file')

    playsound('patient.mp3')

    data = {'msg': server_resp,
            'intent': server_intent}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp