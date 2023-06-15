from config_parser import parse_config
from mqtt_client import create_mqtt_client
import datetime
from random import uniform
import json
import time


class CarPark:
    def __init__(self, config):
        self.config = config
        self.location = config['carpark']["location"]
        self.total_cars = 0
        self.total_spaces = config['carpark']['total_spaces']

        # Begin with the number of available spaces to be the total spaces
        self.available_spaces = self.total_spaces
        self.mqtt_client = create_mqtt_client(config['carpark']['name'])
        self.mqtt_client.on_message = self.on_message_callback
        self.mqtt_client.subscribe('sensor')

        # Initialize default values on the display
        self.publish_data()

        self.mqtt_client.loop_forever()

    def publish_data(self):
        temperature = uniform(15, 35)
        now = datetime.datetime.now().strftime("%H:%M:%S")
        message_data = {
            "temperature": temperature,
            "datetime": now,
            "available_spaces": self.available_spaces

        }
        # convert the message_data dictionary into json string
        message_to_send = json.dumps(message_data)
        self.mqtt_client.publish('carpark', message_to_send)

    def detect_car_entry(self):
        if self.available_spaces != 0:
            self.total_cars += 1
            self.available_spaces -= 1
            print("Car entered!")
            print(f"Total cars: {self.total_cars}")
            print(f"Bays left: {self.available_spaces}")
            print("-----------------------")
            # Publish the amount of bays left.
            self.publish_data()
        else:
            print("There are no more bays!")

    def detect_car_exit(self):
        if self.total_cars != 0:
            self.total_cars -= 1
            self.available_spaces += 1
            print("Car exited!")
            print(f"Total cars: {self.total_cars}")
            print(f"Bays left: {self.available_spaces}")
            print("-----------------------")
            # Publish the amount of bays left.
            self.publish_data()
        else:
            print("There are no cars left in the carpark!")

    def on_message_callback(self, client, userdata, msg):
        message = msg.payload.decode()
        # Detect entry
        if message == 'enter':
            self.detect_car_entry()

        # Detect exit
        elif message == 'exit':
            self.detect_car_exit()


if __name__ == '__main__':
    config = parse_config()
    parking_lot = CarPark(config)
