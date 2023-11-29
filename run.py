from pickle import TRUE
import re
import speech_recognition as sr
import pyttsx3
import json
import requests
import traceback
import chatbot
import wave
import pyaudio
import whisper
from typing import Optional
import time
import whisper
from threading import Thread
from threading import Thread
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

whisper_filter_list = ['you', 'thank you.',
                       'thanks for watching.', "Thank you for watching."]

MIC_OUTPUT_FILENAME = "outfile.wav"
VOICE_OUTPUT_FILENAME = "audioResponse.wav"

logging_eventhandlers = []

def initialize_model():
    global model
    model = whisper.load_model("base")

auto_recording = False

def tts_and_play_audio(text, model):
    print(f"Text received: {text}")
    print("Inference...")
    t0 = time.time()
    chunks = model.inference_stream(
        text,
        "en",
        gpt_cond_latent,  # Replace with your actual values
        speaker_embedding  # Replace with your actual values
    )

    wav_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            print(f"Time to first chunk: {time.time() - t0}")
        print(f"Received chunk {i} of audio length {chunk.shape[-1]}")
        wav_chunks.append(chunk)

    # Concatenate audio chunks
    wav = torch.cat(wav_chunks, dim=0)

    # Save the audio file
    torchaudio.save("xtts_streaming.wav", wav.squeeze().unsqueeze(0).cpu(), 24000)

    # Play the audio using sounddevice
    sounddevice.play(wav.squeeze().cpu().numpy(), 24000, blocking=True)

def handle_input(input_text: Optional[str] = None):
    if input_text is not None:
        # If text input is provided, use it
        user_input = input_text
    else:
        # If no text input, listen to the microphone
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            print("Speak now or enter text:")
            try:
                if input_text is None:
                    audio = r.listen(source, timeout=5)  # Adjust timeout as needed
                else:
                    audio = r.listen(source, timeout=0)  # For text input, set timeout to 0
            except sr.WaitTimeoutError:
                print("Timeout. No input received.")
                return

            with open(MIC_OUTPUT_FILENAME, "wb") as file:
                file.write(audio.get_wav_data())
                print("Transcribing")
                global model
                initialize_model()
                audio = whisper.load_audio(MIC_OUTPUT_FILENAME)
                audio = whisper.pad_or_trim(audio)
                mel = whisper.log_mel_spectrogram(audio).to(model.device)
                options = whisper.DecodingOptions(
                    task='transcribe',
                    language='english',
                    without_timestamps=True,
                    fp16=False if model.device == 'cpu' else None
                )
                result = whisper.decode(model, mel, options)
                user_input = result.text
                global whisper_filter_list
                if user_input == '':
                    return
                print('filtering')
                if user_input.strip().lower() in whisper_filter_list:
                    print('Input filtered.')
                    return

    # Send the user input to your chatbot or processing logic
    chatbot.send_user_input(user_input)

def start_record_auto():
    global auto_recording
    auto_recording = True
    thread = Thread(target=start_STTS_loop_chat)
    thread.start()

def start_STTS_loop_chat():
    global auto_recording
    while auto_recording:
        listen()

def stop_record_auto():
    global auto_recording, ambience_adjusted
    auto_recording = False
    ambience_adjusted = False

def listen():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Speak now")
        audio = r.listen(source)
        with open(MIC_OUTPUT_FILENAME, "wb") as file:
            file.write(audio.get_wav_data())
            print("Transcribing")
            global model
            initialize_model()
            audio = whisper.load_audio(MIC_OUTPUT_FILENAME)
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(model.device)
            options = whisper.DecodingOptions(task='transcribe',
                                              language='english', without_timestamps=True, fp16=False if model.device == 'cpu' else None)
            result = whisper.decode(model, mel, options)
            user_input = result.text
            global whisper_filter_list
            if user_input == '':
                return
            print('filtering')
            if user_input.strip().lower() in whisper_filter_list:
                print('Input filtered.')
                return

            chatbot.send_user_input(user_input)

def log_message(message_text):
    print(message_text)
    global logging_eventhandlers
    for eventhandler in logging_eventhandlers:
        eventhandler(message_text)

def get_user_choice():
    while True:
        choice = input("Choose an option (1 for voice, 2 for text): ")
        if choice in ['1', '2']:
            return choice
        else:
            print("Invalid choice. Please enter 1 or 2.")

# Entry point to start auto recording and listening
if __name__ == "__main__":
    choice = get_user_choice()
    if choice == '1':
        start_record_auto()  # Start recording and listening
        # Add a loop to continuously prompt for input (speech)
        while True:
            listen()
            time.sleep(2)  # Adjust sleep duration as needed
    elif choice == '2':
        # Add a loop to continuously prompt for input (text)
        while True:
            user_input = input("Enter text: ")
            if user_input.strip():
                handle_input(user_input)
            time.sleep(2)  # Adjust sleep duration as needed
    else:
        print("Invalid choice. Exiting.")
