from config_parser import parse_config
from mqtt_client import create_mqtt_client
import datetime
from random import uniform
import json
import time
import threading

class CarPark:
    def __init__(self, config):
        self.config = config
        self.location = config['carpark']["location"]
        self.total_cars = 0
        self.total_spaces = config['carpark']['total_spaces']

        # Set all spaces to be available
        self.available_spaces = self.total_spaces

        # Create mqtt client
        self.mqtt_client = create_mqtt_client(config['carpark']['name'])
        self.mqtt_client.on_message = self.on_message_callback
        self.mqtt_client.subscribe('sensor')

        # Initialize default values on the display
        self.publish_data()
        # self.publish_temperature()

        self.mqtt_client.loop_start()

    def publish_data(self):
        # Simulate Temperature
        temperature = uniform(15, 35)

        # Capture the current time of entry/exit
        now = datetime.datetime.now().strftime("%H:%M:%S")

        # Create dictionary of current data
        message_data = {
            "temperature": temperature,
            "datetime": now,
            "available_spaces": self.available_spaces

        }

        # convert the message_data dictionary into json string, then publish to MQTT
        message_to_send = json.dumps(message_data)
        self.mqtt_client.publish('carpark', message_to_send)

    def detect_car_entry(self):

        # If there are spaces left
        if self.available_spaces != 0:
            self.total_cars += 1
            self.available_spaces -= 1
            print("Car entered!")
            print(f"Total cars: {self.total_cars}")
            print(f"Bays left: {self.available_spaces}")
            print("-----------------------")
            # Publish the amount of bays left to MQTT.
            self.publish_data()
        else:
            # No spaces left
            print("There are no more bays!")

    def detect_car_exit(self):
        # If there are still cars left
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
            # No cars left
            print("There are no cars left in the carpark!")

    def on_message_callback(self, client, userdata, msg):
        message = msg.payload.decode()
        # Detect entry
        if message == 'enter':
            self.detect_car_entry()

        # Detect exit
        elif message == 'exit':
            self.detect_car_exit()

    def publish_temperature_time(self):
        while True:
            temperature_time = {'temperature': uniform(15, 30),
                                'time': datetime.datetime.now().strftime("%H:%M:%S")}
            message = json.dumps(temperature_time)
            self.mqtt_client.publish('carpark/temperature', message)

            # Use threading to not block the program
            event = threading.Event()

            # Wait 6 seconds to simulate time and weather change
            event.wait(6)


if __name__ == '__main__':
    config = parse_config()
    parking_lot = CarPark(config)
    parking_lot.publish_temperature_time()
    parking_lot.mqtt_client.loop_stop()
