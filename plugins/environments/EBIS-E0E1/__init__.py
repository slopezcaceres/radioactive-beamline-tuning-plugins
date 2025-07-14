from badger import environment
from badger.interface import Interface
from badger.factory import get_intf
import json

Interface, configs_caribumatic = get_intf('EBIS-E0E1')
int_caribumatic = Interface(configs_caribumatic['params'])
        
# Load configuration from config_caribu.json
config_path = '/Users/Sergiolopez/Library/Application Support/Badger/plugins/interfaces/config_awacs.json'

with open(config_path, 'r') as file:
    config = json.load(file)

# Extract the desired configuration values for the POST request
# Assuming you want the values under "good_tune" -> "EBIS-E0E1"
raw_init_values = config["good_tune"]["EBIS-E0E1"]

init_values = {
    f"{item['device']}:{item['chan']}": item["val"]
    for item in raw_init_values
}

class Environment(environment.Environment):

    name = 'EBIS-E0E1'
        
    variables = {
        
        'STE002:CONTROL_X': [-1.0, 1.0], #kV
        'STE002:CONTROL_Y': [-1.0, 1.0], #kV
        'EDE001:CONTROL': [4.60, 4.70], #kV
        'EDE002:CONTROL': [3.50, 3.60], #kV
        'QDE101:CONTROL_X': [1.45, 1.85], #kV
        'QDE101:CONTROL_Y': [2.25, 2.75], #kV
        'STE101:CONTROL_X': [-1.0, 1.0], #kV
        'STE101:CONTROL_Y': [-1.0, 1.0], #kV

    }

    observables = ['EBIS_RATEMETER']

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


