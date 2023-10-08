import pyaudio
import wave
import keyboard
import os
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
FILE_PREFIX = "output"
file_num = 1

audio = pyaudio.PyAudio()

def list_input_devices():
    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    devices = []
    for i in range(0, numdevices):
        if audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
            devices.append((i, audio.get_device_info_by_host_api_device_index(0, i).get('name')))
    return devices

def get_next_filename():
    global file_num
    while os.path.exists(f"{FILE_PREFIX}{file_num}.wav"):
        file_num += 1
    return f"{FILE_PREFIX}{file_num}.wav"

devices = list_input_devices()
print("Available input devices:")
for index, device in devices:
    print(f"{index}: {device}")

while True:
    try:
        selected_device = int(input("Select the device number you want to use for recording: "))
        if any(device[0] == selected_device for device in devices):
            break
        else:
            print("Invalid choice. Please select a valid device number.")
    except ValueError:
        print("Please enter a valid number.")

print("\nPress spacebar to start recording...")
print("Press 'esc' to exit the application...")

while True:
    if keyboard.is_pressed('esc'):
        print("Exiting...")
        break
    if keyboard.is_pressed('space'):
        time.sleep(0.2)  # Introduce a delay
        frames = []
        print("Recording...")
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True, input_device_index=selected_device,
                            frames_per_buffer=CHUNK)

        while not keyboard.is_pressed('space') and not keyboard.is_pressed('esc'):
            data = stream.read(CHUNK)
            frames.append(data)

        if keyboard.is_pressed('esc'):
            stream.stop_stream()
            stream.close()
            print("Exiting...")
            break
        
        print("Recording finished...")
        stream.stop_stream()
        stream.close()

        WAVE_OUTPUT_FILENAME = get_next_filename()
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        print(f"File saved as {WAVE_OUTPUT_FILENAME}!")

        print("Press spacebar to start recording again...")

audio.terminate()
