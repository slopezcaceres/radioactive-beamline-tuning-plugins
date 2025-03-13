from badger import interface
import requests       
import pandas as pd
import os
from random import random
import time
import json
import threading

class Interface(interface.Interface):

    name = 'CARIBUMATIC-K1B'

    def __init__(self, params=None): 
        super().__init__(params=params)
        self.half_life_P = 6.05  # s for mass 142
        self.half_life_D = 10.51 * 60  # Convert to seconds
        self.half_life_G = 91.8 * 60  # Convert to seconds
        self.stop_thread = False
        self.old_rate = None
        self.new_rate = None
        self.old_parameters = None
        self.difference = None
        self.difference_read = False  # Flag to track if difference has been read
        self.main_thread_set_values_executed = False  # Flag to track if set_values has been executed by the main thread
        self.first_get_values_called = False # Flag to track if get_values has been called
        self.main_thread_pause_executed = False  # Flag to track if the pause has been executed by the main thread
        self._beam_off_thread = None # Initialize thread attribute
        self._condition = threading.Condition()  # Initialize condition variable
        self._pause_main_thread_event = threading.Event()  # Event to control the main thread
        self._resume_main_thread_event = threading.Event()  # Event to resume the main thread
        self.last_values = {        'EDK101:CONTROL': 0.0,
                                    'EDK102:CONTROL': 0.0}  # Initialize with default or zeroes

    def set_values(self, post_dict):
    #with self._condition:    
        self.last_values = post_dict  # Update last_values with the current post_dict
        print(f"1-setting values main thread")
        resp = requests.post("http://127.0.0.1:5000/", json=post_dict)
        #self.main_thread_set_values_executed = True # Indicate that set_values was executed in the main thread
        #self._condition.notify_all()  # Notify the background thread to proceed
        time.sleep(5)
    

    def get_values(self, input_list):
        if not self.first_get_values_called:
            self.first_get_values_called = True
            #self._start_beam_off_thread()  # Start the thread after the first get_values call
        
    #with self._condition:
        # The main thread checks if it should pause
        if self._pause_main_thread_event.is_set():
            print("Pausing main thread, waiting for background thread to finish...")
            self._pause_main_thread_event.clear()  # Clear the event to allow future pauses
            #self.main_thread_pause_executed = True # Indicate that main thread has been paused
            #self._condition.notify_all() # Notify the background thread to proceed
            self._resume_main_thread_event.wait()  # Wait until the background thread signals to resume
            self._resume_main_thread_event.clear()  # Clear the resume event for future use

        input_list = [input_list]
        key = input_list[0]
        #print(f"Key being used: {key}")
        resp_get = requests.get('http://127.0.0.1:5000/', json={"setting": [key], "fcup": [], "bpm": []})
        print(f"2-getting main thread rate")
        #print(f"Response: {resp_get.status_code}, {resp_get.text}")
        resp_json = resp_get.json()
        values = resp_json["setting"]["control"][key]
        
        # Return the calculated difference if available
        if self.difference is not None:
            self.difference_read = True  # Mark that the difference has been read
            true_rate = self.difference
            self.difference = None
            print(f"2.1-true_rate 1 value: {true_rate}")
            return true_rate
        else:
            self.new_rate = 0
            background = self.new_rate
            print(f"2.1-background value: {background}")
            true_rate = values - background 
            print(f"2.2-true_rate 2 value: {true_rate * 7 * 10**44}")
            true_rate *= 7 * 10**44

        # Check if this is the maximum true_rate and update if necessary
        if self.max_true_rate is None or true_rate > self.max_true_rate:
            self.max_true_rate = true_rate
            self.best_post_dict = self.last_values.copy()  # Save the corresponding post_dict
            self._update_json_config()  # Update the JSON file
            print(f"New maximum rate found: {self.max_true_rate}. Updated config file.")

        return true_rate

    def _set_values_internal(self, post_dict):
        """Internal method for setting values within the background thread."""
        resp = requests.post("http://127.0.0.1:5000/", json=post_dict)
        time.sleep(3)  # Simulate delay if needed

    def _get_values_internal(self, input_list):
        """Internal method for getting values within the background thread."""
        #input_list = [input_list]
        key = input_list[0]
        print(f"Key internal being used: {key}")        
        resp_get = requests.get('http://127.0.0.1:5000/', json={"setting": [key], "fcup": [], "bpm": []})
        resp_json = resp_get.json()
        values = resp_json["setting"]["control"][key]
        
        return values * 7 * 10**44
        
    def beam_off(self):
        while not self.stop_thread:
            # This thread will sleep here for a few half-lives
            #time.sleep(self.half_life_P * 50)  # Sleep for a few half-lives     
            time.sleep(1200)  # Sleep for five minutes. This gives time to the optimizer to increase the beam rate.    
            print(f"3-background thread kicking in")
            
            # Signal the main thread to pause
            self._pause_main_thread_event.set()

            #self.main_thread_pause_executed = False  # Reset the flag for the next iteration

            # Step 1: Save the last values from get_values and set_values
            key = "LAUREL_RATEMETER:MONITOR"
            self.old_rate = self._get_values_internal([key])
            print(f"4-getting old rate (background thread): {self.old_rate}")
            self.old_parameters = self.last_values  # Save the most recent post_dict used

            # Step 2: Post beamOff parameters
            beamOff_parameters = self.last_values.copy()
            control_x_value = beamOff_parameters["STK000:CONTROL_X"]
            
            # Retrieve limits directly from the environment variables
            lower_limit, upper_limit = self.environment.variables['STK000:CONTROL_X']
            print(f"5-retriving limits: {lower_limit} - {upper_limit}")
            # Apply the logic to keep control_x_value within the range [-800, 800]
            if control_x_value + 600 > upper_limit:
                beamOff_parameters["STK000:CONTROL_X"] -= 600
            elif control_x_value - 600 < lower_limit:
                beamOff_parameters["STK000:CONTROL_X"] += 600
            else:
                beamOff_parameters["STK000:CONTROL_X"] += 600  # Add 500 if it's within the range

            print(f"6-setting beam off parameters")
            self._set_values_internal(beamOff_parameters)
            time.sleep(10)
            # Step 3: Get the new values after beam_off
            #time.sleep(self.half_life_P * 5) # Wait 5 half-lives
            self.new_rate = self._get_values_internal([key]) # Background
            print(f"7-getting background rate background thread")
            # Step 4: Calculate the difference
            print(f"Old rate: {self.old_rate}, Background rate: {self.new_rate}")
            self.difference = self.old_rate - self.new_rate
            print(f"8-Calculated difference: {self.difference}")
            
            # If the difference is not positive, sleep for 3 half_life_P and then recalculate
            while self.difference <= 0:
                print(f"9.1-Difference is not positive. Sleeping for {self.half_life_P * 2} seconds.")
                time.sleep(self.half_life_P * 3)
                # Recalculate the new rate and difference
                self.new_rate = self._get_values_internal([key])
                print(f"9.2-remeasuring after sleeping background thread, Background rate: {self.new_rate}")
                self.difference = self.old_rate - self.new_rate
                print(f"9.3-Recalculated difference: {self.difference}")

            self.difference_read = False  # Reset the read flag

            # Restore the old parameters
            print(f"9-setting old_parameters") 
            self._set_values_internal(self.old_parameters)
            time.sleep(5)
            # Signal the main thread to resume
            self._resume_main_thread_event.set()

    def _start_beam_off_thread(self):
        # This starts the beam_off method in a separate thread
        self._beam_off_thread = threading.Thread(target=self.beam_off)
        self._beam_off_thread.daemon = True  # Set the thread as a daemon
        self._beam_off_thread.start()

    def stop_beam_off_thread(self):
        # This stops the beam_off thread
        self.stop_thread = True
        if self._beam_off_thread is not None:
            self._beam_off_thread.join()

    def _update_json_config(self):
        config_path = "/Users/Sergiolopez/Library/Application Support/Badger/plugins/interfaces/config_caribu.json"  # Adjust this path as needed
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            
            # Update the "good_tune" -> "K1B" entry with the best post_dict
            config['good_tune']['K1B'] = self.best_post_dict
            
            with open(config_path, 'w') as file:
                json.dump(config, file, indent=4)
            
            print(f"Updated config file with new best parameters.")
        
        except Exception as e:
            print(f"Error updating config file: {e}")




