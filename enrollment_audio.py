
import pyaudio
import wave
import uuid
import os
from time import sleep

AUDIO_DIR = os.path.join(os.getcwd(), 'enrollment_audios')
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 4
DEVICE_INDEX = pyaudio.PyAudio().get_default_input_device_info().get('index')

os.system(f"mkdir -p {os.path.join(os.getcwd(), AUDIO_DIR)} &")


while True:
    audio = pyaudio.PyAudio()

    wave_output_filepath = os.path.join(
        AUDIO_DIR, str(uuid.uuid4()) + ".wav")

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, input_device_index=DEVICE_INDEX,
                        frames_per_buffer=CHUNK)
    print("RECORDING STARTED")
    Recordframes = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    print("RECORDING STOPPED")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(wave_output_filepath, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()
    print("==================================================")
    sleep(1)
    
