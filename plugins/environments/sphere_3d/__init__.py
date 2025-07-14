from badger import environment


class Environment(environment.Environment):

    name = 'sphere_3d'  # name of the environment
    variables = {  # variables and their hard-limited ranges
        'x0': [-1, 1],
        'x1': [-1, 1],
        'x2': [-1, 1],
    }
    observables = ['f']  # measurements

    # Internal variables to store the current values of
    # the variables and observables
    _variables = {
        'x0': 1.0,
        'x1': 2.0,
        'x2': 3.0,
    }
    _observations = {
        'f': None,
    }

    # Variable getter -- tells Badger how to get current values of the variables
    def get_variables(self, variable_names):
        variable_outputs = {v: self._variables[v] for v in variable_names}

        return variable_outputs

    # Variable setter -- how to set variables to the given values
    def set_variables(self, variable_inputs: dict[str, float]):
        for var, x in variable_inputs.items():
            self._variables[var] = x

        # Filling up the observations
        f = self._variables['x0'] ** 2 + self._variables['x1'] ** 2 + \
            self._variables['x2'] ** 2

        self._observations['f'] = [f]

    # Observable getter -- how to get current values of the observables
    def get_observables(self, observable_names):
        return {k: self._observations[k] for k in observable_names}