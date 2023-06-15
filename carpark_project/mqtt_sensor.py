import tkinter as tk
from mqtt_client import create_mqtt_client
from config_parser import parse_config


class CarDetector:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car.
    This is a skeleton only."""

    def __init__(self, config):
        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")
        self.mqtt_client = create_mqtt_client('Car Sensor')
        self.topic = config["topics"]["sensor"]
        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘',  font=('Arial', 50), cursor='bottom_left_corner',
            command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.root.mainloop()

    def incoming_car(self):
        # Publish 'enter' text to the topic 'sensor'
        self.mqtt_client.publish(self.topic, 'enter')
        # print("Car goes in")

    def outgoing_car(self):
        # Publish 'exit' text to the topic 'sensor'
        self.mqtt_client.publish(self.topic, 'exit')
        # print("Car goes out")


if __name__ == "__main__":
    config = parse_config()
    car_sensor = CarDetector(config)
    car_sensor.mqtt_client.loop_forever()
