from picamera import PiCamera
from time import sleep
import datetime as dt
camera = PiCamera()
camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
t = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
camera.resolution = (640, 480)
camera.vflip = True
camera.start_preview(alpha=200)

camera.start_recording('/home/pi/Videos/%s.h264' % t)
sleep(5)
camera.stop_recording()
camera.stop_preview()
