import os
import numpy as np
import gradio as gr
import assemblyai as aai
from translate import Translator
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pathlib import Path
from dotenv import load_dotenv
from io import BytesIO
import soundfile as sf

# Load environment variables from .env file
load_dotenv()

def voice_to_voice(audio_file):
    # Transcribe speech
    transcript = transcribe_audio(audio_file)

    if transcript.status == aai.TranscriptStatus.error:
        raise gr.Error(transcript.error)
    else:
        transcript = transcript.text

    # Translate text
    list_translations = translate_text(transcript)
    generated_audio_data = []

    # Generate speech from text
    for translation in list_translations:
        audio_tuple = text_to_speech(translation)
        generated_audio_data.append(audio_tuple)

    return generated_audio_data[0], list_translations[0]

# Function to transcribe audio using AssemblyAI
def transcribe_audio(audio_file):
    aai.settings.api_key = os.getenv("ASSEMBLY_AI_API_KEY")

    config = aai.TranscriptionConfig(language_detection=True)
    transcriber = aai.Transcriber(config=config)

    transcript = transcriber.transcribe(audio_file)
    print(f"Language : {transcript.json_response['language_code']}")
    print(f"Transcript: {transcript.text}")

    return transcript

# Function to translate text
def translate_text(text: str) -> list:
    languages = ["bn"]
    list_translations = []

    for lan in languages:
        translator = Translator(from_lang="autodetect", to_lang=lan)
        translation = translator.translate(text)
        list_translations.append(translation)

    return list_translations

# Function to generate speech without storing as a file
def text_to_speech(text: str):
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    response = client.text_to_speech.convert(
        voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.8,
            style=0.5,
            use_speaker_boost=True,
        ),
    )

    audio_bytes = BytesIO()
    for chunk in response:
        if chunk:
            audio_bytes.write(chunk)
    
    audio_bytes.seek(0)  # Reset buffer position
    
    # Convert BytesIO to NumPy array
    audio_data, sample_rate = sf.read(audio_bytes, dtype='int16')
    return sample_rate, audio_data

with gr.Blocks() as demo:
    gr.Markdown("## Record yourself and immediately receive voice translations.")
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"],
                                   type="filepath",
                                   show_download_button=True,
                                   waveform_options=gr.WaveformOptions(
                                       waveform_color="#01C6FF",
                                       waveform_progress_color="#0066B4",
                                       skip_length=2,
                                       show_controls=False,
                                   ))
            with gr.Row():
                submit = gr.Button("Submit", variant="primary")
                btn = gr.ClearButton(audio_input, "Clear")

    with gr.Row():
        with gr.Group() as bangla:
            bg_output = gr.Audio(label="Bangla", interactive=False)
            bg_text = gr.Markdown()

    output_components = [bg_output, bg_text]
    submit.click(fn=voice_to_voice, inputs=audio_input, outputs=output_components, show_progress=True)

if __name__ == "__main__":
    demo.launch()
