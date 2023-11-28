from time import sleep, ctime
from os import listdir, system, remove
from os.path import isfile, join
try:
    from gpiozero import LED
    led = LED(17)

except:
    print(f'No gpiozero module found')



directory = __file__.strip("Command_Centre.py").strip(":")
protected_files = ['Command_Centre.py', 'Telegram_Manager.py', 'wollybot.py', 'telegramID.txt']
git_repo = 'https://raw.githubusercontent.com/8BitFishy/wollybot/deployed/'

def update():
    system("rm wollybot/Command_Centre.py")
    system("rm wollybot/Telegram_Manager.py")
    system("rm wollybot/wollybot.py")
    system(f"wget -P {directory} {git_repo}Command_Centre.py")
    system(f"wget -P {directory} {git_repo}Telegram_Manager.py")
    system(f"wget -P {directory} {git_repo}wollybot.py")
    return

def download(filename):
    system(f"wget -P {directory} {git_repo}{filename}")
    return

def handle_error(E, Octavius_Receiver):
    Octavius_Receiver.send_message("Action failed - " + E.__class__.__name__)
    print(ctime() + " - failed with exception:")
    print(E)
    return

def talk(Octavius_Receiver):
    Octavius_Receiver.send_message("I am active. My current commands are: ")
    Octavius_Receiver.send_message("On")
    Octavius_Receiver.send_message("Off")
    Octavius_Receiver.send_message("Hold")
    Octavius_Receiver.send_message("Talk")
    Octavius_Receiver.send_message("Reboot")
    Octavius_Receiver.send_message("Update")
    Octavius_Receiver.send_message("Download (filename")
    Octavius_Receiver.send_message("Print files")
    Octavius_Receiver.send_message("Print (filename)")
    Octavius_Receiver.send_message("Length (filename)")
    Octavius_Receiver.send_message("Delete (filename)")
    return

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

def reboot():
    system("sudo reboot")
    return

def delete(filename):
    remove(filename)
    return

def download(filename):
    system(f"wget -P {directory} {git_repo}{filename}")
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
            handle_error(E, Octavius_Receiver)

    elif action == 'TALK':
        talk(Octavius_Receiver)

    elif action == "HOLD":
        try:
            duration = int(command[1])
            Octavius_Receiver.send_message(f"Holding button for {duration} seconds")
            print(ctime() + " - Action - Hold " + str(duration))
            hold(duration)

        except Exception as E:
            handle_error(E, Octavius_Receiver)


    elif action == "PRINT" and command[1] != "files":

        filename = str(command[1])
        with open(f'{directory}{filename}') as file:
            count = sum(1 for _ in file)
            file.close()
        if count > 0:
            print(ctime() + " - Action - Sending file: ")
            print(f'{directory}{filename}')
            Octavius_Receiver.send_message(f"Accessing {filename}")

            try:
                f = open(f'{directory}{filename}')
                if len(command) == 3:
                    for line in (f.readlines()[-int(command[2]):]):
                        Octavius_Receiver.send_message(str(line).strip())

                else:
                    Octavius_Receiver.send_message(str(f.read()))
                f.close()

            except Exception as E:
                handle_error(E, Octavius_Receiver)

        else:
            Octavius_Receiver.send_message(f"{filename} is currently empty")


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
            handle_error(E, Octavius_Receiver)


    elif action == "REBOOT":
        print(ctime() + " - Rebooting")
        Octavius_Receiver.send_message("Rebooting")

        try:
            reboot()

        except Exception as E:
            handle_error(E, Octavius_Receiver)


    elif action == "DELETE":
        filename = str(command[1])
        if filename not in protected_files:
            print(ctime() + " - Action - Deleting file: " + filename)
            Octavius_Receiver.send_message(f"Deleting {filename}")

            try:
                delete(f'{directory}{filename}')
                Octavius_Receiver.send_message(f"{filename} deleted")

            except Exception as E:
                handle_error(E, Octavius_Receiver)

        else:
            Octavius_Receiver.send_message("That file is protected, please don't try to delete this")


    elif action == "LENGTH":

        filename = str(command[1])
        print(ctime() + " - Action - Sending length of file: " + filename)
        Octavius_Receiver.send_message(f"Reading length of {filename}")

        try:
            with open(f'{directory}{filename}') as file:
                count = sum(1 for _ in file)
                Octavius_Receiver.send_message(f"File is {count} lines long")
                file.close()

        except Exception as E:
            handle_error(E, Octavius_Receiver)


    elif action == "UPDATE":
        try:
            print(ctime() + " - Action - Update")
            Octavius_Receiver.send_message(f"Updating files")
            update()
            print(ctime() + " - Update Complete")
            Octavius_Receiver.send_message(f"Update complete, rebooting")
            reboot()

        except Exception as E:
            handle_error(E, Octavius_Receiver)

    elif action == "DOWNLOAD":
        filename = str(command[1])

        try:
            print(ctime() + f" - Action - Download {filename}")
            Octavius_Receiver.send_message(f"Downloading {filename} from my repo")
            download(filename)
            Octavius_Receiver.send_message(f"{filename} downloaded")

        except Exception as E:
            handle_error(E, Octavius_Receiver)


    else:
        print(ctime() + " - No action - Command not recognised")
        Octavius_Receiver.send_message("Command not recognised")