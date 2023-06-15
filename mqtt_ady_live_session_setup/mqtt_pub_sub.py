"""
    THIS WILL LISTEN ON DUCKS, AND PUBLISH TO GEESE
"""
import paho.mqtt.client as mqtt
import json
import datetime

# Declare constants
MQTT_HOST = "localhost"  # replace local host with computer name that MQTT is running on
MQTT_PORT = 1883  # default MQTT port
MQTT_KEEP_ALIVE = 300  # seconds - this keeps the connection open

MQTT_CLIENT_NAME = "geese-on"  # must be unique
MQTT_SUBSCRIBE_TOPIC = "test/ducks"  # main topic: test, sub topic: ducks
MQTT_PUBLISH_TOPIC = "test/geese"  # main topic: test, sub topic: geese

# Instantiate a client object
client = mqtt.Client(MQTT_CLIENT_NAME)

# Connect to the server
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)

# Subscribe to the ducks topic
client.subscribe(MQTT_SUBSCRIBE_TOPIC)


def on_message_callback(client, userdata, message):
    msg = message
    msg_data = str(msg.payload.decode("UTF-8"))  # decode the message payload into UTF-8 characters
    # convert incoming json string into dictionary
    json_data = json.loads(msg_data)

    # You can access keys from the dictionary now
    print(f"Received current temperature: {json_data['temperature']}")

    # get the temperature from the publisher
    temperature = json_data["temperature"]

    # decide if the incoming temp is too hot, cold or just right
    if temperature < 22:
        message_text = "Too cold!"
    elif temperature > 30:
        message_text = "Too hot!"
    else:
        message_text = "Perfect weather!"

    # store the data in a dictionary
    data_to_publish = {'message': message_text,
                       'temperature': temperature
                       }

    # prints out what data is going to be published before making it JSON
    print(data_to_publish)
    data_as_json = json.dumps(data_to_publish)

    # publishes to geese
    client.publish(MQTT_PUBLISH_TOPIC, data_as_json)


# Listen for messages - call the callback function once message is received
client.on_message = on_message_callback
print(f"{MQTT_CLIENT_NAME} is listening on {MQTT_PORT} for messages with the topic {MQTT_SUBSCRIBE_TOPIC}")

client.loop_forever()
