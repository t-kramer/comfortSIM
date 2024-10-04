import numpy as np

from pythermalcomfort.models import pmv_ppd
from pythermalcomfort.utilities import v_relative


class Environment:
    def __init__(self):
        self.shape = None  # Shape will be set after the first parameter is loaded
        self.parameters = {}  # Dictionary to store environmental parameters
        self.env_matrix = None  # 3D array to store all environmental parameter data

    def load_parameter(self, param_name, csv_file):
        """Load data for a specific parameter from a CSV file into the environment."""
        data = np.genfromtxt(csv_file, delimiter=",")

        if self.shape is None:
            # Set the shape based on the first parameter loaded
            self.shape = data.shape
            print(f"Shape set to {self.shape} based on {param_name}")
        elif data.shape != self.shape:
            raise ValueError(
                f"Data shape {data.shape} does not match the environment shape {self.shape}."
            )

        self.parameters[param_name] = data

        self.update_env_matrix(data)

    def update_env_matrix(self, data):
        """Private method to update the multidimensional array with new parameter data."""
        if self.env_matrix is None:
            # If it's the first parameter, initialize the 3D array
            self.env_matrix = np.expand_dims(data, axis=0)
        else:
            # Stack new parameter data along the first dimension (axis 0)
            self.env_matrix = np.vstack([self.env_matrix, np.expand_dims(data, axis=0)])

    def get_parameter(self, param_name):
        """Get the data for a specific parameter."""
        if param_name in self.parameters:
            return self.parameters[param_name]
        else:
            raise KeyError(f"Parameter {param_name} not found in the environment.")

    def set_parameter(self, param_name, data):
        """Set or update data for a specific parameter."""
        if self.shape is None:
            self.shape = data.shape
        elif data.shape != self.shape:
            raise ValueError(
                f"Data shape {data.shape} does not match the environment shape {self.shape}."
            )

        self.parameters[param_name] = data

        self.update_env_matrix(data)

    def list_parameters(self):
        """List all parameters currently loaded."""
        return list(self.parameters.keys())


class Comfort:
    def __init__(self, environment, index=None):
        """Initialize Comfort class with an Environment instance."""
        self.environment = environment
        self.comfort_prediction = None
        self.index = index

    def _calculate_pmv(self):
        """Calculate thermal comfort based on environmental data."""
        # set fixed values for now
        air_velocity = 0.1  # m/s
        clothing_level = 0.5  # Clo
        metabolic_rate = 1.2  # MET

        vr = v_relative(v=air_velocity, met=metabolic_rate)

        pmv_values = pmv_ppd(
            tdb=self.environment.get_parameter("air_temperature"),
            tr=self.environment.get_parameter("mean_radiant_temperature"),
            vr=vr,  # needs to be fixed
            rh=self.environment.get_parameter("relative_humidity"),
            met=metabolic_rate,
            clo=clothing_level,
        )["pmv"]

        self.comfort_prediction = pmv_values
        self.index = "PMV"

        return pmv_values

    def _calculate_adaptive(self):
        pass

    def calculate_comfort_index(self):
        """Dynamically calculate the comfort index based on the 'index' argument."""
        if self.index == "PMV":
            return self._calculate_pmv()
        if self.index == "Adaptive":
            return self._calculate_adaptive()
        else:
            raise ValueError(f"Unsupported comfort index provided.")

    def get_comfort_index(self):
        """Get the stored comfort index array."""
        if self.comfort_prediction is not None:
            return self.comfort_prediction
        else:
            raise ValueError("Comfort index has not been calculated yet.")

    def list_comfort_factors(self):
        """List all factors used for calculating comfort."""
        return self.environment.list_parameters()
