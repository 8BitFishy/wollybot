import json
import sys

import requests
import urllib
from time import time, ctime, sleep
from platform import system
import os

filename = 'telegramID.txt'
if system() == "Linux":
    directory = __file__.strip("Telegram_Manager.py").strip(":")
else:
    directory = os.getcwd() + "\\"
    #print(os.listdir())

with open(f'{directory}{filename}') as f:
    IDS = f.read().splitlines()

chat_id = str(IDS[0])
TOKEN = str(IDS[1])
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class Message_Receiver:
    def __init__(self, text):
        self.text = text
        self.last_update_id = None
    
    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content
    
    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js
    
    def get_updates(self, offset=None):
        url = URL + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js
    
    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def send_message(self, text):

        try:
            print(ctime() + " - Sending Message - " + text)
            text = urllib.parse.quote_plus(text)
            url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
            self.get_url(url)
            return True

        except Exception as e:
            print(f"{ctime()} - Error reaching URL, cannot send message")
            print(e)
            return False

    
    def get_response(self):
        self.text = ""
        try:
            updates = self.get_updates(self.last_update_id)

            if len(updates["result"]) is not None:

                if len(updates["result"]) > 0:

                    self.last_update_id = int(updates["result"][0]["update_id"])

                    #print(ctime() + " - Received Update")
                    #print(updates)

                    date_time = int(str(time()).split(".")[0])
                    time_since_message = updates["result"][0]["message"]["date"] - date_time
                    self.last_update_id = self.get_last_update_id(updates) + 1

                    if abs(time_since_message) < 20:
                        self.text = updates["result"][0]["message"]["text"]
                        print(ctime() + ' - Received message - "' + self.text + '"')

                    else:
                        print(ctime() + " - Message timed out")

            return self.text

        except Exception as e:
            print(ctime() + " - Caught exception")
            try:
                if str(updates["error_code"]) == str(409):
                    print(ctime() + " - Is 409 error")
                    raise sys.exit()

            except:
                pass
            print(f"{ctime()} - Error reaching URL, cannot get updates")
            print(f"{ctime()} - Exception {e}")
            self.text = ''
            sleep(5)
            return self.text

def generate_receiver():
    Octavius_Receiver = Message_Receiver("")
    return Octavius_Receiver
