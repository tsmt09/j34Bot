import urllib.request
import json

class TeleBot34:
    token = None
    botinfo = None
    curroffset = 0
    updateQueue = []
    regClients = []
    def __init__(self, token):
        self.token = token
        self.getBotInfo()
        pass

    def getBotInfo(self):
        # make request
        f = urllib.request.urlopen("https://api.telegram.org/bot" + self.token +
                                   "/getMe")
        if f.status == 200:
            self.botinfo = json.loads(f.read().decode("utf-8"))

    def getBotUpdates(self):
        # make request
        f = urllib.request.urlopen("https://api.telegram.org/bot" + self.token +
                                   "/getUpdates")
        if f.status == 200:
            update = json.loads(f.read().decode("utf-8"))
            self.updateQueue.extend(update['result'])

        # search for biggest offset
        for e in self.updateQueue:
            if e['update_id'] > self.curroffset:
                self.curroffset = e['update_id']
        # delete list
        f = urllib.request.urlopen("https://api.telegram.org/bot" + self.token +
                                       "/getUpdates?offset=" + str(self.curroffset+1))
        if f.status != 200:
            print("Error deleting updates")

    def sendMessage(self, message, client):
        postParams = {
            'chat_id': client['id'],
            'text': message
        }
        postParams = json.dumps(postParams).encode('utf-8')
        req = urllib.request.Request("https://api.telegram.org/bot" + self.token +
                                   "/sendMessage", data=postParams,
                                   headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        if response == 200:
            print("send ok")

    def sendMessageToAllRegistered(self, message):
        for u in self.regClients:
            self.sendMessage(message, u)

    def handleBotUpdates(self):
        #iterate items
        for e in self.updateQueue:
            if e['message']['text'] == '/start':
                print("user registers " + e['message']['from']['username'], end='')
                # search for id, dont register if registered
                isRegistered = False
                for u in self.regClients:
                    if u['id'] == e['message']['from']['id']:
                        isRegistered = True

                # TODO: send telegram answers
                if not isRegistered:
                    self.regClients.append(e['message']['from'])
                    self.sendMessage("Du wurdest registriert!", e['message']['from'])
                    print("... registered")
                else:
                    print("... not registered")
                    self.sendMessage("Du warst schon registriert!", e['message']['from'])
                    pass

            elif e['message']['text'] == '/stop':
                print("user unregisters " + e['message']['from']['username'], end='')
                # search for element
                isRemoved = False
                for u in self.regClients:
                    if e['message']['from']['id'] == u['id']:
                        print("... removed")
                        self.regClients.remove(u)
                        self.sendMessage("Du wurdest entfernt!", e['message']['from'])
                        isRemoved = True
                if not isRemoved:
                    print("... not removed")
                    self.sendMessage("Du warst nicht auf der Liste :/!", e['message']['from'])
        self.updateQueue.clear()

    def loop(self):
        self.getBotUpdates()
        self.handleBotUpdates()





if __name__ == "__main__":
    t = TeleBot34('306535330:AAGMiYkaXuTNyXK_qUDKKnH_bCslZbQ2oqE')
    t.getBotUpdates()
    t.handleBotUpdates()
    t.sendMessageToAllRegistered("Hallo du Hurensohn")
