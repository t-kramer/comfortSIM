import numpy as np
import pandas as pd
import json


def export_results(simulation_results, export_format, file_name):
    """
    Export prediction results as matrix, structured CSV or JSON.

    Parameters:
    ----------
    simulation_results : pandas.DataFrame or numpy.ndarray
        The simulation results to export.
    export_format : str
        The format to export the results in. Can be 'matrix', 'csv', or 'json'.
    file_name : str
        The name of the file to export the results to.

    Returns:
    -------
    None
    """

    if export_format == 'matrix':
        # Assuming simulation_results is a numpy array
        np.savetxt(file_name, simulation_results)
    elif export_format == 'csv':
        # Assuming simulation_results is a pandas DataFrame
        simulation_results.to_csv(file_name, index=False)
    elif export_format == 'json':
        # Assuming simulation_results is a pandas DataFrame
        simulation_results.to_json(file_name, orient='records')
    else:
        print(f"Unsupported export format: {export_format}")