"""
    THIS IS A SUBSCRIBER THAT IS SUBSCRIBED TO GEESE AND LISTENS IN
    FOR MESSAGES THAT HAVE BEEN SENT TO GEESE VIA MQTT_PUB_SUB.PY
    THE MESSAGES ARE JSON DESCRIBING THE WEATHER CONDITION
"""
import paho.mqtt.client as mqtt
import json
import datetime

# Declare constants
MQTT_HOST = "localhost"  # replace local host with computer name that MQTT is running on
MQTT_PORT = 1883  # default MQTT port
MQTT_KEEP_ALIVE = 300  # seconds - this keeps the connection open

MQTT_CLIENT_NAME = "geese-off"  # must be unique
MQTT_TOPIC = "test/geese"  # main topic: test, sub topic: ducks

# Instantiate a client object
client = mqtt.Client(MQTT_CLIENT_NAME)

# Connect to the server
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

# Subscribe to the topic
client.subscribe(MQTT_TOPIC)


def on_message_callback(client, userdata, message):
    msg = message
    msg_data = str(msg.payload.decode("UTF-8"))  # decode the message payload into UTF-8 characters
    json_data = json.loads(msg_data)
    print(f"The current temperature is {round(json_data['temperature'])} degrees. {json_data['message']}")


# Listen for messages - call the callback function once message is received
client.on_message = on_message_callback

print(f"{MQTT_CLIENT_NAME} is listening on {MQTT_PORT} for messages with the topic {MQTT_TOPIC}")

client.loop_forever()
