#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==========================================================================
# BUILT-IN/GENERIC IMPORTS FOR MAIDS
#==========================================================================
import RPi.GPIO as GPIO
import time
import datetime as datetime
import smtplib
import ssl
import os
import http.client
import urllib
import vlc
import mysql.connector

#==========================================================================
# MODULES IMPORTED
#==========================================================================
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from subprocess import call
from mysql.connector import Error
from playsound import playsound

#==========================================================================
#************************ GLOBALS *****************************************
#==========================================================================
#
# MAIDS PROJECT-SPECIFIC GLOBALS ******************************************
#
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
__school__ = "Humber College"
__program__ = "Computer Engineering Technology"
__course__ = "CENG317"
__studentno__ = "N00674230"
__instructor__ = "Mr. Austin Tian"
__description__ = "MEIS ALARM INTRUSION DETECTION SYSTEM"
#
# MAIDS PROJECT PINOUT GLOBALS ********************************************
#
__SWITCH_PIN__ = 4
__GREEN_LED_PIN__ = 11
__RED_LED_PIN__ = 13
__MOTION_PIN__ = 29
__SOUND_PIN__ = 31
__BUZZER_PIN__ = 33
chan_list2 = (__RED_LED_PIN__,__GREEN_LED_PIN__,__BUZZER_PIN__)
#
# MAIDS PROJECT EMAIL/PUSH NOTIFICATION GLOBALS ***************************
#
__recipient__ = 'cfpm@live.ca'                      # recipient email
__sender__ = 'claudiomeis57@gmail.com'              # sender email
__subject__ = "MAIDS - INTRUSION DETECTION ALERT"  # email Subject
__msg_preamble__ = "INTRUSION DETECTED BY MAIDS!\n1234 BROOK ROAD, ETOBICOKE, ON. - LIVING ROOM ENTRY\n"
__port__ = 587                                      # port For starttls
__smtp_server__ = "smtp.gmail.com"
__username__ = "claudiomeis57@gmail.com"            # Setup username for login
__password__ = "Conor@2018"                         # Setup password for login
#
# MAIDS PROJECT SOUND ACTIVATION GLOBALS **********************************
#
__sounds__ = ( 'c:/s/leaveroom.mp3', 'c:/s/10.mp3', 'c:/s/9.mp3', 'c:/s/8.mp3', \
                'c:/s/7.mp3', 'c:/s/6.mp3', 'c:/s/5.mp3', 'c:/s/4.mp3', \
                'c:/s/3.mp3', 'c:/s/2.mp3', 'c:/s/1.mp3', 'c:/s/maids_activated.mp3' \
                'c:/s/s2.wav', 'c:/s/51267034.mp3')
__count__ = 11
#
#MySQL DATABASE GLOBALS ***************************************************
#
__address__ = "1234 Brook Road, Etobicoke, ON."
__location__ = "Room"
__reportingperson__ = "CONOR PATRICK JOSEPH MEIS"
__contactphone__ = "647-123-4567"
__contactemail__ = "cfpm@live.ca"
intrusiondate = datetime.datetime.now()

#==========================================================================
#************************ END OF GLOBALS **********************************
#==========================================================================

#==========================================================================
# MAIDS PYTHON SCRIPT DESCRIPTION
#==========================================================================
#
#   This script will set up the inputs/oputput pins for the Meis
#   Alarm Intrusion Detection System (MAIDS) and manipulated them
#   to provide a fully functional intrusion detection system based
#   on motion and sound sensors, warning lights and buzzer alarm.
#   multi-channel alerts are sent upon intrusion being registered
#   by sensors.

#==========================================================================
# MAIDS MIT LICENSE INFORMATION
#==========================================================================
#
# Copyright 2019 Claudio F. Meis - MAIDS PROJECT
#
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

