#Import required libraries
from gpiozero import MotionSensor, Button, LED
from picamera import PiCamera
from email.mime.multipart import MIMEMultipart
import email.mime.application
import smtplib
from subprocess import call 
import os
import sys
import time
from time import sleep
import datetime
import RPi.GPIO as GPIO

#Creating PIR Sensor, PiCamera, LED and Button
pir = MotionSensor(17) #pin where positive cable is connected
camera = PiCamera()
led = LED(21)
button = Button(23)
#Set trigger PIN for buzzer 18
triggerPIN = 18

#Set buzzer PIN to output
GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPIN,GPIO.OUT)
buzzer = GPIO.PWM(triggerPIN, 1000) #Set frequency to 1 Khz

#Set email addresses and the credentials of the sender
from_email_addr = 'raspberrymt87@gmail.com'
from_email_password = 'Sarakas1987!'
#Set the Email address of the receiver
to_email_addr = 'tsantiraki@gmail.com'

#Create Alarm State which by default is off.
Alarm_state = False

#The intrusion event control loop
while True:
      
   if button.is_pressed or GPIO.input(17): #If motion detect by sensor or button pressed
        Alarm_state = True #Changes the Alarm State to on
        print('Alarm ON')
        print("Motion Detected")
        
   #When motion detected by sensor or button pressed on
   if Alarm_state == True:
        led.on()
        #define PWM signal and start it on trigger PIN       
        buzzer.start(10) # Set dutycycle to 10
        sleep(1)

        #Setting camera’s resolution and rotation before starting video recording
        camera.resolution = (640,480)
        camera.rotation = 180
        #Recorded file will be saved as 'alert_video.h264'
        camera.start_recording('alert_video.h264')
        camera.wait_recording(7)
        camera.stop_recording()

        #Coverting video from .h264 to .mp4
        command = "MP4Box -add alert_video.h264 alert_video.mp4"
        call([command], shell=True)
        print("video converted")

        #Creating the Message
        msg = MIMEMultipart()
        msg[ 'Subject'] = 'INTRUDER ALERT..!!'
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr

        #Video file attachment to the email
        Captured = '/home/pi/alert_video.mp4' #The file from the specific directory
        fp = open(Captured,'rb') #Opening the file in binary mode
        att = email.mime.application.MIMEApplication(fp.read(),_subtype=".mp4")
        fp.close()
        att.add_header('Content-Disposition','attachment',filename='video' + datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S') + '.mp4')
        msg.attach(att)
        print("attach successful")

        #Removing .h264 file
        os.remove("/home/pi/alert_video.h264")

        #Renaming the recorded file
        os.rename('alert_video.mp4', datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S') + '.mp4')

        #Sending the Mail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email_addr, from_email_password)
        server.sendmail(from_email_addr, to_email_addr, msg.as_string())
        server.quit()
        print('Email sent')
        Alarm_state = False
        