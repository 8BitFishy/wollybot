from gpiozero import LED
import os
import shutil
import subprocess
import sys
from time import sleep, ctime
led = LED(17)
from os import execv
#from pygit2 import clone_repository


def on():
    led.on()
    sleep(1)
    led.off()
    print(ctime() + " - Action - Turning computer on")
    return

def off():
    led.off()
    print(ctime() + " - Action - Turning computer off")
    return

def hold(duration, Octavius_Receiver):
    Octavius_Receiver.send_message("Holding...")
    led.on()
    print(ctime() + " - Action - Pressed")
    sleep(duration)
    led.off()
    Octavius_Receiver.send_message("...Released")
    print(ctime() + " - Action - Released")
    return


def Restart():
    return


def handle(msg, Octavius_Receiver):
    duration = 0
    #print(ctime() + f"Message Received - {msg}")

    command = msg.split()
    action = command[0]

    if action == 'ON':
        try:
            on()
            Octavius_Receiver.send_message("Turning computer on")
        except NameError:
            Octavius_Receiver.send_message("LED package not recognised, are you sure this is a pi?")

    elif action == 'OFF':
        try:
            off()
            Octavius_Receiver.send_message("Turning computer off")
        except NameError:
            Octavius_Receiver.send_message("LED package not recognised, are you sure this is a pi?")

    elif action == 'TALK':
        Octavius_Receiver.send_message("Hello, what can I do for you?")

    elif action == "HOLD":
        try:
            duration = int(command[1])
            hold(duration, Octavius_Receiver)
        except NameError:
            Octavius_Receiver.send_message("LED package not recognised, are you sure this is a pi?")

    elif action == "LOG":
        Octavius_Receiver.send_message("Sending logs")
        print(ctime() + " - Action - Send Logs")
        try:
            f = open("cron_log.txt")
            for line in f:
                Octavius_Receiver.send_message(str(line))
            f.close()
        except Exception as E:
            Octavius_Receiver.send_message("Action failed")
            print(ctime() + " - failed with exception:")
            print(E)

    else:
        print(ctime() + " - No action - Command not recognised")
        Octavius_Receiver.send_message("Command not recognised")