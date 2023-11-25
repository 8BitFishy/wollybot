import json
import requests
import urllib
from time import time, ctime

filename = 'telegramID.txt'

with open(filename) as f:
    IDS = f.read().splitlines()

chat_id = str(IDS[0])
TOKEN = str(IDS[1])
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class Message_Receiver:
    def __init__(self, text):
        self.text = text
        self.last_update_id = None

    
    def get_url(self, url):
        try:
            response = requests.get(url)
            content = response.content.decode("utf8")

        except Exception as e:
            print(f"{ctime()} - Error reaching URL ", end="")
            if "get" in url:
                print("for updates:")
            elif "send" in url:
                print("to send message:")
            print(e)
            content = None

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
        #text = text.capitalize()
        print(ctime() + " - Sending Message - " + text)
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    
    def get_response(self):

        updates = self.get_updates(self.last_update_id)

        if len(updates["result"]) > 0:

            self.last_update_id = int(updates["result"][0]["update_id"])

            print(ctime() + " - Received Update: ")
            print(updates)

            date_time = int(str(time()).split(".")[0])

            time_since_message = updates["result"][0]["message"]["date"] - date_time

            self.text = updates["result"][0]["message"]["text"]
            print(ctime() + ' - Update Text - "' + self.text + '"')
            self.last_update_id = self.get_last_update_id(updates) + 1

            if abs(time_since_message) > 20:
                print(ctime() + " - Message timed out")
                self.text=''


        else:
            self.text = ''

        return self.text


def generate_receiver():
    Octavius_Receiver = Message_Receiver("")
    return Octavius_Receiver
