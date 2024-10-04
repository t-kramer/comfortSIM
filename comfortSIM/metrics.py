# calculate indices and metrics
import numpy as np


def calculate_spatial_autonomy(comfort_prediction_array, area_threshold=0.8):
    """
    Calculates sTA based on comfort prediction results.

    Args:
        comfort_prediction_array (numpy.ndarray): 2D array containing predictions of spatial thermal preference.
        percentage_area (float, optional): Area threshold for annual sTA calculation; defaults to 0.8.

    Returns:
        comfort_hours (numpy.ndarray): 2D array containing a boolean comfort prediction for each grid point.
        hourly_autonomy (numpy.ndarray): 1D array where each element represents the hourly sTA.
        spatial_autonomy (float): Annual sTA depending on specified area threshold.
    """

    class SpatialAutonomyResult:
        def __init__(self, annual_autonomy, hourly_autonomy, comfort_hours):
            self.annual_autonomy = annual_autonomy
            self.hourly_autonomy = hourly_autonomy
            self.comfort_hours = comfort_hours

    comfortable_points = (abs(comfort_prediction_array) <= 0.5).astype(int)

    hourly_autonomy = (
        np.sum(comfortable_points, axis=0) / comfort_prediction_array.shape[0]
    )

    annual_autonomy = round(
        float(
            np.sum(np.where(hourly_autonomy > area_threshold, 1, 0))
            / comfort_prediction_array.shape[1]
        ),
        2,
    )

    return SpatialAutonomyResult(annual_autonomy, hourly_autonomy, comfortable_points)


def calculate_temperature_range(
    temperature_array, lower_limit: float, upper_limit: float
):
    """
    Calculates the temperature range based on the specified lower and upper limits.

    Args:
        temperature_array (numpy.ndarray): 2D array containing temperature values.
        lower_limit (float): Lower limit of the temperature range.
        upper_limit (float): Upper limit of the temperature range.

        Returns:
        numpy.ndarray: 2D array containing the boolean values indicating if point value is in defined limits.

    """

    conditions = [
        (temperature_array <= lower_limit),
        (temperature_array > lower_limit) & (temperature_array < upper_limit),
        (temperature_array >= upper_limit),
    ]

    values = [-1, 0, 1]

    return np.select(conditions, values)


def calculate_hourly_spatial_heterogeneity(environmental_parameter_array):
    """
    Calculates the hourly spatial heterogeneity based on the environmental parameter array.

    Args:
        environmental_parameter_array (numpy.ndarray): 2D array containing environmental parameter values.

    Returns:
        numpy.ndarray: 1D array containing the hourly spatial heterogeneity values.
    """

    return environmental_parameter_array.max(
        axis=0
    ) - environmental_parameter_array.min(axis=0)


def calculate_annual_point_heterogeneity(environmental_parameter_array):
    """
    Calculates the annual point heterogeneity based on the environmental parameter array.

    Args:
        environmental_parameter_array (numpy.ndarray): 2D array containing environmental parameter values.

    Returns:
        numpy.ndarray: 1D array containing the annual point heterogeneity values.
    """

    return environmental_parameter_array.max(
        axis=1
    ) - environmental_parameter_array.min(axis=1)


def calculate_thi_area(environmental_parameter_array):
    """
    Calculates the THI area based on the environmental parameter array.

    Args:
        environmental_parameter_array (numpy.ndarray): 2D array containing environmental parameter values.

    Returns:
        float: THI area value.
    """

    return round(np.median(np.ptp(environmental_parameter_array, axis=0)), 2)


def calculate_thi_point(environmental_parameter_array):
    """
    Calculates the THI point based on the environmental parameter array.

    Args:
        environmental_parameter_array (numpy.ndarray): 2D array containing environmental parameter values.

    Returns:
        float: THI point value.
    """

    return round(np.median(np.ptp(environmental_parameter_array, axis=1)), 1)
