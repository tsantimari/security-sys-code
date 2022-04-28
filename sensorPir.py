import RPi.GPIO  
from gpiozero import MotionSensor

pir = MotionSensor(17)

while True:
    pir.wait_for_motion()
    print("Motion Detected")
    pir.wait_for_no_motion()
