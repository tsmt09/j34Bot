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
    timeout = 60
    connected = 0
    connectedMsg = 0
    machineState = 0
    conerrorPrintOnce = 0

    def __init__(self, config):
        # init MQTT Client
        self.pahoClient = mqtt.Client()
        self.pahoClient.on_connect = self.onConnect
        self.pahoClient.on_message = self.onMessage
        self.pahoClient.on_disconnect = self.onDisconnect
        self.username = config['MQTT']['USER']
        self.password = config['MQTT']['PASS']
        self.server = config['MQTT']['SERV']
        self.port = int(config['MQTT']['PORT'])
        self.subs = config['MQTT-Subs']
        self.connected = 0
        self.connectedMsg = 0
        # init Bot
        self.bot = TeleBot34(config['Telegram']['Token'])

    def onDisconnect(self, client, userdata, rc):
        print("paho disconnect: "+str(rc))
        self.connected = 0

    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected")
            self.connectedMsg = 0
            self.connected = 1
            self.conerrorPrintOnce = 0
            for k, v in self.subs.items():
                print("subscribe to: "+v)
                client.subscribe(v)
        # print error once if connection is unavailable
        else:
            print("noconnect")
            if self.conerrorPrintOnce == 0:
                print("No Connect: " + str(rc))
                self.conerrorPrintOnce = 1

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
                    print("machine turned on")
                    self.bot.sendMessageToAllRegistered("Ein Waschgang wurde gestartet!")
            elif state < 2:
                # state is now off
                # check if it was on
                if self.machineState == 2:
                    print("machine turned off")
                    self.bot.sendMessageToAllRegistered("Ein Waschgang wurde beendet!")
            self.machineState = state

    def connect(self):
        print("conn")
        try:
            self.pahoClient.username_pw_set(self.username, self.password)
            self.pahoClient.connect(self.server, self.port, self.timeout)
        except ConnectionRefusedError as err:
            print(err)
            if self.connectedMsg == 0:
                self.bot.sendMessageToAllRegistered("bot MQTT disconnected!");
                print("connection refused by server")
                self.connectedMsg = 1

    def loop(self):
        if self.connected < 1:
            self.connect()
        self.pahoClient.loop()
        self.bot.loop()
