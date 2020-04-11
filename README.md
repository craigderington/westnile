# westnile
 A Paho Mosquito Client Subscriber/Publisher App


##### Services

Web - httpbin.org 
Mosquitto - Eclipse Mosquitto Broker
MQtt Client - Starts Listening for Topics
MQtt Publisher - Broadcast Messages to the Broker Client

##### Usage:

Run docker-compose command at the project folder root and scale number of publishers.

```
# n = number of publisher containers
$ docker-compose up --scale mqttpublisher=n
```






