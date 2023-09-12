#from gpiozero import LED
import os
import subprocess
import sys
from time import sleep
led = LED(17)


def on():
    led.on()
    sleep(1)
    led.off()
    print("Turning computer on")
    return

def off():
    led.off()
    print("Turning computer off")
    return

def hold(duration, Octavius_Receiver):
    Octavius_Receiver.send_message("Holding...")
    led.on()
    print("Pressed")
    sleep(duration)
    led.off()
    Octavius_Receiver.send_message("...Released")

    print("Released")
    return

'''
def Self_Update():
    os.chdir("..")
    updater_filepath = os.path.abspath(os.curdir) + "\\Updater.py"
    print("Running updater")
    update_file_dir = "Update_Files"
    
    with open(updater_filepath) as f:
        exec(f.read())
    
    if os.path.exists(update_file_dir):
        shutil.rmtree(update_file_dir)

    #    os.remove(update_file_dir)

    clone_repository("https://github.com/8BitFishy/wollybot", update_file_dir,
                     bare=False, repository=None, remote=None, checkout_branch=None, callbacks=None)

    import sys, subprocess
    subprocess.run(["python", updater_filepath])
    subprocess.Popen("python -c \"import os, time; time.sleep(1); os.remove('{}');\"".format(sys.argv[0]))
    sys.exit(0)


    #exit()
    #os.chdir("..")
    #updater_filepath = os.path.abspath(os.curdir) + "\\Updater.py"
    #subprocess.Popen(f'python3 {updater_filepath}')

    #r = requests.get('https://raw.githubusercontent.com/8BitFishy/wollybot/wolly_bot2.py')
    #print(r)




def Restart():
    return

'''

def handle(msg, Octavius_Receiver):
    duration = 0
    print(msg)
    #rawcommand = msg['text']
    #capcommand = msg.upper()

    command = msg.split()
    action = command[0]

    print('Got command: %s' % command)
    print("{}".format(action), end="")

    if action == 'ON':
        print()
        try:
            on()
            Octavius_Receiver.send_message("Turning computer on")
        except NameError:
            Octavius_Receiver.send_message("LED package not recognised, are you sure this is a pi?")

    elif action == 'OFF':
        print()
        try:
            off()
            Octavius_Receiver.send_message("Turning computer off")
        except NameError:
            Octavius_Receiver.send_message("LED package not recognised, are you sure this is a pi?")

    elif action == 'TALK':
        print()
        Octavius_Receiver.send_message("Hello, what can I do for you?")

    elif action == "HOLD":
        try:
            duration = int(command[1])
            print(" {}".format(duration))
            hold(duration, Octavius_Receiver)
        except NameError:
            Octavius_Receiver.send_message("LED package not recognised, are you sure this is a pi?")
    '''
    elif action == "UPDATE":
        print()
        try:
            Octavius_Receiver.send_message("Are you sure you want to update? Yes / No")
            response = Octavius_Receiver.get_response()
            if response == "YES":
                print("Running self update")
                Self_Update()
            else:
                pass
        except Exception as e:
            print(e)
    '''
    else:
        print()
        print("Command not recognised")
        Octavius_Receiver.send_message("Command not recognised")
