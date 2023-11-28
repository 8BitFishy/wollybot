import Telegram_Manager
import Command_Centre
from time import sleep, ctime
import atexit

print(ctime() + " - Starting Script")

def receiver_loop(Octavius_Receiver):

    while True:
        text = Octavius_Receiver.get_response()
        if text != "":
            Command_Centre.handle(text, Octavius_Receiver)

        sleep(2)



def exiting():
    print(ctime() + " - Exiting")



if __name__ == '__main__':
    print(ctime() + " - Initialising")

    atexit.register(exiting)

    sleep(30)


    previousmessage = ''

    try:
        Octavius_Receiver = Telegram_Manager.generate_receiver()


    except Exception as E:
        print(ctime() + " - Error Initialising - ")
        print(str(E))
        print(ctime() + " - Retrying in 10 seconds")

        Octavius_Receiver = None
        while Octavius_Receiver is None:
            sleep(10)
            try:
                Octavius_Receiver = Telegram_Manager.generate_receiver()

            except Exception as E:
                print(ctime() + " - Error Initialising - ")
                print(str(E))
                print(ctime() + " - Retrying in 10 seconds")

    print(ctime() + " - Initialisation Complete, Connecting to URL")

    connected = Octavius_Receiver.send_message("I am online...")
    attempts = 0

    if connected is False:
        print(ctime() + " - Re-trying…")
        while connected is False:
            attempts += 1
            sleep(10)
            connected = Octavius_Receiver.send_message("I am online...")
            print(ctime() + " - Re-trying…")
            if attempts > 10:
                connected = True
                
    receiver_loop(Octavius_Receiver)

