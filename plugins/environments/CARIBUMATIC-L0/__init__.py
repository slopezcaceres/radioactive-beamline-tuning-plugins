from badger import environment
from badger.interface import Interface
from badger.factory import get_intf
import json

Interface, configs_caribumatic = get_intf('CARIBUMATIC-L0')
int_caribumatic = Interface(configs_caribumatic['params'])
 
# Load configuration from config_caribu.json
config_path = '/Users/slopezcaceres/Library/Application Support/Badger/plugins/interfaces/config_awacs.json'

with open(config_path, 'r') as file:
    config = json.load(file)

# Extract the desired configuration values for the POST request
# Assuming you want the values under "good_tune" -> "L0"
raw_init_values = config["good_tune"]["L0"]

init_values = {
    f"{item['device']}:{item['chan']}": item["val"]
    for item in raw_init_values
}


class Environment(environment.Environment):

    name = 'CARIBUMATIC-L0'
        
    variables = {
        'QTL001:CONTROL_X1': [500, 1000],
        'QTL001:CONTROL_X2': [500, 1000],
        'QTL001:CONTROL_Y': [500, 2000],
        'STL001:CONTROL_X': [-1000, 1000],
        'STL001:CONTROL_Y': [-1000, 1000],
        'STL002:CONTROL_X': [-1000, 1000],
        'STL002:CONTROL_Y': [-1000, 1000],
    }
    observables = ['LAUREL_RATEMETER:MONITOR']

    _variables = init_values

    def __init__(self, interface : Interface , params: dict):
        super().__init__(interface = int_caribumatic, params = configs_caribumatic['params'])
        self.interface = int_caribumatic
        self.params = configs_caribumatic['params']
        self.interface.environment = self  # Pass the environment instance to the interface to get the STK000:CONTROL_X limits

    def get_variables(self, variable_names):
        variable_outputs = {v: self._variables[v] for v in variable_names}
        return variable_outputs

    def set_variables(self, variable_inputs: dict[str, float]):
        self.interface.set_values(variable_inputs)

    def get_observables(self, observable_names):
        observable_outputs = {obs: self.interface.get_values(obs) for obs in observable_names}
        return observable_outputs


