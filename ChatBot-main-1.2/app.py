from flask import Flask, render_template, request, jsonify



import openai

import pyttsx3

import os
from gtts import gTTS
import time

openai.api_key = "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"

messages = [{"role": "system", "content": "You are a Mental consultant and friend ,give fast and short answer and your answe should be in 30 words , if anyone ask you about your name then answer Andy, you are made by code Pentane Team"}]




app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():

    try:
        user_input = request.form["msg"]

        # Generate a text response using OpenAI GPT
        text_response = CustomChatGPT(user_input)

        # Convert the text response to voice using gTTS
        voice_path = generate_voice_response(text_response)

        # Return both text and voice responses
        return jsonify({'text_response': text_response, 'voice_response': voice_path})
    except Exception as e:
        return jsonify({'error': str(e)})

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

def generate_voice_response(text_response):
    timestamp = int(time.time())
    voice_path = f'static/voice_response_{timestamp}.mp3'
    voice_response = gTTS(text=text_response, lang='en', slow=False)
    voice_response.save(voice_path)

    # Play the audio response
    engine = pyttsx3.init()
    engine.say(text_response)
    engine.runAndWait()
    engine.stop()

    # Delete the audio file after playing
    os.remove(voice_path)

    return voice_path

if __name__ == '__main__':
    app.run(debug=True)


