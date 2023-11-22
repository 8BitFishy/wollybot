import json
import requests
import urllib
from time import time
import datetime

filename = 'telegramID.txt'

with open(filename) as f:
    IDS = f.read().splitlines()

chat_id = str(IDS[0])
TOKEN = str(IDS[1])
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class Message_Receiver:
    def __init__(self, text, last_update_id):
        self.text = text
        self.last_update_id = last_update_id
        self.log = "log.txt"

    
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
        text = urllib.parse.quote_plus(text)
        self.printlog(text)
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)
    
    def get_response(self):

        print("Entering get response")
        updates = self.get_updates(self.last_update_id)
        print(f"Update ID = {self.last_update_id}")
        print(updates)

        if len(updates["result"]) > 0:
            date_time = int(str(time()).split(".")[0])
            time_since_message = updates["result"][0]["message"]["date"] - date_time

            if abs(time_since_message) < 20 and self.last_update_id is not None:
                self.printlog("Update found")
                self.printlog("Update ID = {}".format(self.last_update_id))
                self.text = updates["result"][0]["message"]["text"]
                self.printlog("Received update = {}".format(updates["result"][0]["message"]["text"]))
                self.last_update_id = self.get_last_update_id(updates) + 1


            else:
                print("Message timeout")
                self.text=''
                self.last_update_id = self.get_last_update_id(updates) + 1


        else:
            self.text = ''

        self.text = self.text.upper()
        print("Leaving get response with text: {}".format(self.text))
        return self.text
    
    
    def get_confirmation(self, Octavius_Vocab):
    
        response = self.get_response()

        if response in Octavius_Vocab.affirmativelist:
            return True
        else:
            return False

    def printlog(self, text):
        f = open(self.log, "a")
        f.write((str(datetime.datetime.now()).split(".", 1)[0]) + (" - ") + str(text))
        f.close()



def generate_receiver():
    Octavius_Receiver = Message_Receiver("", None)
    return Octavius_Receiver
