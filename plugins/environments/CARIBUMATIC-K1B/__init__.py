from badger import environment
from badger.interface import Interface
from badger.factory import get_intf
import json

Interface, configs_caribumatic = get_intf('CARIBUMATIC-K1B')
int_caribumatic = Interface(configs_caribumatic['params'])

# Load configuration from config_caribu.json
config_path = '/Users/Sergiolopez/Library/Application Support/Badger/plugins/interfaces/config_caribu.json'

with open(config_path, 'r') as file:
    config = json.load(file)

# Extract the desired configuration values for the POST request
# Assuming you want the values under "good_tune" -> "K1B"
init_values = config["good_tune"]["K1B"]
        

class Environment(environment.Environment):

    name = 'CARIBUMATIC-K1B'
        
    limit = {
        'STK000:CONTROL_X': [-800,800]
    }

    variables = {
        'EDK101:CONTROL': [4300, 4700],
        'EDK102:CONTROL': [4300, 4700],
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


