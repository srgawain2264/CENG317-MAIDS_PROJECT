#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==========================================================================
# MAIDS PYTHON SCRIPT INFORMATION
#==========================================================================
__author__ = "Claudio F. Meis"
__projectname__ = "MAIDS PROJECT"
__date__ = "October 12, 2019"
__copyright__ = "Copyright (c) 2019, Claudio F. Meis, The MAIDS project"
__credits__ = ["Claudio F. Meis","Conor Meis"]
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Claudio F. Meis"
__email__ = "cfpm@live.ca,claudiomeis57@gmail.com"
__status__ = "Dev"
__school__ = "Humber Institute of Technology and Advanced Learning"
__program__ = "Computer Engineering Technology"
__course__ = "CENG317"
__studentno__ = "N00674230"
__instructor__ = "Mr. Austin Tian"
__teammates__ = ['none']
__description__ = "MEIS ALARM INTRUSION DETECTION SYSTEM"
#==========================================================================

#==========================================================================
# MAIDS PYTHON SCRIPT DESCRIPTION
#==========================================================================
#
#   This script will set up the inputs/oputput pins for the Meis
#   Alarm Intrusion Detection System (MAIDS) and manipulated them
#   to provide a fully functional intrusion detection system based
#   on motion and sound sensors, warning lights and buzzer alarm.
#   Email notifications with pictures and Android Push Notifications
#   are sent upon intrusion being registered by sensors.


#==========================================================================
# MAIDS MIT LICENSE INFORMATION
#==========================================================================

