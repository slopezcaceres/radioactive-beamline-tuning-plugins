import requests
import time
import threading

class Interface(interface.Interface):

    name = 'CARIBU-matic'

    half_life_P = 1.687 # s
    half_life_D = 10.51 # m
    half_life_G = 91.8 # m

    def __init__(self, params=None): 
        super().__init__(params=params)
        self.stop_thread = False
        self.old_rate = None
        self.new_rate = 0
        self.old_parameters = None
        self.last_values = {"STK000:CONTROL_X": 0.0,
                            "STK000:CONTROL_Y": 0.0,
                            "QDK001:CONTROL_X": 0.0,
                            "QDK001:CONTROL_Y": 0.0,
                            "STK001:CONTROL_X": 0.0,
                            "STK001:CONTROL_Y": 0.0}  # Initialize with default or previous known values
        self.difference = None
        self.difference_read = False  # Flag to track if difference has been read
        self._start_beam_off_thread()  # Start the beam_off thread when the interface is created

    def get_values(self, input_list):
        key = input_list[0]
        resp_get = requests.get('http://127.0.0.1:5000/', json={"setting": ["LAUREL_RATEMETER:MONITOR"], "fcup": [], "bpm": []})
        resp_json = resp_get.json()
        values = resp_json["setting"]["control"]["LAUREL_RATEMETER:MONITOR"]
        
        # Return the calculated difference if available
        if self.difference is not None:
            self.difference_read = True  # Mark that the difference has been read
            true_rate = self.difference.copy()
            return true_rate * 7 * 10**44
        else:
            background = self.new_rate.copy()
            true_rate = values - background 
            return true_rate * 7 * 10**44

    def set_values(self, post_dict):
        self.last_values = post_dict  # Update last_values with the current post_dict
        resp = requests.post("http://127.0.0.1:5000/", json=post_dict)
        time.sleep(3)

    def beam_off(self):
        while not self.stop_thread:
            # This thread will sleep here for 10 minutes
            time.sleep(half_life_P*3)  # Sleep for 3 half-lives     
            
            # After 3 half-lives, this code runs
            # Step 1: Save the last values from get_values and set_values
            self.old_rate = self.get_values(["LAUREL_RATEMETER:MONITOR"])
            self.old_parameters = self.last_values  # Save the most recent post_dict used

            # Step 2: Post zeros
            beamOff_parameters = self.last_values.copy()
            beamOff_parameters["STK000:CONTROL_X"] = 500  # Change only the first item
            self.set_values(beamOff_parameters)

            # Step 3: Get the new values after beam_off
            time.sleep(half_life_P*1) # Wait 1 half-life 
            self.new_rate = self.get_values(["LAUREL_RATEMETER:MONITOR"]) # Background

            # Step 4: Calculate the difference
            self.difference = self.old_rate - self.new_rate
            self.difference_read = False  # Reset the read flag

            # Wait for the difference to be read
            while not self.difference_read:
                time.sleep(1)  # Check every second

            # Restore the old parameters
            self.set_values(self.old_parameters)

            # Reset the difference to None after processing
            self.difference = None

    def _start_beam_off_thread(self):
        # This starts the beam_off method in a separate thread
        beam_off_thread = threading.Thread(target=self.beam_off)
        beam_off_thread.start()

    def stop_beam_off_thread(self):
        self.stop_thread = True
        beam_off_thread.join()


