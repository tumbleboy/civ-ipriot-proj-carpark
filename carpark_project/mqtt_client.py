import paho.mqtt.client as mqtt
from config_parser import parse_config


def create_mqtt_client(name):
    config = parse_config()
    client = mqtt.Client(name)
    client.connect(config['broker']['host'], config['broker']['port'], config['broker']['keep_alive'])
    print("connected successfully")
    return client
