from time import sleep, ctime
from os import listdir
from os.path import isfile, join
#from gpiozero import LED
#led = LED(17)

def on():
    led.on()
    return

def off():
    led.off()
    return

def hold(duration):
    on()
    sleep(duration)
    off()
    return


def Restart():
    return


def handle(msg, Octavius_Receiver):

    command = msg.split()
    action = command[0].upper()

    if action == "HELLO":
        Octavius_Receiver.send_message("Hello, what can I do for you?")

    elif action == 'ON' or action == "OFF":

        try:
            if action == "ON":
                modifier = "on"
            else:
                modifier = "off"

            Octavius_Receiver.send_message("Turning computer " + modifier)
            print(ctime() + " - Action - Turning computer " + modifier)
            hold(1)

        except Exception as E:
            Octavius_Receiver.send_message("Action failed - " + E.__class__.__name__)
            print(ctime() + ctime() + " - failed with exception:")
            print(E)

    elif action == 'TALK':
        Octavius_Receiver.send_message("I am active. My current commands are: ")
        Octavius_Receiver.send_message("On")
        Octavius_Receiver.send_message("Off")
        Octavius_Receiver.send_message("Hold")
        Octavius_Receiver.send_message("Talk")
        Octavius_Receiver.send_message("Print files")
        Octavius_Receiver.send_message("Print (filename)")


    elif action == "HOLD":
        try:
            duration = int(command[1])
            Octavius_Receiver.send_message(f"Holding button for {duration} seconds")
            print(ctime() + " - Action - Hold " + str(duration))
            hold(duration)

        except Exception as E:
            Octavius_Receiver.send_message("Action failed - " + E.__class__.__name__)
            print(ctime() + " - failed with exception:")
            print(E)


    elif action == "PRINT" and command[1] != "files":

        filename = str(command[1])
        print(ctime() + " - Action - Sending file: " + filename)
        Octavius_Receiver.send_message(f"Accessing {filename}")

        try:
            f = open(filename)
            if len(command) == 3:
                for line in (f.readlines()[-int(command[2]):]):
                    Octavius_Receiver.send_message(str(line))

            else:
                Octavius_Receiver.send_message(str(f.read()))
            f.close()

        except Exception as E:
            Octavius_Receiver.send_message("Action failed - " + E.__class__.__name__)
            print(ctime() + " - failed with exception:")
            print(E)

    elif action == "PRINT" and command[1] == "files":

        print(ctime() + " - Action - Read file names")

        try:
            current_directory = __file__.strip("Command_Centre.py").strip(":")
            print(ctime() + " - Searching directory: \n" + current_directory)
            Octavius_Receiver.send_message("Files found:")

            for f in listdir(current_directory):
                if isfile(join(current_directory, f)):
                    Octavius_Receiver.send_message(f)

        except Exception as E:
            Octavius_Receiver.send_message("Action failed - " + E.__class__.__name__)
            print(ctime() + " - failed with exception:")
            print(E)


    else:
        print(ctime() + " - No action - Command not recognised")
        Octavius_Receiver.send_message("Command not recognised")