# chatbot.py

import requests
import json
import time
import aispeech  # Import the entire module, not just the function
import html  # Import the html module for decoding HTML entities

conversation_log = []  # Maintain a structured conversation log
AI_RESPONSE_FILENAME = 'ai-response.txt'
logging_eventhandlers = []

# Get the initialized TTS model from aispeech module
tts_model = aispeech.initialize_tts_model()  # Replace 'tts_model' with the actual variable name
gpt_cond_latent, speaker_embedding = aispeech.compute_speaker_latents(tts_model)

def send_user_input(user_input):
    global conversation_log

    log_message(f"User: {user_input}")

    # Add the user's input to the conversation log with role 'user'
    conversation_log.append({"role": "user", "content": user_input})

    url = "http://localhost:5000/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "mode": "chat",
        "character": "example",
        "messages": conversation_log
    }

    response = requests.post(url, headers=headers, json=data, verify=False)

    if response.status_code == 200:
        assistant_message = response.json()['choices'][0]['message']['content']

        # Decode HTML entities to their actual characters
        assistant_message = html.unescape(assistant_message)

        log_message(f'AI: {assistant_message}')

        # Add the AI's response to the conversation log with role 'assistant'
        conversation_log.append({"role": "assistant", "content": assistant_message})

        # Use 'tts_and_play_audio' from 'aispeech' to process and play the AI response
        aispeech.tts_and_play_audio(assistant_message, tts_model, gpt_cond_latent, speaker_embedding)  # Pass the AI's response and the TTS model to the function
        time.sleep(0.1)
    else:
        print(f"Error: Status code {response.status_code}")

def log_message(message_text):
    print(message_text)
    global logging_eventhandlers
    for eventhandler in logging_eventhandlers:
        eventhandler(message_text)


if __name__ == '__main__':
    while True:
        # This is just a placeholder for testing; you won't need to manually enter the text here.
        user_input = input("Enter your message: ")

        # Call the function to send the user's input to the new API
        send_user_input(user_input)
