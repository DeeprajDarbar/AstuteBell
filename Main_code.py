import face_recognition
import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
from datetime import datetime
import shutil
import os
import smail
from pushbullet.pushbullet import PushBullet
import picamera
print("all libraries loaded")
gmail_user = "macwanfrank1996@gmail.com" #Sender email address
gmail_pwd = ".1.2.3.7.8.9" #Sender email password
to = "macwanfrank96@gmail.com" #Receiver email address
subject = "Security Breach" #Email subject
text = "There is some activity at your door. See the attached picture." #text you want to send in email
known_image = face_recognition.load_image_file("/home/pi/Desktop/known/frank.jpg")
sensor = 4 #pin connection of pir sensor to raspberry pi 

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)







def recog():
    visitor=0
    known_encoding = face_recognition.face_encodings(known_image)[0]
    print('known image encodings done')
    previous_state = False
    current_state = False
    while True:
            
        previous_state=current_state
        current_state=GPIO.input(sensor)
        if(current_state != previous_state):
            if(current_state): new_state="HIGH"
            else: new_state="LOW"
            print("GPIO pin %s is %s" % (sensor,new_state))
            if(current_state):
                print("A photo will be taken in 3 seconds")
                time.sleep(3)
                with picamera.PiCamera() as camera:
                    camera.resolution = (340, 220)
                    time.sleep(2)
                    camera.capture('unknown.jpg')
                unknown_image = face_recognition.load_image_file("/home/pi/Desktop/unknown.jpg")
                face_locations = face_recognition.face_locations(unknown_image)
                if(len(face_locations) == 0):
                    print("no face detected")
                    os.remove('unknown.jpg')
                    continue
                    
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                print("encodings calculated")
                results = face_recognition.compare_faces([known_encoding], unknown_encoding)
                print(results)
                if results == [True]:
                    GPIO.setup(14, GPIO.OUT)
                    print("person recognised,frank")
                    p = PushBullet("o.a441em4dWH3fzGm1mcURidwfuJ1gG4Jn") #secret key of pushbullet API
                    devices = p.getDevices()
                    p.pushNote(devices[0]["iden"], 'Frank is at the door', 'open the door')
                    os.remove("unknown.jpg")
                    print("message sent")
                    GPIO.cleanup()
                    break
                else:
                    while(os.path.exists("/home/pi/Desktop/known/"+str(visitor)+".jpg")):
                        visitor=visitor+1
                    os.rename("/home/pi/Desktop/unknown.jpg","/home/pi/Desktop/"+str(visitor)+".jpg")
                    shutil.move("/home/pi/Desktop/"+str(visitor)+".jpg","/home/pi/Desktop/known")
                    print("unknown person")
                    picname = str(visitor) + ".jpg"
                    visitor=visitor+1
                        #cv2.imwrite(picname,frame) 
                    p = PushBullet("o.a441em4dWH3fzGm1mcURidwfuJ1gG4Jn") #secret key of pushbullet API
                    devices = p.getDevices()
                    p.pushFile(devices[0]["iden"], picname, "unknown person", open("/home/pi/Desktop/known/"+picname, "rb"))

                    print("Sending email")
                    attach=picname #attachments to send with email
                    smail.send_mail(attach)
                    print("email sent")           
                    break
        

