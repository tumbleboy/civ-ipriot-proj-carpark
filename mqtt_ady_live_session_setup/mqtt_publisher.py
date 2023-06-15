"""
    THIS IS A PUBLISHER THAT WILL PUBLISH MESSAGES TO A SPECIFIC TOPIC SO THAT
    CLIENTS CAN SUBSCRIBE TO THAT TOPIC AND RECEIVE THOSE MESSAGES
    THE MESSAGES ARE DICTIONARIES DELIVERED IN JSON FORMAT
"""
import paho.mqtt.client as mqtt
import time
from random import randrange, uniform
import json
import datetime

MQTT_HOST = "localhost"  # replace local host with computer name that MQTT is running on
MQTT_PORT = 1883  # default MQTT port
MQTT_KEEP_ALIVE = 300  # seconds - this keeps the connection open

MQTT_CLIENT_NAME = "duck-off"  # must be unique
MQTT_TOPIC = "test/ducks"  # main topic: test, sub topic: ducks

# Instantiate a client object
client = mqtt.Client(MQTT_CLIENT_NAME)

# Connect to the server
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)
print(f"Sending message to MQTT broker {MQTT_HOST} on port {MQTT_PORT}")
print(f"with the topic {MQTT_TOPIC}")

# Publish to the topic
while True:
    time.sleep(4)
    # simulate temperature and current time and store in dictionary
    temperature = uniform(15, 35)
    now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    message_data = {
        "client": MQTT_CLIENT_NAME,
        "topic": MQTT_TOPIC,
        "temperature": temperature,
        "datetime": now
    }
    # convert the message_data dictionary into json string
    message_to_send = json.dumps(message_data)

    # publish to topic
    client.publish(MQTT_TOPIC, message_to_send)
