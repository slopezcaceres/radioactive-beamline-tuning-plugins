from badger import environment
from badger.interface import Interface
from badger.factory import get_intf

Interface, configs_caribumatic = get_intf('CARIBU-matic')
int_caribumatic = Interface(configs_caribumatic['params'])
        

class Environment(environment.Environment):

    name = 'CARIBU-matic'
        
    variables = {
        'STK000:CONTROL_X': [-800, 800],
        'STK000:CONTROL_Y': [-800, 800],
        'QDK001:CONTROL_X': [200, 500],
        'QDK001:CONTROL_Y': [200, 500],
        'STK001:CONTROL_X': [-800, 800],
        'STK001:CONTROL_Y': [-800, 800],
    }
    observables = ['LAUREL_RATEMETER:MONITOR']

    _variables = {
        "STK000:CONTROL_X": 470.0,
        "STK000:CONTROL_Y": 110.0,
        "QDK001:CONTROL_X": 413.0,
        "QDK001:CONTROL_Y": 316.0,
        "STK001:CONTROL_X": -70.0,
        "STK001:CONTROL_Y": -120.0
    }
    # _observations = {
    #     'LAUREL_RATEMETER:MONITOR': 0,
    # } 

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

        # for var, x in variable_inputs.items():
        #     self._variables[var] = x
            
        #     self.interface.set_values(var, x)

        # # Filling up the observations
       # f = self._variables['STK000:CONTROL_X'] ** 2 + self._variables['STK000:CONTROL_Y'] ** 2

        #self._observations['LAUREL_RATEMETER:MONITOR'] = f

    def get_observables(self, observable_names):
        observable_outputs = {obs: self.interface.get_values(obs) for obs in observable_names}
        return observable_outputs

        #observable_names == 'LAUREL_RATEMETER:MONITOR'
        #return {k: self._observations[k] for k in observable_names}
        #return self.interface.get_value('LAUREL_RATEMETER:MONITOR')

