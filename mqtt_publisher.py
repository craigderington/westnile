#!.env/bin/python

import argparse
import config
import context
from datetime import datetime, timedelta
import json
import logging
import paho.mqtt.client as mqtt
import random
import requests
import string
import time


logging.basicConfig(filename="{}.log".format(__name__), level=logging.DEBUG)

# constants
RADIOS = ["8973", "9989", "9990", "10201", "12413", "13773"]
NETWORKS = ["ORLFL01", "NANMA01", "DALTX01", "RALNC01"]


# client connack response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code: {}".format(str(rc)))
        client.connected_flag = True
    else:
        print("Bad Connection.  Return Code: {}".format(str(rc)))
        client.disconnect_flag = True


# display the message id when a message is published
def on_publish(mqttc, obj, mid):
    print("Published Message ID: {}".format(str(mid)))


# on log function
def on_log(mqttc, obj, level, string):
    print(string)


# on disconnect
def on_disconnect(client, userdata, rc):
    print("Client {} Disconnected: {}".format(str(client), str(rc)))
    client.connected_flag = False
    client.disconnect_flag = True


# generate a new reading
def get_reading(client_id):
    data = {}
    data["radio_id"] = random.choice(RADIOS)
    data["network_id"] = client_id
    data["timestamp"] = datetime.now().strftime("%c")
    data["level"] = random.randint(100, 999)/100.00
    data["current"] = random.randint(100, 999)/100.00
    data.update()
    return data


# main
def main():
    """ Create the MQtt client and loop forever """    
    # set the publisher client ID from args
    parser = argparse.ArgumentParser(description="Unique Client ID for MQtt Client")
    parser.add_argument("--client_id", 
                        type=str, 
                        help="Publisher client requires a client ID.  Must be unique.")
    
    # parse the command line arguments
    args = parser.parse_args()
    
    if args:
        client_id = args.client_id
    else:
        client_id = "".join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(16)]
        )

    # create mqtt client
    client = mqtt.Client(args.client_id)
    logger = logging.getLogger(__name__)
    client.enable_logger(logger)
    
    # register callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # check debug
    if config.DEBUG:
        client.on_log = on_log

    if config.MQ_USERNAME:
        client.username_pw_set(config.MQ_USERNAME, config.MQ_PASSWORD)

    # publish new messages every 5 minutes  
    while True:      

        # client connect
        client.connect(
            config.MQ_HOST,
            config.MQ_PORT,
            config.MQ_KEEP_ALIVE
        )

        # get a new random reading and publish
        reading = get_reading(client_id)
        data = json.dumps(reading)
        client.publish(
            "OWL/Networks/" + client_id,
            data
        )

        # sleep
        time.sleep(5.01)


if __name__ == "__main__":
    main()
