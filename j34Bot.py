import configparser
import time
from paho34 import Paho34

config=configparser.ConfigParser()
config.read('config.ini')

def main():
    mqtt = Paho34(config)
    while True:
        mqtt.loop()
        time.sleep(0.2)
    return 0

if __name__ == "__main__":
    main()
