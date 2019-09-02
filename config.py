import os

DEBUG = True
HTTPBIN_BASE_URL = "http://localhost/post"
MQ_HOST = "172.17.0.2"
MQ_PORT = 1883
MQ_KEEP_ALIVE = 60
MQ_PASSWORD = None
MQ_USERNAME = None
CLIENT_ID = "OWL_NETWORKS"
SECRET_KEY = os.urandom(64)  
MQ_VERBOSE = True