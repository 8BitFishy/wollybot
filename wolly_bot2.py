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

    print(ctime() + " - Starting")

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

    Octavius_Receiver.send_message("I am online...")

    receiver_loop(Octavius_Receiver)

