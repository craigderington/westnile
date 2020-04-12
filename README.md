# westnile
 A Dockerized Paho Mosquitto Client Subscriber/Publisher App.  Simulate remote cellular radio IoT devices deployed in the field and publishing their sensor data to the Mosquitto message broker.

##### Docker Compose Network Services Stack

* Eclipse Mosquitto Broker - Custom Docker image implementing web sockets on port 9001
* MQtt Client - Sets up the topics and listens on ports 1883 and 9001
* MQtt Publisher - Simulate messages from remote IoT device - Scale to n
* Web Gateway - httpbin.org - Docker image - radio subscriber request/response data postback
* MQtt Explorer - HiveMQ Websockets Client Showcase - built-in browser based MQtt Explorer using web sockets

See the repo docker-compose.yml for a detailed list of network services.

##### Installation

Clone this repository

```
$ git clone https://github.com/craigderington/westnile.git
```

##### Usage

Run docker-compose command at the project folder root and scale number of publishers.
```n = number of publisher containers```

```
$ cd westnile
$ docker-compose up --scale mqttpublisher=n
```

##### HiveMQ Browser Client

Use the built-in HiveMQ browser client to subscribe to topics and publish new messages.  Open your web browser and visit http://0.0.0.0:8080 and enter these values:

* Broker = "0.0.0.0"
* Port = 9001
* ClientID = default value

##### Database Records

To view database records; from the command line, run this command

```
$ docker exec westnile_mqttclient_1 python
```

Then from the mqttclient container's Python shell...

```
Python 3.7.3 (default, Dec 13 2019, 19:58:14) 
[Clang 11.0.0 (clang-1100.0.33.17)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import sqlite3
>>> con = sqlite3.connect("westnile.db")
>>> cur = con.cursor()
>>> rows = cur.execute("SELECT * from messages)
>>> for row in rows:
    print(row)
```

##### TODO: IoT Data Browser Container App

Coming soon:  Implement Flask and SQLAlchemy to browse, view and edit the sqlite3 radio data.
