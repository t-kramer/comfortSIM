import numpy as np


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
