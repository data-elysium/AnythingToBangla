# Voice to Voice Translator

On this web app, you can record your voice in English and create translations of what you said in many different languages. And the best thing is, the created translations will be read out in your own voice.

![a screenshot of the interface](ss.png)

## Technologies Used
1. Gradio for the interface
2. AssemblyAI - for transcription
3. Python translate module - for translation of text
4. Elevenlabs - for reading translated text in your own voice

## API Keys Needed
* [AssemblyAI API key](https://www.assemblyai.com/?utm_source=youtube&utm_medium=referral&utm_campaign=yt_mis_66)
* [Elevenlabs API key](https://elevenlabs.io/)

Note: You need at least 30 minutes of a voice recording of yourself for *Professional voice cloning*. There is also a simpler voice cloning option that only requires 30 seconds of voice recording.

*Professional voice cloning is a paid feature.*

## Running with Docker
To run this application using Docker, follow these steps:

1. **Build the Docker Image**
   ```sh
   docker build -t bangla_app .
   ```

2. **Run the Docker Container** (Replace `YOUR_ASSEMBLYAI_API_KEY` and `YOUR_ELEVENLABS_API_KEY` with your actual API keys and `YOUR_VOICE_ID` with your voice id)
   ```sh
   docker run -p 7860:7860 \
       -e ASSEMBLY_AI_API_KEY=YOUR_ASSEMBLYAI_API_KEY \
       -e ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY \
       -e ELEVENLABS_VOICE_ID=YOUR_VOICE_ID \
       -d bangla_app
   ```

Now, your application should be running on `http://localhost:7860/`. Open this URL in your browser to access the app.

