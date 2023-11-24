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
    
    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)
    
    def send_message(self, text):
        #text = text.capitalize()
        print(ctime() + " - Sending Message - " + text)
        text = urllib.parse.quote_plus(text)
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)
    
    def get_response(self):

        #print("Entering get response")
        updates = self.get_updates(self.last_update_id)
        #print(f"Update ID = {self.last_update_id}")

        if len(updates["result"]) > 0:
            self.last_update_id = int(updates["result"][0]["update_id"])

            print(ctime() + " - Received Update: ")
            print(updates)

            date_time = int(str(time()).split(".")[0])
            time_since_message = updates["result"][0]["message"]["date"] - date_time

            if abs(time_since_message) < 20 and self.last_update_id is not None:
                self.text = updates["result"][0]["message"]["text"]
                print(ctime() + ' - Received Message - "' + self.text + '"')
                self.last_update_id = self.get_last_update_id(updates) + 1

            else:
                print(ctime() + " - Message timeout")
                self.text=''
                self.last_update_id = self.get_last_update_id(updates) + 1


        else:
            self.text = ''

        self.text = self.text.upper()
        #print("Leaving get response with text: {}".format(self.text))
        return self.text


def generate_receiver():
    Octavius_Receiver = Message_Receiver("")
    return Octavius_Receiver
