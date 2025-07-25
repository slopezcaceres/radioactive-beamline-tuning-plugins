from badger import environment
from typing import Optional 
from pydantic import Field

class Environment(environment.Environment):
    name = "DUMMY_SECTION4"

    peak_x:Optional[float]=Field(default=300.0, description='maximum value of x')
    peak_y:Optional[float]=Field(default=300.0, description='maximum value of y')
    peak_rate:Optional[float]=Field(default=270.0, description='maximum value of rate')

    variables = {
        "QDK001:CONTROL_X": [200, 500],
        "QDK001:CONTROL_Y": [200, 500],
    }

    observables = ["LAUREL_RATEMETER"]

    _variables = {
        "QDK001:CONTROL_X": 300.0,
        "QDK001:CONTROL_Y": 300.0,
    }

    def __init__(self, interface=None, params=None,**kwargs):
        super().__init__(interface=None, params=params, **kwargs)

    def set_variables(self, variable_inputs):
        self._variables.update(variable_inputs)

    def get_variables(self, variable_names):
        return {k: self._variables[k] for k in variable_names}

    def get_observables(self, observable_names):
        x = self._variables["QDK001:CONTROL_X"]
        y = self._variables["QDK001:CONTROL_Y"]

        rate = -((x - self.peak_x) ** 2 + (y - self.peak_y) ** 2) / 10000 + self.peak_rate

        return {observable_names[0]: round(rate, 2)}
