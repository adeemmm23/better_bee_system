# Better Bee Monitoring System

Better Bee is a monitoring system for beehives that tracks location, noise levels, temperature, humidity, and activity.

## Features

- Location detection and alerts.
- Noise level monitoring and alerts.
- Temperature and humidity monitoring with alerts.
- Hive activity monitoring.

## Dependencies

- Python 3.x
- Various Python packages (specified in each individual script)

## Usage

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the monitoring system by executing `python start_monitoring.py`.

The monitoring system will start threads for location detection, noise monitoring, temperature/humidity monitoring, and hive activity monitoring.

## Scripts

- `location_detector.py`: Monitors hive location and sends alerts if location changes.
- `sound_detector.py`: Monitors noise levels inside the hive and sends alerts for high or low noise.
- `temperature_humidity_detector.py`: Monitors temperature and humidity inside the hive, sending alerts for abnormal levels.
- `active.py`: Monitors hive activity and sends alerts based on predefined thresholds.
