import os

DEBUG = True
HTTPBIN_BASE_URL = "http://httpbin/post"
MQ_HOST = "mosquitto"
MQ_PORT = 1883
MQ_KEEP_ALIVE = 60
MQ_PASSWORD = None
MQ_USERNAME = None
CLIENT_ID = "CLD_NETWORKS"
SECRET_KEY = os.urandom(64)  
MQ_VERBOSE = True
