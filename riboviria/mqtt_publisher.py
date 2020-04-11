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

# configure logging
logging.basicConfig(filename="{}.log".format(__name__), level=logging.DEBUG)

# constants
RADIOS = ["8973", "9989", "9990", "10201", "12413", "13773"]
NETWORKS = ["NYCNY2011", "BOSMA5077", "LACA3978", "LVNV10022", "SEAWA9011", "TAMFL1042",
            "RALNC7565", "BALMD3322", "DALTX7701", "CHIIL5555"]


def on_connect(client, userdata, flags, rc):
    """
    On Connect callback
    Client connack response from the server.
    :param client, userdata, flags, rc
    :return client.connected_flag
    """
    if rc == 0:
        print("Connected with result code: {}".format(str(rc)))
        client.connected_flag = True
    else:
        print("Bad Connection.  Return Code: {}".format(str(rc)))
        client.disconnect_flag = True


def on_publish(client, obj, mid):
    """
    On Publish callback
    Display the message id when a message is published
    :param client, obj, mid
    :return mid <message_id> int
    """
    print("Published Message ID: {}".format(str(mid)))


def on_log(client, obj, level, string):
    """
    On Log callback
    Logging utilities
    :param client, obj, level, string
    :return string
    """
    print(string)


def on_disconnect(client, userdata, rc):
    """
    On disconnect callback
    Display message when client disconnects
    :param client, userdata, rc
    :return client.disconnect_flag
    """
    print("Client {} Disconnected: {}".format(str(client), str(rc)))
    client.connected_flag = False
    client.disconnect_flag = True


# generate a new reading
def get_reading(client_id):
    """
    Generate a psuedo random radio reading
    :param client_id
    :return data <dict>
    """
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
    """ 
    Create the MQtt client 
    :param client_id <string>
    :return MQtt publisher client loop
    """    
    # set the publisher client ID from args
    # parser = argparse.ArgumentParser(description="Unique Client ID for MQtt Client")
    """
    # parser.add_argument("-c", 
                        type=str,
                        required=True,
                        default="NYCNY2011", 
                        help="Publisher client requires a client ID.  Must be unique.")
    
    # parse the command line arguments
    args = parser.parse_args()    
    """
    # create mqtt client
    client_id = NETWORKS[random.randint(0,9)]
    client = mqtt.Client(client_id)
    logger = logging.getLogger(__name__)
    client.enable_logger(logger)
    
    # register callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # check debug
    if config.DEBUG:
        client.on_log = on_log

    # check username
    if config.MQ_USERNAME:
        client.username_pw_set(config.MQ_USERNAME, config.MQ_PASSWORD)

    # publish new messages every ~ 5 minutes  
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
            "CLD/Networks/" + client_id,
            data
        )

        # sleep
        time.sleep(5.01)


if __name__ == "__main__":
    main()
