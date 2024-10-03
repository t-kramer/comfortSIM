# utility functions
import numpy as np


def filter_by_schedule(array):
    """
    Filters the input array by a typical schedule.

    Args:
        array (numpy.ndarray): 1D array containing values to be filtered.

    Returns:
        numpy.ndarray: 1D array containing the values filtered by the schedule.
    """

    schedule_workingday = np.array(
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    )
    schedule_weekendday = np.array(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    schedule_workingweek = np.tile(schedule_workingday, 5)
    schedule_weekend = np.tile(schedule_weekendday, 2)
    schedule_weekly = np.concatenate([schedule_workingweek, schedule_weekend])

    schedule_yearly = np.concatenate(
        [schedule_workingday, np.tile(schedule_weekly, 52)]
    )

    boolean_filter = schedule_yearly.astype(bool)

    return array[boolean_filter]
