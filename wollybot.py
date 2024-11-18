try:
    from time import sleep, ctime
    import Telegram_Manager
    import Command_Centre
    import atexit
    from os import system as os
    from platform import system
    print(ctime() + " - Starting Script")

except ModuleNotFoundError as E:
    print("Module missing")
    print(str(E).split("'")[1])
    exit()





def receiver_loop(Octavius_Receiver):
    scheduled_time = None
    scheduled_action = None
    while True:

        text = Octavius_Receiver.get_response()
        if text != "":
            command_content = Command_Centre.handle(text, Octavius_Receiver)

            if command_content is not None:
                scheduled_action = command_content[0]
                scheduled_time = command_content[1]
                print(ctime() + f" - Scheduling action {scheduled_action} at time {scheduled_time}")
                Octavius_Receiver.send_message("Scheduling action {scheduled_action} at time {scheduled_time}")


        if scheduled_time == ctime().split(" ")[3][0:5]:
            print(ctime() + f" - Scheduled action {scheduled_action} at time {scheduled_time}")
            Command_Centre.handle(scheduled_action, Octavius_Receiver)
            scheduled_action = None
            scheduled_time = None

        sleep(2)



def exiting():
    print(ctime() + " - Exiting")


try:
    if __name__ == '__main__':

        print(ctime() + " - Initialising")

        atexit.register(exiting)

        if system() == "Linux":
            sleep(30)
        else:
            pass

        previousmessage = ''
        Octavius_Receiver = None

        while Octavius_Receiver is None:
            sleep(10)
            try:
                Octavius_Receiver = Telegram_Manager.generate_receiver()

            except Exception as E:
                print(ctime() + " - Error Initialising - ")
                print(str(E))
                print(ctime() + " - Retrying in 10 seconds")

        if Octavius_Receiver is None:
            print(ctime() + " - Initialisation failed, rebooting")
            os("sudo reboot")

        else:
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
                        print(ctime() + " - Connection cannot be established, rebooting")
                        os("sudo reboot")

            receiver_loop(Octavius_Receiver)

except Exception as E:
    print(E)