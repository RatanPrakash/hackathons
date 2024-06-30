from djitellopy import Tello
import time

# Connect to Tello drone
tello = Tello()
tello.connect()

# Take off
tello.takeoff()

# Wait for 10 seconds
time.sleep(10)

# Land
tello.land()

# Disconnect from Tello drone
tello.end()
