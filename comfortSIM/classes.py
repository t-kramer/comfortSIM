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
        data = np.genfromtxt(csv_file, delimiter=",").round(2)

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
    def __init__(self, environment):
        """Initialize the Comfort base class with an Environment instance."""
        self.environment = environment
        self.comfort_prediction = None  # To store the calculated comfort index
        self.index = None  # This will be set in the child classes

    def calculate_spatial_autonomy(self, area_threshold=0.8):
        """Calculate spatial autonomy based on comfort predictions."""

        if self.comfort_prediction is None:
            raise ValueError("Comfort prediction has not been calculated yet.")

        comfort_prediction_array = self.comfort_prediction

        comfortable_points = (abs(comfort_prediction_array) <= 0.5).astype(int)

        hourly_autonomy = np.mean(comfortable_points, axis=0)
        annual_autonomy = round(np.mean(hourly_autonomy > area_threshold), 2)

        return self.SpatialAutonomyResult(
            annual_autonomy, hourly_autonomy, comfortable_points
        )

    class SpatialAutonomyResult:
        """Inner class to store spatial autonomy results."""

        def __init__(self, annual_autonomy, hourly_autonomy, comfort_hours):
            self.annual_autonomy = float(annual_autonomy)
            self.hourly_autonomy = hourly_autonomy
            self.comfort_hours = comfort_hours

    def get_comfort_index(self):
        """Get the stored comfort index array."""
        if self.comfort_prediction is not None:
            return self.comfort_prediction
        else:
            raise ValueError("Comfort index has not been calculated yet.")

    def list_comfort_factors(self):
        """List all factors used for calculating comfort."""
        return self.environment.list_parameters()


class PMV(Comfort):
    def __init__(self, environment):
        """Initialize the PMVComfort class with an Environment instance."""
        super().__init__(environment)  # nherit from Comfort class
        self.index = "PMV"  # Set the index name

    def calculate_comfort_index(self, continuous=False):
        """Calculate the PMV thermal comfort index."""
        # Set fixed values for now
        air_velocity = 0.1  # m/s
        clothing_level = 0.8  # Clo
        metabolic_rate = 1.1  # MET

        vr = v_relative(v=air_velocity, met=metabolic_rate)

        pmv_array = pmv_ppd(
            tdb=self.environment.get_parameter("air_temperature"),
            tr=self.environment.get_parameter("mean_radiant_temperature"),
            vr=vr,
            rh=self.environment.get_parameter("relative_humidity"),
            met=metabolic_rate,
            clo=clothing_level,
            limit_inputs=False,
        )["pmv"]

        # discrete PMV values
        if continuous == False:

            choices = [1, -1, 0]

            pmvConditions = [
                pmv_array > 0.5,
                pmv_array < -0.5,
                (pmv_array >= -0.5) & (pmv_array <= 0.5),
            ]
            pmv_values = np.select(pmvConditions, choices, default=pmv_array)

        else:
            pmv_values = pmv_array

        self.comfort_prediction = pmv_values

        return pmv_values


class AdaptiveComfort(Comfort):
    def __init__(self, environment):
        """Initialize the AdaptiveComfort class with an Environment instance."""
        super().__init__(environment)
        self.index = "Adaptive"  # Set the index name

    def calculate_comfort_index(self):
        """Calculate the adaptive comfort index."""
        pass
