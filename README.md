# westnile
 A Dockerized Paho Mosquitto Client Subscriber/Publisher App


##### Compose Network Services

* Web - httpbin.org - Docker image - radio subscriber data postback
* Eclipse Mosquitto Broker - Docker image
* MQtt Client - Starts Listening for Topics
* MQtt Publisher - Broadcast Messages to the Broker Client - Scale to n
* MQtt Explorer - TODO: built-in browser based MQtt Explorer

See the repo docker-compose.yml for detailed services list.

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

##### Database

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






