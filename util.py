import webcolors
import assemblyai as aai
import os
import string
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
import requests
import streamlit as st

DEEPGRAM_URL = "https://api.deepgram.com/v1/speak?model=aura-luna-en"

ASSEMBLY_AI_API_KEY = st.secrets["ASSEMBLY_AI_API_KEY"]
DEEPGRAM_API_KEY = st.secrets["DEEPGRAM_API_KEY"]
ELEVEN_LABS_API_KEY = st.secrets["ELEVEN_LABS_API_KEY"]

def closest_colour(requested_colour):
    min_colours = {}
    for name in webcolors.names("css3"):
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def speech_to_text(audio_path) :
    try :
        aai.settings.api_key = ASSEMBLY_AI_API_KEY

        config = aai.TranscriptionConfig(language_detection=True, punctuate=True, format_text=True)

        transcriber = aai.Transcriber(config=config)

        transcript = transcriber.transcribe(audio_path)

        if transcript.status == aai.TranscriptStatus.error:
            return "Error"
        else :
            return transcript.text
    except Exception as e:
        return "Error"
    
def text_to_speech(text) :
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    
    text = text.translate(str.maketrans('', '', string.punctuation))
    text_lower = text.lower()

    payload = {
        "text": text_lower
    }

    audio_file_path = "./temp/temp_audio_play.mp3"  # Path to save the audio file

    with open(audio_file_path, 'wb') as file_stream:
        response = requests.post(DEEPGRAM_URL, headers=headers, json=payload, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file_stream.write(chunk) # Write each chunk of audio data to the file

    return audio_file_path

def text_to_speech_spanish(text) :
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/cgSgspJ2msm6clMCkdW9"

    headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVEN_LABS_API_KEY
    }

    data = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
    }

    audio_file_path = "./temp/temp_audio_play_spanish.mp3"

    response = requests.post(url, json=data, headers=headers)
    with open(audio_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    return audio_file_path
