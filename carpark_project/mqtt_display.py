import random
import threading
import time
import tkinter as tk
from typing import Iterable
from mqtt_client import create_mqtt_client
import json

class WindowedDisplay:
    """Displays values for a given set of fields as a simple GUI window.
    Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, title: str, display_fields: Iterable[str]):
        """Creates a Windowed (tkinter) display to replace sense_hat display.
        To show the display (blocking) call .show() on the returned object.

        Parameters
        ----------
        title : str
            The title of the window (usually the name of your carpark from the config)
        display_fields : Iterable
            An iterable (usually a list) of field names for the UI.
            Updates to values must be presented in a dictionary with these values as keys.
        """
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):

            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field+self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""
        self.window.mainloop()

    def update(self, updated_values: dict):
        """Update the values displayed in the GUI.
        Expects a dictionary with keys matching the field names passed to the constructor."""
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()


class CarParkDisplay:
    """Provides a simple display of the car park status.
    This is a skeleton only.
    The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self):
        self.temperature = 0
        self.available_bays = 0
        self.time = 0
        self.mqtt_client = create_mqtt_client('Carpark Display')

        # Listen for car updates
        self.mqtt_client.on_message = self.on_message_callback

        # Listen for temp and time updates
        self.mqtt_client.message_callback_add('carpark/temperature', self.on_message_temperature_time)

        self.window = WindowedDisplay(
            'Moondalup', CarParkDisplay.fields)
        updater = threading.Thread(target=self.check_updates)
        updater.daemon = True
        updater.start()
        self.window.show()

    # Method to update car bays
    def on_message_callback(self, client, userdata, msg):
        message = msg.payload.decode()
        # Convert incoming JSON into dictionary
        json_data = json.loads(message)
        # Update number of bays
        self.available_bays = json_data['available_spaces']

    # Method to update temperature and time
    def on_message_temperature_time(self, client, userdata, msg):
        message = msg.payload.decode()
        message = json.loads(message)
        self.temperature = message['temperature']
        self.time = message['time']
        print(message)

    def check_updates(self):
        self.mqtt_client.subscribe('carpark/temperature')
        self.mqtt_client.subscribe('carpark')

        self.mqtt_client.loop_start()
        while True:
            # If there are bays available
            if self.available_bays != 0:

                # NOTE: Dictionary keys *must* be the same as the class fields
                field_values = dict(zip(CarParkDisplay.fields, [
                    self.available_bays,
                    f"{int(self.temperature)}C°",  # Convert incoming float to int
                    self.time]))

                # When you get an update, refresh the display.
                self.window.update(field_values)

            else:  # If there are no bays available

                # NOTE: Dictionary keys *must* be the same as the class fields
                field_values = dict(zip(CarParkDisplay.fields, [
                    "FULL",
                    f"{int(self.temperature)}C°",
                    self.time]))

                # When you get an update, refresh the display.
                self.window.update(field_values)


if __name__ == "__main__":
    display = CarParkDisplay()
    display.mqtt_client.loop_stop()