#**************************************************************************
# START OF FUNCTIONS BLOCK
#**************************************************************************
# Function block contains the following functions:
# 1. set_up_gpio()           --> line 160
# 2. maids()                 --> line 184
# 3. notify()                --> line 253
# 4. alarm()                 --> line 275
# 5. alert()                 --> line 291
# 6. sound(sound)            --> line 302
# 7. motion(motion)          --> line 321
# 8. send_mail()             --> line 340
# 9. send_androidpush()      --> line 382
# 10. appendtodb()           --> line 403
# 11. intruderwarning()      --> line 424
# 12. siren()                --> line 437
# 13. activationwarning()    --> line 450
# 14. dbinsert()             --> line 466

#==========================================================================
# 1. set_up_gpio() --> SETUP GPIO NUMBERING SYSTEM AND I/O's
#==========================================================================
def set_up_gpio():

    GPIO.setmode(GPIO.BOARD)        # SETUP NUMBERING SYSTEM FOR GPIO
    GPIO.setwarnings(False)         # DISABLE WARNINGS

    # SETTING UP INPUT/OUTPUT PINS *******************************************
    #GPIO.setup(__SWITCH_PIN__, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #SWITCH - IN
    GPIO.setup(__MOTION_PIN__, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #MOTION SENSOR - PIR - IN
    GPIO.setup(__SOUND_PIN__, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #SOUND SENSOR - IN

    GPIO.Setup(chan_list2,(GPIO.OUT,GPIO.OUT,GPIO.OUT))      #RED/GREEN LED OUT & BUZZER OUT
    '''   
    GPIO.setup(__RED_LED_PIN__, GPIO.OUT)                           
    GPIO.setup(__GREEN_LED_PIN__, GPIO.OUT)   
    GPIO.setup(__BUZZER_PIN__, GPIO.OUT)         

'''
    GPIO.output(chan_list2,(GPIO.LOW,GPIO.LOW,GPIO.HIGH))            #RED/GREEN LED OFF - BUZZER OFF

#**************************************************************************

#==========================================================================
# 2. maids() --> WELCOME SCREEN FUNCTION FOR MAIDS
#==========================================================================
def maids():
    ''' MAIDS Function -- Displays MAIDS onscreen logo and project information.
    Parameters:
    :param none:
    Input Data:
    See MAIDS PROJECT SPECIFIC INFORMATION section
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
    print("      ==========================================================================================\n")
    print("      Project Name: " + __projectname__ + " - Description: " + __description__)
    print("      Author: " + __author__ + " - Stud. No: " + __studentno__ + " Email: " + __email__)
    print("      Date: " + __date__ + " - " + __copyright__)
    print("      License: " + __license__ + " - Version: " + __version__ + " - Maintainer: " + __maintainer__)
    print("      School: " + __school__ + " - Program: " + __program__)
    print("      Program: " + __program__)
    print("      Course: " + __course__ + " - Instructor: " + __instructor__)
    print("      ==========================================================================================\n")
    time.sleep(3)
#**************************************************************************

#==========================================================================
# 3. notify() --> UPDATE DATABASE/SEND EMAIL/SEND PUSH TO ANDROID PHONE FUNCTION
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
    send_email()
    #SENDING PUSH NOTIFICATION TO ANDROID PHONE
    print("Sending push notification to Android phone...")
    send_androidpush()
    time.sleep(1)
#**************************************************************************

#==========================================================================
# 4. alarm() --> SET LIGHT/SOUND ALARM FORMAT
#==========================================================================
def alarm():
    ''' MAIDS Function -- Sets LED flashing/sound pattern..
    Parameters:
    :param none:
    Input Data:
    none
    '''
    GPIO.output(chan_list2,(GPIO.HIGH,GPIO.LOW,GPIO.LOW))   #RED LED/BUZZER ON & GREEN LED OFF
    time.sleep(0.1)
    GPIO.output(chan_list2,(GPIO.LOW,GPIO.LOW,GPIO.HIGH))   #RED LED/GREEN LED/BUZZER OFF
    time.sleep(0.1)
#**************************************************************************

#==========================================================================
# 5. alert() --> SOUND SENSOR FUNCTION
#==========================================================================
def alert():
    for x in range(1, 6):
        alarm()
    intruderwarning()
    notify()
    siren()
    time.sleep(5)

#==========================================================================
# 6. sound(sound) --> SOUND SENSOR FUNCTION
#==========================================================================
def sound(sound):
    ''' MAIDS Function -- Detects sound.
    Parameters:
    :param none:
    Input Data:
    none
    '''
    GPIO.output(__GREEN_LED_PIN__,GPIO.HIGH)
    if GPIO.input(sound) == False:
        print("MAIDS - MAIDS ALERT - Sound Detected!")
        alert()
        GPIO.output(__GREEN_LED_PIN__, GPIO.HIGH)
    else:
        GPIO.output(__GREEN_LED_PIN__,GPIO.HIGH)
#**************************************************************************

#==========================================================================
# 7. motion(motion) --> MOTION SENSOR FUNCTION
#==========================================================================
def motion(motion):
    ''' MAIDS Function -- Detects motion.
    Parameters:
    :param none:
    Input Data:
    none
    '''
    GPIO.output(__GREEN_LED_PIN__,GPIO.HIGH)
    if GPIO.input(motion) == False:
        print("MAIDS ALERT - Motion Detected!")
        alert()
        GPIO.output(__GREEN_LED_PIN__, GPIO.HIGH)
    else:
        GPIO.output(__GREEN_LED_PIN__,GPIO.HIGH)
#**************************************************************************

#==========================================================================
# 8. send_email() --> SENDING ALERT WITH PICTURE TO RECIPIENT
#==========================================================================
def send_email():
    ''' MAIDS Function -- Sends picture of intruder to email address.
    Parameters:
    :param none:
    Input Data:
    none
    '''
    os.system("fswebcam -r 1280x720 --title 'MAIDS INTRUSION ALERT' --subtitle '1234 BROOK ROAD, ETOBICOKE, ON.' --timestamp '%Y-%m-%d %H:%M (%Z)' --info 'LIVING ROOM ENTRY' --jpeg -1 --save /home/pi/webcam/image.jpg")
    recipient = __recipient__                           # recipient email
    sender = __sender__                                 # sender email
    subject = __subject__                               # email Subject
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.preamble = __msg_preamble__
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("/home/pi/webcam/image.jpg", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="/home/pi/webcam/image.jpg"')    # File/format name
    msg.attach(part)

    try:
       # INFORMATION FOR SMTP SERVER
       port = __port__                                  # port For starttls
       smtp_server = __smtp_server__                    # server address
       s = smtplib.SMTP(smtp_server,port)               # Setup SMTP server for Gmail
       s.starttls()
       # GMAIL LOGIN INFORMATION
       username=__username__                            # Setup username for login
       password=__password__                            # Setup password for login
       s.login(username,password)                       # gmail.com login with username/password
       # SENDING EMAIL TO RECIPIENT
       s.sendmail(sender, recipient, msg.as_string())    # send email
       s.quit()
    except:
        print ("Error: Unable to send email")            # Exception
#**************************************************************************

#==========================================================================
# 9. send_androidpush() --> SETUP ANDROID PUSH NOTIFICATION INFORMATION WITH PUSHOVER SERVICE
#==========================================================================
def send_androidpush():
    ''' MAIDS Function --Sends push notification to Android phone.
    Parameters:
    :param none:
    Input Data:
    token id: "ahztmyszcui2w1svm21bbo813yie44"
    user id: "ujt5f9osjotntdhapm64ab4dg8jt2m"
    '''
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": "ahztmyszcui2w1svm21bbo813yie44",
        "user": "ujt5f9osjotntdhapm64ab4dg8jt2m",
        "message": "INTRUSION DETECTED BY MAIDS - ALERT SENT! - REPORTING PERSON: JOHN SMITH CONTACT: 647-123-4567 EMAIL: cfpm@live.ca - INTRUSION ADDRESS: 1234 BROOK ROAD, ETOBICOKE, ON. LOCATION: LIVING ROOM",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
#**************************************************************************

#==========================================================================
# 10. appendtodb() --> APPEND INTRUSION DATA TO TEXT and MySQL DATABASE
#==========================================================================
def appendtodb():
    ''' MAIDS Function -- Updates text database.
    Parameters:
    :param none:
    Input Data:
    none
    '''
    # APPENDING INTRUSION INFORMATION TO DATABASE
    filename = "/home/pi/maids_alarm_record.txt"                #assign text file to update
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S") #create timestamp
    f= open(filename,"a+")                                      #open file to append
    f.write("\n")                                               #write info to file
    f.write(f"INTRUSION DETECTED -- ALARM ACTIVATED! EMAIL WITH PHOTO SENT! DATE/TIME: {now}\n")
    f.write("REPORTING PERSON: JOHN SMITH CONTACT: 647-123-4567 EMAIL: cfpm@live.ca\n")
    f.write("INTRUSION ADDRESS: 1234 BROOK ROAD, ETOBICOKE, ON. LOCATION: LIVING ROOM\n\n")
    f.close()                                                   #close file

    dbinsert(__address__, __location__, intrusiondate, __reportingperson__, __contactphone__,__contactemail__)
#**************************************************************************

#==========================================================================
# 11. intruderwarning() -- > PLAY INTRUDER WARNING MESSAGE
#==========================================================================
def intruderwarning():
    ''' MAIDS Function -- Plays warning message to intruder through vlc.
    Parameters:
    :param none:
    Input Data: /home/pi/mp3/51267034.mp3 file
    '''
    playsound('c:/s/51267034.mp3')
    time.sleep(0.20)
#**************************************************************************

#==========================================================================
# 12. siren() -- > PLAY SIREN ALARM SOUND
#==========================================================================
def siren():
    ''' MAIDS Function -- Plays a siren alarm sound through vlc.
    Parameters:
    :param none:
    Input Data: /home/pi/mp3/51267034.mp3 file
    '''
    playsound('c:/s/s2.wav')
    time.sleep(0.20)
#**************************************************************************

#==========================================================================
# 13. activationwarning() -- > PLAY SIREN ALARM SOUND
#==========================================================================
def activationwarning():
    ''' MAIDS Function -- Plays a siren alarm sound through playsound module.
    Parameters:
    :param none:
    Input Data: __sounds__ list
    :Needed: pip install playsound
    '''
    for index in range(len(__sounds__)):
        print(f"{__count__ - index}")
        playsound(__sounds__[index])
        time.sleep(0.20)
#**************************************************************************

#==========================================================================
# 14. dbinsert() -- > INSERT INTRUSION INFORMATION INTO MYSQL DATABASE
#==========================================================================
def dbinsert(address, location, intrusiondate, reportingperson, contactphone, contactemail):
    ''' MAIDS Function -- inserts intrusion particulars to MySQl database.
    Parameters:
    :param address:
    :param location:
    :param intrusiondate:
    :param reportingperson:
    :param contactphone:
    :param contactemail:
    :Input Data: __sounds__ list
    '''
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='maids1',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO maidsintrusion (address, location, intrusiondate, reportingperson, contactphone, contactemail)  \
                                VALUES (%s, %s, %s, %s, %s, %s) """
        a = (address, location, intrusiondate, reportingperson, contactphone, contactemail)
        cursor.execute(mySql_insert_query, a)
        connection.commit()
        print("Record inserted successfully into Laptop table")
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#**************************************************************************
# END OF FUNCTIONS SECTION
#**************************************************************************

#==========================================================================
# STARTTING MAIN SCRIPT
#==========================================================================

set_up_gpio()                                                       #Setup GPIO Information
maids()                                                             #Display MAIDS logo/project information
print("MAIDS Surveillance Mode - Arming...")
activationwarning()                                                 #warning to vacate the room
print("MAIDS Surveillance Mode - Armed and Active...\n")
GPIO.add_event_detect(__SOUND_PIN__, GPIO.BOTH, bouncetime=200)     # Sound sensor: Detect when pin goes HIGH or LOW
GPIO.add_event_callback(__SOUND_PIN__, sound)                       # assign function to PIN & run it
GPIO.add_event_detect(__MOTION_PIN__, GPIO.BOTH, bouncetime=200)    # Motion sensor: Detect when pin goes HIGH or LOW
GPIO.add_event_callback(__MOTION_PIN__, motion)                     # assign function to PIN, and run it

try:
    while True:             # infinite loop
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()          #cleanup

GPIO.cleanup()              #cleanup