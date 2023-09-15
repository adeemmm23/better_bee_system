from datetime import date, datetime
import json
import requests
from gps import *
import time

location_changed_alert = {
    "name": "Changed Hive Location",
    "location": "location",
    "icon": "Icons.location_pin",
    "serious": True,
    "problem": "The location of your hive has been altered, which might have been caused by factors such as unauthorized movement or adverse weather conditions. Sudden changes in hive location can disrupt the foraging patterns and orientation of the bee colony, potentially endangering their survival.",
    "solution": "To address this situation, first, ensure that the hive has not been stolen or tampered with. If the change was due to bad weather or other environmental factors, carefully relocate the hive back to its original position during a time when weather conditions are favorable. Alternatively, use the hive's GPS coordinates and the map in the app to track its new location.",
    "date": "",
    "value": ""
}

gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)

location = {
    "lat": 0,
    "lon": 0,
}


def put_firebase(data):
    url = "https://better-buzz-default-rtdb.europe-west1.firebasedatabase.app/location/.json"
    headers = {"Content-Type": "application/json"}
    try:
        requests.put(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print("Failed to send Location data")


def post_alert(data, value):
    data["date"] = str(date.today().strftime("%B %d, %Y")) + \
        " at " + str(datetime.now().strftime("%H:%M"))
    data["value"] = "lat: " + str(value["lat"]) + ", lon: " + str(value["lon"])
    url = f"https://better-buzz-default-rtdb.europe-west1.firebasedatabase.app/alerts/.json"
    headers = {"Content-Type": "application/json"}
    try:
        requests.post(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print("Failed to send Location alert")


def get(gps):
    global location
    nx = gpsd.next()
    if nx['class'] == 'TPV':
        location["lat"] = getattr(nx, 'lat', "Unknown")
        location["lon"] = getattr(nx, 'lon', "Unknown")
        print(f'Location: lat {location["lat"]}, lon {location["lon"]}')


def main():
    global gpsd
    global location
    clock = 0
    alerted = False

    old_location = location

    while True:
        get(gpsd)
        put_firebase(location)

        if old_location != location and alerted == False:
            post_alert(location_changed_alert, location)
            old_location = location
            alerted = True

        if clock >= 60:
            alerted = False
            clock = 0
        else:
            clock += 1
            
        time.sleep(1)


if __name__ == "__main__":
    main()
