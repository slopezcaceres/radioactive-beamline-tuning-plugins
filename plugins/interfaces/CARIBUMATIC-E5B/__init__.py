from badger import interface
import requests
import time
import json

class Interface(interface.Interface):
    name = 'CARIBUMATIC-E5B'

    def __init__(self, params=None):
        super().__init__(params=params)
        self.last_values = {
            "QTE502_X1:CONTROL": 0.0,
            "QTE502_X2:CONTROL": 0.0,
            "QTE502_Y:CONTROL": 0.0,
            "STE502_X:CONTROL": 0.0,
            "STE502_Y:CONTROL": 0.0,
            "STE503_X:CONTROL": 0.0,
            "STE503_Y:CONTROL": 0.0
        }  # Initialize with default or zeroes

        self.first_get_values_called = False
        self.max_true_rate = None
        self.best_post_dict = None

    def set_values(self, post_dict):
        awacsSet = []

        for key, val in post_dict.items():
            device, chan = key.split(":", 1)  # split into device and CONTROL_*
            awacsSet.append({
                "device": device,
                "chan": chan,
                "val": val
            })
        self.last_values = awacsSet
        requests.post("http://127.0.0.1:5000/", json=awacsSet)
        time.sleep(5)

    def get_values(self, input_list):
        awacsRatemeter=[{"device":input_list, "chan":"READ"},]
        resp_get = requests.get('http://127.0.0.1:5000/', json=awacsRatemeter)
        true_rate = resp_get.json()["data"][0]["val"]

        # Convert true_rate to float if it's an integer
        if isinstance(true_rate, int):
            true_rate = float(true_rate)

        # Optionally, round the float to a specific precision if needed
        true_rate = round(true_rate, 2)  # Example: round to 2 decimal places

        print(f"true_rate value: {true_rate}")

        if self.max_true_rate is None or true_rate > self.max_true_rate:
            self.max_true_rate = true_rate
            self.best_post_dict = self.last_values.copy()
            self._update_json_config()
            print(f"New maximum rate found: {self.max_true_rate}. Updated config file.")

        return true_rate

    def _update_json_config(self):
        config_path = "/Users/Sergiolopez/Library/Application Support/Badger/plugins/interfaces/config_awacs.json"
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)

            config['good_tune']['E5B'] = self.best_post_dict

            with open(config_path, 'w') as file:
                json.dump(config, file, indent=4)

            print("Updated config file with new best parameters.")
        except Exception as e:
            print(f"Error updating config file: {e}")
