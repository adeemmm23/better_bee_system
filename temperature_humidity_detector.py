from datetime import date, datetime
import json
import random
import requests
# import Adafruit_DHT
from time import sleep

high_temperature_alert = {
    "name": "High Temperature",
    "location": "temperature",
    "icon": "Icons.thermostat_outlined",
    "serious": True,
    "problem": "The temperature within your hive is too high. It is crucial to monitor and regulate the temperature to ensure the well-being of your bees. Be careful, high temperature can cause damage in the beehive structure.",
    "solution": "To address this issue, you should take immediate action to cool down the hive. Adequate ventilation and shading can help bring the temperature back to a safe range for your bees. Also allow carbon dioxide to escape.",
    "date": "",
    "value": ""
}

low_temperature_alert = {
    "name": "Low Temperature",
    "location": "temperature",
    "icon": "Icons.thermostat_outlined",
    "serious": True,
    "problem": "The temperature within your hive is too low. Maintaining an appropriate temperature is essential to safeguard the health and activity of your bees.",
    "solution": "To rectify this situation, you should take prompt measures to warm up the hive. Adding insulation and providing a heat source can help raise the temperature to a suitable range for your bees.",
    "date": "",
    "value": ""
}

high_humidity_alert = {
    "name": "High Humidity Level",
    "location": "humidity",
    "icon": "Icons.water_damage",
    "serious": True,
    "problem": "The humidity level within your hive is too high. Excess humidity can lead to mold growth and other issues that may affect your bees' health.",
    "solution": "To address this issue, you should improve hive ventilation and reduce moisture buildup. Ensure proper hive construction and consider using absorbent materials to regulate humidity.",
    "date": "",
    "value": ""
}

low_humidity_alert = {
    "name": "Low Humidity Level",
    "location": "humidity",
    "icon": "Icons.water_damage",
    "serious": False,
    "problem": "The humidity level within your hive is unusually low. Bees require a certain level of humidity for brood development and overall hive health.",
    "solution": "To rectify this situation, you should provide a water source near the hive and use misting techniques to increase humidity. Ensure that the hive has proper insulation to retain moisture.",
    "date": "",
    "value": ""
}


def put_firebase_temperature(data):
    url = "https://better-buzz-default-rtdb.europe-west1.firebasedatabase.app/temperature/.json"
    headers = {"Content-Type": "application/json"}
    try:
        requests.put(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print("Failed to send Temperature data")


def put_firebase_humidity(data):
    url = "https://better-buzz-default-rtdb.europe-west1.firebasedatabase.app/humidity/.json"
    headers = {"Content-Type": "application/json"}
    try:
        requests.put(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print("Failed to send Humidity data")


def post_alert(data, value):
    data["date"] = str(date.today().strftime("%B %d, %Y")) + \
        " at " + str(datetime.now().strftime("%H:%M"))
    data["value"] = value
    url = f"https://better-buzz-default-rtdb.europe-west1.firebasedatabase.app/alerts/.json"
    headers = {"Content-Type": "application/json"}
    try:
        requests.post(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print("Failed to send Temperature or Humidity alert")


# pin = 23
# sensor = Adafruit_DHT.DHT11
# humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        


def main():
    clock_temperature = 0
    alerted_temperature = False

    clock_humidity = 0
    alerted_humidity = False

    while True:
        temperature = random.randint(14, 16)
        humidity = random.randint(60, 65) * 1.0
        print(f"Temperature: {temperature} °C")
        print(f"Humidity: {humidity} %")
        sleep(1)

        put_firebase_temperature(temperature)
        put_firebase_humidity(humidity)

        if temperature > 37 and alerted_temperature == False:
            post_alert(high_temperature_alert, temperature)
            alerted_temperature = True

        if temperature < 33 and alerted_temperature == False:
            post_alert(low_temperature_alert, temperature)
            alerted_temperature = True

        if clock_temperature >= 400:
            alerted_temperature = False
            clock_temperature = 0
        else:
            clock_temperature += 1

        if humidity > 60 and alerted_humidity == False:
            post_alert(high_humidity_alert, humidity)
            alerted_humidity = True

        if humidity < 50 and alerted_humidity == False:
            post_alert(low_humidity_alert, humidity)
            alerted_humidity = True

        if clock_humidity >= 600:
            alerted_humidity = False
            clock_humidity = 0

        else:
            clock_humidity += 1


if __name__ == "__main__":
    main()
