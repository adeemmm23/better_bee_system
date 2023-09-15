import json
import time
import requests
from datetime import datetime


def put_firebase(data):
    url = "https://better-buzz-default-rtdb.europe-west1.firebasedatabase.app/active/.json"
    headers = {"Content-Type": "application/json"}
    try:
        requests.put(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print("Failed to send last active time")


def main():
    while True:
        current_datetime = datetime.now()
        formatted_time = {
            "year": current_datetime.strftime("%Y"),
            "month": current_datetime.strftime("%m"),
            "day": current_datetime.strftime("%d"),
            "hour": current_datetime.strftime("%H"),
            "minute": current_datetime.strftime("%M"),
            "second": current_datetime.strftime("%S")
        }
        put_firebase(formatted_time)
        print(f'Last active: {current_datetime.strftime("%H:%M:%S %d/%m/%Y")}')
        time.sleep(3600)


if __name__ == "__main__":
    main()
