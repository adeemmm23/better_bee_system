import json
import requests
from datetime import datetime, date
import sounddevice as sd
import numpy as np

high_noise_alert = {
    "name": "High Noise Level",
    "location": "noise",
    "icon": "Icons.volume_up_outlined",
    "serious": True,
    "problem": "The noise level inside your hive appears to be unusually high. Elevated noise levels within the hive can indicate issues with bee behavior, communication, or potential overcrowding.",
    "solution": "To address this situation, first, carefully inspect the hive's interior. Check for signs of overcrowding, such as limited space for brood and food storage. Evaluate the queen's reproduction rate and overall hive health. If necessary, provide additional space or consider splitting the colony if it's too large and give a good amount of sunlight, warmth, and shade. Place you hive in a planting and flowering area.",
    "date": "",
    "value": ""
}

low_noise_alert = {
    "name": "Low Noise Level",
    "location": "noise",
    "icon": "Icons.volume_up_outlined",
    "serious": False,
    "problem": "The noise level around your hive is unusually low, which could potentially be attributed to a malfunction in the bee noise tracking device's microphone. Bees rely on noise for communication and navigation, and a lack of noise may falsely indicate an issue.",
    "solution": "To investigate this further, check the bee noise tracking device's microphone for any signs of damage or malfunction. Ensure it is properly positioned to accurately capture bee activity noise. Additionally, consider testing the device in a controlled environment to verify its functionality.",
    "date": "",
    "value": ""
}


def put_firebase(data):
    url = "https://better-buzz-default-rtdb.europe-west1.firebasedatabase.app/noise/.json"
    headers = {"Content-Type": "application/json"}
    try:
        requests.put(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print("Failed to send Noise data")


def post_alert(data, value):
    data["date"] = str(date.today().strftime("%B %d, %Y")) + \
        " at " + str(datetime.now().strftime("%H:%M"))
    data["value"] = value
    url = f"https://better-buzz-default-rtdb.europe-west1.firebasedatabase.app/alerts/.json"
    headers = {"Content-Type": "application/json"}
    try:
        requests.post(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print("Failed to send Noise alert")


def calculate_dominant_frequency(audio_data, sample_rate):
    n = len(audio_data)
    frequencies = np.fft.fftfreq(n, d=1/sample_rate)
    magnitude = np.abs(np.fft.fft(audio_data))
    dominant_frequency = frequencies[np.argmax(magnitude)]
    return dominant_frequency


def main():
    clock = 0
    alerted = False

    duration = 1
    sample_rate = 44100

    while True:
        audio_data = sd.rec(int(duration * sample_rate),
                            samplerate=sample_rate, channels=1)
        sd.wait()

        dominant_frequency_hz = abs(calculate_dominant_frequency(
            audio_data[:, 0], sample_rate))

        print(f"Noise: {dominant_frequency_hz:.2f} Hz")
        put_firebase(dominant_frequency_hz)

        if dominant_frequency_hz > 500 and alerted == False:
            post_alert(high_noise_alert, dominant_frequency_hz)
            alerted = True

        if dominant_frequency_hz < 5 and alerted == False:
            post_alert(low_noise_alert, dominant_frequency_hz)
            alerted = True

        if clock >= 600:
            alerted = False
            clock = 0
        else:
            clock += 1


if __name__ == "__main__":
    main()