# Copyright 2019 Claudio F. Meis

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#==========================================================================
# LIBRARY IMPORTED FOR MAIDS
#==========================================================================
import RPi.GPIO as GPIO
#==========================================================================
# BUILT-IN/GENERIC IMPORTS FOR MAIDS
#==========================================================================
import time
import datetime
import smtplib
import ssl
import os
import http.client
import urllib
import vlc
#==========================================================================
# MODULES IMPORTED
#==========================================================================
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders
from subprocess import call
from pygame.locals import*
#==========================================================================
# SETUP NUMBERING SYSTEM FOR GPIO
#==========================================================================
GPIO.setmode(GPIO.BOARD)
#==========================================================================
#DISABLE WARNINGS
#==========================================================================
GPIO.setwarnings(False)
#==========================================================================
# SETTING UP PIN NUMBERS TO BE USED - GLOBALS
#==========================================================================
#SWITCH_PIN = 4      #GPIO4 - PIN 7 IN BOARD - IN
MOTION_PIN = 29    #GPIO5 - PIN 29 IN BOARD - IN
SOUND_PIN = 31      #GPIO6 - PIN 31 IN BOARD – IN
BUZZER_PIN = 33     #GPIO13 - PIN 33 IN BOARD - OUT
RED_LED_PIN = 11    #GPIO27 - PIN 13 IN BOARD - OUT
GREEN_LED_PIN = 13  #GPIO22 - PIN 15 IN BOARD – OUT
#==========================================================================
# SETTING UP INPUT/OUTPUT PINS
#==========================================================================
#GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #SWITCH - IN
GPIO.setup(MOTION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #MOTION SENSOR - PIR - IN
GPIO.setup(SOUND_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #SOUND SENSOR - IN
GPIO.setup(BUZZER_PIN, GPIO.OUT)                            #BUZZER - OUT
GPIO.setup(RED_LED_PIN, GPIO.OUT)                           #RED LED - OUT
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)                         #GREEN LED - OUT
#==========================================================================
# SETTING UP ALL INPUTS/OUTPUTS 
#==========================================================================
GPIO.output(BUZZER_PIN,GPIO.HIGH)
GPIO.output(GREEN_LED_PIN,GPIO.LOW)
GPIO.output(RED_LED_PIN,GPIO.LOW)
#==========================================================================
# WELCOME SCREEN FUNCTION FOR MAIDS
#==========================================================================
def maids():
    ''' MAIDS Function -- Displays MAIDS onscreen logo and project information.

    Parameters:
    :param none:

    Input Data:
    none

    ''' 
    os.system("clear")
    print("                            \\\\\\\//// ")
    print("                       \\//\/\\\\\\\/// ")
    print("                     \\\`      \\\\\\///")
    print("                    \\       ||\      \ ")
    print("                    \  \\   //     _\  `\ ")
    print("                   /  /. \  \\    /O.    `\,")
    print("                  //  |__\\ //\         . __\ ")
    print("                /`           //\\      , .\ / ")
    print("               \\\\          //\        ___|")
    print("              ////\\            \\     `   \ ")
    print("           //////////\\\\       //__       |")
    print("           |`  \\\//////\\        \_ \______|")
    print("          |     \\\\//\\/////\\\   \ ")
    print("         ./      \\\\////////\\     |\ ")
    print("         |        \\\\////\\//\\\\\\\\ ")
    print("         |          \\\///      \\\\\\ ")
    print("         |          \\\//         \// ")
    print("         |            \/        \ |")
    print("         |             `         \|")
    print("         | |                      \                       / ")
    print("          | |           \           \                     // ")
    print("          | |                        \                   //// ")
    print("          | |             .          `|                 ///// ")
    print("          | |                         `\                \\//// ")
    print("           \`|                          `|              \\||/ ")
    print("            | |             \            `|  ,--.         \ \,")
    print("            |  \                          |./    `\        | |")
    print("             |  |                                 |        | |")
    print("             |___|            .                   |        | |")
    print("             /   |                                |        | |")
    print("             |    |                               ;        | |")
    print("             |                                    |        | |")
    print("           __|                                   /`       /` ;")
    print("          /   \                          ,      ; \     ,` ,/ ")
    print("          \____\              \       \,/__________|__.' ,`")
    print(" ")
    print("      MMM  MM  MMM   AAAAAAAA   IIIIIIII   DDDDDDD    SSSSSSSS")
    print("      MMMM MM MMMM   AAAAAAAA     IIII     DDDDDDD    SSSSSSSS")
    print("      MMMM MM MMMM   AAA  AAA     IIII     DDD  DDD   SSS     ")
    print("      MMMM MM MMMM   AAA  AAA     IIII     DDD  DDD   SSS     ")
    print("      MMMMMMMMMMMM   AAAAAAAA     IIII     DDD  DDD   SSSSSSSS")
    print("      MMM MMMM MMM   AAAAAAAA     IIII     DDD  DDD        SSS")
    print("      MMM  MM  MMM   AAA  AAA     IIII     DDD  DDD        SSS")
    print("      MMM  MM  MMM   AAA  AAA     IIII     DDDDDDD    SSSSSSSS")
    print("      MMM  MM  MMM   AAA  AAA   IIIIIIII   DDDDDDD    SSSSSSSS")
    print(" ")
    print("      ================================================================================\n")
    print("      Project Name: " + __projectname__ + " - Description: " + __description__)
    print("      Author: " + __author__ + " - Stud. No: " + __studentno__)
    print("      Date: " + __date__ + " - " + __copyright__)
    print("      License: " + __license__ + " - Version: " + __version__ + " - Maintainer: " + __maintainer__)
    print("      School: " + __school__ + " - Program: " + __program__)
    print("      Program: " + __program__)
    print("      Course: " + __course__ + " - Instructor: " + __instructor__)
    print("      Contact Email: " + __email__)
    print("      ================================================================================\n")
    time.sleep(3)
#==========================================================================
# UPDATE DATABASE/SEND EMAIL/SEND PUSH TO ANDROID PHONE FUNCTION
#==========================================================================
def notify():
    ''' MAIDS Function -- Appends text database/send email/sends android push notification.

    Parameters:
    :param none:

    Input Data:
    none

    ''' 
    #APPEND DATABASE/SENDG EMAIL WITH PICTURE/SEND ANDROID PUSH NOTIFICATION - INTRUSION ALERT
    print("Appending Intrusion Alert to Database...")
    appendtodb()
    #TAKING PIC AND SENDING EMAIL
    print("Sending Intrusion Alert to email...")
    send_picture_to_email()
    #SENDING PUSH NOTIFICATION TO ANDROID PHONE
    print("Sending push notification to Android phone...")
    send_android_pushnot()
    time.sleep(1)
#==========================================================================
# SET LIGHT/SOUND ALARM FORMAT
#==========================================================================
def alarm():
    ''' MAIDS Function -- Sets LED flashing/sound pattern..

    Parameters:
    :param none:

    Input Data:
    none

    '''     
    GPIO.output(RED_LED_PIN,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(RED_LED_PIN,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN,GPIO.HIGH)
#==========================================================================
# SOUND SENSOR FUNCTION  
#==========================================================================
def sound(sound):
    ''' MAIDS Function -- Detects sound.

    Parameters:
    :param none:

    Input Data:
    none

    '''    
    GPIO.output(GREEN_LED_PIN,GPIO.HIGH)
    if GPIO.input(sound) == False:
        print("MAIDS - Sound Detected!")
        for x in range(1,5):
            alarm()
        intruderwarning()
        notify()
    else:
        GPIO.output(GREEN_LED_PIN,GPIO.HIGH)
#==========================================================================
# MOTION SENSOR FUNCTION  
#==========================================================================
def motion(motion):
    ''' MAIDS Function -- Detects motion.

    Parameters:
    :param none:

    Input Data:
    none

    '''
    GPIO.output(GREEN_LED_PIN,GPIO.HIGH)
    if GPIO.input(motion) == False:
        print("MAIDS - Motion Detected!")
        for x in range(1,5):
            alarm()
        intruderwarning()
        notify()
    else:
        GPIO.output(GREEN_LED_PIN,GPIO.HIGH)
#==========================================================================
# SENDING ALERT WITH PICTURE TO RECIPIENT    
#==========================================================================
def send_picture_to_email():
    ''' MAIDS Function -- Sends picture of intruder to email address.

    Parameters:
    :param none:

    Input Data:
    none

    '''
    #now = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    #image = now+".jpg"
    os.system("fswebcam -r 1280x720 --title 'MAIDS INTRUSION ALERT' --subtitle '1234 BROOK ROAD, ETOBICOKE, ON.' --timestamp '%Y-%m-%d %H:%M (%Z)' --info 'LIVING ROOM ENTRY' --jpeg -1 --save /home/pi/webcam/image.jpg")
    #call(["fswebcam", "/home/pi/webcam/"+now+".jpg"])  # call program fswebcam to take a picture
    recipient = 'cfpm@live.ca'                      # recipient email
    sender = 'claudiomeis57@gmail.com'                  # sender email
    subject = "MAIDS - INTRUSION DETECTION ALERT"       # email Subject
    msg = MIMEMultipart()
    msg['Subject'] = subject  
    msg['From'] = sender 
    msg['To'] = recipient  
    msg.preamble = "INTRUSION DETECTED BY MAIDS!\n1234 BROOK ROAD, ETOBICOKE, ON. - LIVING ROOM ENTRY\n"   
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open("/home/pi/webcam/image.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="/home/pi/webcam/image.jpg"')    # File/format name
    msg.attach(part)
        
    try:  
       # INFORMATION FOR SMTP SERVER
       port = 587                       # port For starttls
       smtp_server = "smtp.gmail.com"               # server address
       s = smtplib.SMTP(smtp_server,port)           # Setup SMTP server for Gmail
       s.starttls()  

       # GMAIL LOGIN INFORMATION
       username="claudiomeis57@gmail.com"               # Setup username for login
       password="Conor@2018"                            # Setup password for login
       s.login(username,password)                       # gmail.com login with username/password

       # SENDING EMAIL TO RECIPIENT
       s.sendmail(sender, recipient, msg.as_string())       # send email
       s.quit()  

    # SETTING UP EXCEPTIONS - ERRORS
    except SMTPException as error:  
        print ("SMTP Error!")                           # Exception
    except:  
        print ("Error: Unable to send email")           # Exception
#==========================================================================
# SETUP ANDROID PUSH NOTIFICATION INFORMATION WITH PUSHOVER SERVICE
#==========================================================================
def send_android_pushnot():
    ''' MAIDS Function --Sends push notification to Android phone.

    Parameters:
    :param none:

    Input Data:
    none

    '''
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": "ahztmyszcui2w1svm21bbo813yie44",
        "user": "ujt5f9osjotntdhapm64ab4dg8jt2m",
        "message": "INTRUSION DETECTED BY MAIDS - EMAIL/PICTURE SENT! - REPORTING PERSON: JOHN SMITH CONTACT: 647-123-4567 EMAIL: cfpm@live.ca - INTRUSION ADDRESS: 1234 BROOK ROAD, ETOBICOKE, ONTARIO LOCATION: LIVING ROOM",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
#==========================================================================
# APPEND INTRUSION DATA TO DATABASE
#==========================================================================
def appendtodb():
    ''' MAIDS Function -- Updates text database.

    Parameters:
    :param none:

    Input Data:
    none

    '''
    # APPENDING INTRUSION INFORMATION TO DATABASE
    filename = "/home/pi/maids_alarm_record.txt"
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    f= open(filename,"a+")
    f.write("\n")
    f.write(f"INTRUSION DETECTED -- ALARM ACTIVATED! EMAIL WITH PHOTO SENT! DATE/TIME: {now}\n")
    f.write("REPORTING PERSON: JOHN SMITH CONTACT: 647-123-4567 EMAIL: cfpm@live.ca\n")
    f.write("INTRUSION ADDRESS: 1234 BROOK ROAD, ETOBICOKE, ON. LOCATION: LIVING ROOM\n\n")
    f.close()
#==========================================================================
# PLAY INTRUDER WARNING
#==========================================================================
def intruderwarning():
    ''' MAIDS Function -- Plays warning to intruder.

    Parameters:
    :param none:

    Input Data:
    none
    '''
    player = vlc.MediaPlayer("/home/pi/mp3/51267034.mp3")
    player.play()
#==========================================================================
# STARTTING MAIN SCRIPT
#==========================================================================
#Display MAIDS logo and project information
maids()
#Sound sensor detecting sound
GPIO.add_event_detect(SOUND_PIN, GPIO.BOTH, bouncetime=200)   # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(SOUND_PIN, sound)                     # assign function to GPIO PIN, Run function on change
#Motion sensor detecting movement
GPIO.add_event_detect(MOTION_PIN, GPIO.BOTH, bouncetime=200)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(MOTION_PIN, motion)                   # assign function to GPIO PIN, Run function on change

try:
    # infinite loop
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()          #cleanup
        
GPIO.cleanup()              #cleanup