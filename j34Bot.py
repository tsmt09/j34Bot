import configparser
import time
from paho34 import Paho34
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--config', type=str, help='set config path')

args = parser.parse_args()

if not os.path.isfile(args.config):
    print("config file not found")
    sys.exit(1)

config=configparser.ConfigParser()
config.read(args.config)

def main():
    mqtt = Paho34(config)
    while True:
        mqtt.loop()
        time.sleep(0.2)
    return 0

if __name__ == "__main__":
    main()
