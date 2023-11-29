import os
import time
import torch
import torchaudio
import soundfile
import sounddevice
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from nltk import sent_tokenize
import threading
from queue import Queue  # Import Queue

def initialize_tts_model():
    config = XttsConfig()
    config.load_json("Path-to-config.jason")
    model = Xtts.init_from_config(config)
    model.load_checkpoint(config, checkpoint_dir="Path-to-xtts-model", use_deepspeed=True)
    model.cuda()
    return model

def compute_speaker_latents(model):
    audio_path = "path-to-example-of-voice-to-clone"
    gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=[audio_path])
    return gpt_cond_latent, speaker_embedding

def tts_and_play_audio(text, model, gpt_cond_latent, speaker_embedding):
    print(f"Text received: {text}")

    if not isinstance(model, Xtts):
        raise ValueError("The provided model is not an instance of Xtts.")

    # Split text into sentences
    sentences = sent_tokenize(text)

    # Create a queue to store audio chunks
    audio_queue = Queue()

    # Create a thread for playing audio
    play_thread = threading.Thread(target=play_audio_from_queue, args=(audio_queue,))
    play_thread.start()

    for sentence in sentences:
        print(f"Processing sentence: {sentence}")

        # Generate audio chunks and put them into the queue
        chunks = model.inference_stream(
            sentence,
            "en",
            gpt_cond_latent,
            speaker_embedding
        )

        for chunk in chunks:
            audio_queue.put(chunk)

        # Introduce a delay between sentences
        time.sleep(0.4)

    # Signal the play thread to stop
    audio_queue.put(None)
    play_thread.join()

def play_audio_from_queue(audio_queue):
    temp_wav_path = "temp_audio.wav"
    while True:
        # Get the next audio chunk from the queue
        chunk = audio_queue.get()

        # Check if it's the signal to stop
        if chunk is None:
            break

        # Save the audio to a temporary file
        soundfile.write(temp_wav_path, chunk.squeeze().cpu().numpy(), 24000, format='WAV', subtype='PCM_16')

        # Play the audio using soundfile and sounddevice with blocking=True
        data, sr = soundfile.read(temp_wav_path, dtype='int16')
        sounddevice.play(data, sr, blocking=True)

    # Remove the temporary file
    os.remove(temp_wav_path)

if __name__ == '__main__':
    user_input = input("Enter the text for Coqui TTS: ")

    tts_model = initialize_tts_model()
    gpt_cond_latent, speaker_embedding = compute_speaker_latents(tts_model)

    tts_and_play_audio(user_input, tts_model, gpt_cond_latent, speaker_embedding)

