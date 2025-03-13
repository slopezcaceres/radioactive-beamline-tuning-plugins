from badger import environment
from badger.interface import Interface
from badger.factory import get_intf

Interface, configs_caribumatic = get_intf('CARIBUMATIC-K4E5A')
int_caribumatic = Interface(configs_caribumatic['params'])
        

class Environment(environment.Environment):

    name = 'CARIBUMATIC-K4E5A'
        
    variables = {
        'QDK402:CONTROL_X': [0.5, 2],
        'QDK402:CONTROL_Y': [0.5, 2],
        'QTE501_X1:CONTROL': [50, 300],
        'QTE501_X2:CONTROL': [50, 300],
        'QTE501_Y:CONTROL': [50, 300],
        'STE501:CONTROL_X': [-1000, 1000],
        'STE501:CONTROL_Y': [-1000, 1000],
        'STK402:CONTROL_X': [-1, 1],
        'STK402:CONTROL_Y': [-1, 1],
    }
    observables = ['LAUREL_RATEMETER:MONITOR']

    _variables = {
        "QDK402:CONTROL_X": 1.0,
        "QDK402:CONTROL_Y": 1.04,
        "QTE501_X1:CONTROL": 189,
        "QTE501_X2:CONTROL": 158,
        "QTE501_Y:CONTROL": 222,
        "STE501:CONTROL_X": 172,
        "STE501:CONTROL_Y": -270,
        "STK402:CONTROL_X": 0.25,
        "STK402:CONTROL_Y": -0.49      
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

