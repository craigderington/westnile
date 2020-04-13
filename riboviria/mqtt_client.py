#!.env/bin/python

import os
import context
import requests
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime, timedelta
from db import init_db, db_session
from models import Message
from sqlalchemy import exc, func
import logging
import config

# configure logging
logging.basicConfig(filename="{}.log".format(__name__), level=logging.DEBUG)


# client connack response from the server.
def on_connect(client, userdata, flags, rc):
    
    if rc == 0:
        print("Connected with result code: {}".format(str(rc)))

        main_topic = "CLD/Networks"
        sub_topics = get_networks()

        # subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will automaticaly be renewed.
        for i in sub_topics:
            client.subscribe("{}/{}".format(main_topic, i))

        client.connected_flag = True
    
    else:
        print("Bad connection.  Returned code: {}".format(str(rc)))
        client.bad_connection_flag = True


# published message is received from the server.
def on_message(client, userdata, msg):
    """ MQtt on_message function """
    print("New Message Received: {}".format(str(msg.topic)))

    # encode payload object to json
    data = json.loads(msg.payload.decode("utf-8"))

    try:

        # create a new message object
        new_msg = Message(
            radio_type="Gen6-R64",
            radio_id=data["radio_id"],
            network_id=data["network_id"],
            current=data["current"],
            level=data["level"]
        )

        # save to database
        db_session.add(new_msg)
        db_session.commit()
        db_session.flush()

        # output the new message id
        print("New Message Saved as: {}".format(str(new_msg.id)))

    except exc.SQLAlchemyError as err:
        print("Database exception occured: {}".format(str(err)))


    # post the data to an endpoint
    try:
        r = requests.request(
            "POST",
            config.HTTPBIN_BASE_URL,
            headers={"content-type": "application/json"},
            data=json.dumps(data)
        )

        if r.status_code == 200:
            resp = r.json()
            print("Response Headers: {} "
                  "Response Body: {}".format(r.headers, resp))
        
        else:
            print("HTTPBIN returned status code: {}".format(str(r.status_code)))

    except requests.HTTPError as http_err:
        print("HTTP Error contacting HTTPBIN: {}".format(str(http_err)))


# display the message id when a message is published
def on_publish(mqttc, obj, mid):
    print("Published Message ID: {}".format(str(mid)))


# show on_subscribe message
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: {} {}".format(str(mid), str(granted_qos)))


# on disconnect
def on_disconnect(client, userdata, rc):
    print("Client Disconnected: {}".format(str(rc)))
    client.connected_flag = False
    client.disconnect_flag = True


# on log function
def on_log(mqttc, obj, level, string):
    print(string)


# read list of approved networks
def get_networks():
    """ read approved network list for client topics """
    networks = []
    path = os.getcwd()
    filename = "networks.txt"
    with open(path + "\\" + filename, "r") as f1:
        lines = f1.readlines()
        for line in lines:
            row = line.replace("\n", "")
            networks.append(row)

    return networks

# main
def main():
    """ Create the MQtt client and loop forever """
    # set up the client
    client = mqtt.Client(config.CLIENT_ID)
    logger = logging.getLogger(__name__)
    client.enable_logger(logger)
    
    # init sqlite
    init_db()
    
    # register callbacks
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # check debug
    if config.DEBUG:
        client.on_log = on_log

    if config.MQ_USERNAME:
        client.username_pw_set(config.MQ_USERNAME, config.MQ_PASSWORD)

    # client connect
    client.connect(
        config.MQ_HOST,
        config.MQ_PORT,
        config.MQ_KEEP_ALIVE
    )

    # client loop
    client.loop_forever()


if __name__ == "__main__":
    main()
