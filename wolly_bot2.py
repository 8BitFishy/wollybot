import Telegram_Manager
import Command_Centre
from time import sleep, ctime
import atexit


def receiver_loop(Octavius_Receiver):

    while True:
        text = Octavius_Receiver.get_response()
        if text != "":
            Command_Centre.handle(text, Octavius_Receiver)

        sleep(1)

def exiting():
    print(ctime() + " - Exiting")


if __name__ == '__main__':

    atexit.register(exiting)

    sleep(30)

    print(ctime() + " - Initialising")

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

    print(ctime() + " - Connecting to URL")
    try:
        Octavius_Receiver.send_message("I am online...")

    except Exception as E:
        print(ctime() + " - Re-trying…")
        while failed is True:
            try:
                Octavius_Receiver.send_message("I am online...")
                failed = False
            except:
                sleep(5)

    receiver_loop(Octavius_Receiver)

