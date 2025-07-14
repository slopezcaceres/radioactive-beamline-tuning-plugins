from badger import interface
import requests       
import pandas as pd
import os
from random import random
import time


class Interface(interface.Interface):
    
    name = 'myintf'
    
        def __init__(self, **data): 
            super().__init__(**data)

        self._states = {}
    
    def get_values(self, channel_names):
        channel_outputs = {}
        
        for channel in channel_names:
            try:
                value = self._states[channel]
            except KeyError:
                self._states[channel] = value = 0

            channel_outputs[channel] = value

        return channel_outputs

    def set_values(self, channel_inputs: dict):
        pass