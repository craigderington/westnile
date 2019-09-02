#!.env/bin/python
# publisher.py
import context
import random
import requests
import json
import paho.mqtt.client as mqtt
import time
from datetime import datetime, timedelta
import logging
logging.basicConfig(filename="{}.log".format(__name__), level=logging.DEBUG)

# constants
RADIOS = ["8973", "9989", "9990", "10201", "12413", "13773"]
NETWORKS = ["ORLFL01", "NANMA01", "DALTX01", "RALNC01"]


# client connack response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: {}".format(str(rc)))


# display the message id when a message is published
def on_publish(mqttc, obj, mid):
    print("Published Message ID: {}".format(str(mid)))


# on log function
def on_log(mqttc, obj, level, string):
    print(string)


# generate a new reading
def get_reading():
    data = {}
    data["radio_id"] = random.choice(RADIOS)
    data["network_id"] = "DALTX01"
    data["radio_name"] = data["network_id"] + "_" + data["radio_id"]
    data["timestamp"] = datetime.now().strftime("%c")
    data["level"] = random.randint(100, 999)/100.00
    data["current"] = random.randint(100, 999)/100.00
    data.update()
    return data


# main
def main():
    """ Create the MQtt client and loop forever """
    debug = True
    host = "172.17.0.2"
    client_id = "DALTX01"
    keepalive = 60
    port = 1883
    password = None
    username = None
    verbose = True

    # create mqtt client
    client = mqtt.Client(client_id)
    logger = logging.getLogger(__name__)
    client.enable_logger(logger)
    client.on_connect = on_connect
    client.on_publish = on_publish

    # check debug
    if debug:
        client.on_log = on_log

    if username:
        client.username_pw_set(username, password)

    # publish new messages every 5 minutes  
    while True:      

        # client connect
        client.connect(host, port, keepalive)

        # get a new random reading and publish
        reading = get_reading()
        data = json.dumps(reading)
        client.publish(
            "OWL/Networks/DALTX01",
            data
        )

        # sleep
        time.sleep(7.75)


if __name__ == "__main__":
    main()
