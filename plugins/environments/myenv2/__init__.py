import numpy as np
from badger import environment
from fwhm import calculate_fwhm


class Environment(environment.Environment):

    name = 'myenv'
        
    variables = {
        'x': [0, 10],
        'y': [0, 10],
        'z': [0, 10],
    }
    observables = ['norm', 'mean']

    # Internal variables start with a single underscore
    _variables = {
        'x': 3,
        'y': 2,
        'z': 5,
    }

    def get_variables(self, variable_names: list[str]) -> dict:
       
        file_path = '/Users/slopezcaceres/Library/Application Support/Badger/plugins/interfaces/config_awacs.json' # Path to hist.dat
        try:
            counts = np.loadtxt(file_path)
            print(f"Loaded {len(counts)} bins from {file_path}")
            fwhm = calculate_fwhm(counts, plot=plot)
            if fwhm is not None:
                print(f"FWHM: {fwhm:.2f} bins")
            else:
                print("FWHM could not be calculated.")
            return fwhm
        except Exception as e:
            print(f"Error: {e}")
            return None


        variable_outputs = {v: self._variables[v] for v in variable_names}

        return variable_outputs

    def set_variables(self, variable_inputs: dict[str, float]):
        for var, x in variable_inputs.items():
            self._variables[var] = x

    def get_observables(self, observable_names: list[str]) -> dict:
        x = self._variables['x']
        y = self._variables['y']
        z = self._variables['z']

        observable_outputs = {}
        for obs in observable_names:
            if obs == 'norm':
                observable_outputs[obs] = (x ** 2 + y ** 2 + z ** 2) ** 0.5
            elif obs == 'mean':
                observable_outputs[obs] = (x + y + z) / 3

        return observable_outputs