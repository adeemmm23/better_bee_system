from threading import Thread

import location_detector
import sound_detector
import temperature_humidity_detector
import active

print("Starting Better Bee...")
Thread(target = sound_detector.main).start()
Thread(target = location_detector.main).start()
Thread(target = temperature_humidity_detector.main).start()
Thread(target = active.main).start()