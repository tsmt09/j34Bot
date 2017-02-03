import paho.mqtt.client as mqtt
from telebot34 import TeleBot34

class Paho34:
    # class settings
    pahoClient = None
    username = None
    password = None
    server = None
    port = None
    subs = None
    bot = None
    machineState = 0

    def __init__(self, config):
        # init MQTT Client
        self.pahoClient = mqtt.Client()
        self.pahoClient.on_connect = self.onConnect
        self.pahoClient.on_message = self.onMessage
        self.username = config['MQTT']['USER']
        self.password = config['MQTT']['PASS']
        self.server = config['MQTT']['SERV']
        self.port = int(config['MQTT']['PORT'])
        self.subs = config['MQTT-Subs']
        # init Bot
        self.bot = TeleBot34(config['Telegram']['Token'])

    def onConnect(self, client, userdata, flags, rc):
        global conerrorPrintOnce
        if rc == 0:
            print("connected")
            conerrorPrintOnce = 0
            for k, v in self.subs.items():
                print("subscribe to: "+v)
                client.subscribe(v)
        # print error once if connection is unavailable
        else:
            if conerrorPrintOnce == 0:
                print("No Connect: " + str(rc))
                conerrorPrintOnce = 1

    # onMessage simply print
    def onMessage(self, client, userdata
                  , msg):
        if msg.topic == "llearnd/machine/state":
            #convert to state
            state = int(msg.payload.decode('utf-8'))
            if state == 2:
                # state is now on
                # check if it was off
                if self.machineState < 2:
                    self.bot.sendMessageToAllRegistered("Ein Waschgang wurde gestartet!")
            elif state < 2:
                # state is now off
                # check if it was on
                if self.machineState == 2:
                    self.bot.sendMessageToAllRegistered("Ein Waschgang wurde beendet!")
            self.machineState = state

    def connect(self):
        self.pahoClient.username_pw_set(self.username, self.password)
        self.pahoClient.connect(self.server, self.port)

    def loop(self):
        # TODO: reconnect
        #if not self.pahoClient.connected:
        #    self.connect()
        self.pahoClient.loop()
        self.bot.loop()
