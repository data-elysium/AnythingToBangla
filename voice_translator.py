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
import os

# Load environment variables from .env file
load_dotenv()

def voice_to_voice(audio_file):

    # transcript speech
    transcript = transcribe_audio(audio_file)

    if transcript.status == aai.TranscriptStatus.error:
        raise gr.Error(transcript.error)
    else:
        transcript = transcript.text

    # translate text
    list_translations = translate_text(transcript)
    generated_audio_paths = []

    # generate speech from text
    for translation in list_translations:
        translated_audio_file_name = text_to_speech(translation)
        path = Path(translated_audio_file_name)
        generated_audio_paths.append(path)


    return generated_audio_paths[0], list_translations[0]

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
def translate_text(text: str) -> str:

    languages = ["bn"]
    list_translations = []

    for lan in languages:
        translator = Translator(from_lang="autodetect", to_lang=lan)
        translation = translator.translate(text)
        list_translations.append(translation)

    return list_translations

# Function to generate speech
def text_to_speech(text: str) -> str:

    # ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(
        api_key= os.getenv("ELEVENLABS_API_KEY"),
    )

    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id=os.getenv("ELEVENLABS_VOICE_ID"), #clone your voice on elevenlabs dashboard and copy the id
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.8,
            style=0.5,
            use_speaker_boost=True,
        ),
    )

    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path


input_audio = gr.Audio(
    sources=["microphone"],
    type="filepath",
    show_download_button=True,
    waveform_options=gr.WaveformOptions(
        waveform_color="#01C6FF",
        waveform_progress_color="#0066B4",
        skip_length=2,
        show_controls=False,
    ),
)


with gr.Blocks() as demo:
    gr.Markdown("## Record yourself in English and immediately receive voice translations.")
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
                                ),)
            with gr.Row():
                submit = gr.Button("Submit", variant="primary")
                btn = gr.ClearButton(audio_input, "Clear")
                # btn.click(lambda: audio_input, None)

    with gr.Row():
        

        with gr.Group() as bangla:
            # gr.Image("flags/turkish.png", width = 150, show_download_button=False, show_label=False)
            bg_output = gr.Audio(label="Bangla", interactive=False)
            bg_text = gr.Markdown()

    output_components = [bg_output, bg_text]
    submit.click(fn=voice_to_voice, inputs=audio_input, outputs=output_components, show_progress=True)
           
        
if __name__ == "__main__":
    demo.launch()
