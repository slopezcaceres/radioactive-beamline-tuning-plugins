from badger import environment
from badger.interface import Interface
from badger.factory import get_intf

Interface, configs_caribumatic = get_intf('CARIBUMATIC-E5B')
int_caribumatic = Interface(configs_caribumatic['params'])
        

class Environment(environment.Environment):

    name = 'CARIBUMATIC-E5B'
        
    variables = {
        'QTE502_X1:CONTROL': [50, 300],
        'QTE502_X2:CONTROL': [50, 300],
        'QTE502_Y:CONTROL': [50, 300],
        'STE502_X:CONTROL': [-500, 500],
        'STE502_Y:CONTROL': [-500, 500],
        'STE503_X:CONTROL': [-500, 500],
        'STE503_Y:CONTROL': [-500, 500]
    }
    observables = ['LAUREL_RATEMETER:MONITOR']

    _variables = {
                "QTE502_X1:CONTROL": 128,
                "QTE502_X2:CONTROL": 135,
                "QTE502_Y:CONTROL": 177,
                "STE502_X:CONTROL": -120,
                "STE502_Y:CONTROL": -60,
                "STE503_X:CONTROL": 0,
                "STE503_Y:CONTROL": 57}
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

