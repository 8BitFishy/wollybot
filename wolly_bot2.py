import Telegram_Manager
import Command_Centre
from time import sleep


def receiver_loop(Octavius_Receiver):
    while True:
        text = Octavius_Receiver.get_response()
        if text != "":
            Command_Centre.handle(text, Octavius_Receiver)

        sleep(0.5)


if __name__ == '__main__':
    print("Starting")
    previousmessage = ''

    Octavius_Receiver = Telegram_Manager.generate_receiver()
    Octavius_Receiver.send_message("I am awake...")
    receiver_loop(Octavius_Receiver)

