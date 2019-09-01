#!.env/bin/python

import context
import requests
import paho.mqtt.client as mqtt
import time
from datetime import datetime, timedelta
from db import db_session
import logging
logging.basicConfig(filename="{}.log".format(__name__), level=logging.DEBUG)


# client connack response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: {}".format(str(rc)))

    main_topic = "OWL/Networks"
    sub_topics = ["ORLFL01", "NANMA01", "DALTX01", "RALNC01"]

    # subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will automaticaly be renewed.
    for i in sub_topics:
        client.subscribe("{}/{}".format(main_topic, i))


# published message is received from the server.
def on_message(client, userdata, msg):
    """ MQtt on_message function """
    print("New Message Received: {} {}".format(str(msg.topic), msg.payload.decode("utf-8")))


# display the message id when a message is published
def on_publish(mqttc, obj, mid):
    print("Published Message ID: {}".format(str(mid)))


# show on_subscribe message
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: {} {}".format(str(mid), str(granted_qos)))


# on log function
def on_log(mqttc, obj, level, string):
    print(string)


# main
def main():
    """ Create the MQtt client and loop forever """
    debug = True
    host = "172.17.0.2"
    client_id = "OWL_NETWORKS"
    keepalive = 60
    port = 1883
    password = None
    username = None
    verbose = True

    # init db
    db = db.init_db()

    # create mqtt client
    client = mqtt.Client(client_id)
    logger = logging.getLogger(__name__)
    client.enable_logger(logger)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish

    # check debug
    if debug:
        client.on_log = on_log

    if username:
        client.username_pw_set(username, password)

    # client connect
    client.connect(host, port, keepalive)

    # client loop
    client.loop_forever()


if __name__ == "__main__":
    main()
