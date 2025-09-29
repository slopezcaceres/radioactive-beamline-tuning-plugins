from badger import environment
from typing import Optional 
from pydantic import Field

class Environment(environment.Environment):
    name = "dummy_section1"

    peak_x:Optional[float]=Field(default=350.0, description='maximum value of x')
    peak_y:Optional[float]=Field(default=350.0, description='maximum value of y')
    peak_rate:Optional[float]=Field(default=1200.0, description='maximum value of rate')

    variables = {
        "QDK001:CONTROL_X": [10, 1000],
        "QDK001:CONTROL_Y": [10, 1000],
    }

    observables = ["LAUREL_RATEMETER"]

    _variables = {
        "QDK001:CONTROL_X": 100.0,
        "QDK001:CONTROL_Y": 100.0,
    }

    def set_variables(self, variable_inputs):
        self._variables.update(variable_inputs)

    def get_variables(self, variable_names):
        return {k: self._variables[k] for k in variable_names}

    def get_observables(self, observable_names):
        x = self._variables["QDK001:CONTROL_X"]
        y = self._variables["QDK001:CONTROL_Y"]

        rate = -((x - self.peak_x) ** 2 + (y - self.peak_y) ** 2) / 10000 + self.peak_rate

        return {observable_names[0]: round(rate, 2)}
