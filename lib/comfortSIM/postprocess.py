# This file contains the post-processing functions for the comfortSIM package.

import numpy as np

def predict_spatial_thermal_preference(offsetArrays, environmentalArray, predictionModel):
    """
    Predicts spatial thermal preference based on environmental variables and offset arrays.

    Args:
        offsetArrays (numpy.ndarray): _description_
        environmentalArray (numpy.ndarray): _description_
        predictionModel (sklearn.BaseEstimator): _description_

    Returns:
        combinedPrediction (numpy.ndarray): _description_
    """
    
    ta, rh, tr, vel = np.split(environmentalArray, 4, axis=0)

    predictionArrays = [] # list to store the prediction arrays for each offset class

    # loop through offset arrays
    for offsetArray in offsetArrays:

        flattenedSimResults = np.vstack((ta.flatten(), rh.flatten(), tr.flatten(), vel.flatten(), offsetArray.flatten()))
        inputDf = pd.DataFrame(flattenedSimResults.transpose(), columns=['ta','rh','tr','vel','ts_offset_class']).round(1)

        y_proba = predictionModel.predict_proba(inputDf)
        predictionArrays.append(-y_proba[:,0] + y_proba[:,-1])

    # combining the prediction arrays for each offset class
    combinedPrediction = np.array(predictionArrays)

    return combinedPrediction



def compute_sta(prediction_array, percentage_area=0.5):
    """
    Computes sTA based on simulated indoor environmental data.

    Args:
        prediction_array (numpy.ndarray): 2D array containing predictions of spatial thermal preference.
        percentage_area (float, optional): Percentage of area threshold for sTA; defaults to 0.5.

    Returns:
        comfort_hours (numpy.ndarray): 2D array containing a boolean comfort prediction for each grid point.
        hourly_autonomy (numpy.ndarray): 1D array where each element represents the hourly sTA.
        spatial_autonomy (float): Annual sTA depending on specified percentage area.
    """

    comfort_hours = np.where(abs(prediction_array) <= 0.5, 1, 0)

    hourly_autonomy = np.sum(comfort_hours, axis=0) / prediction_array.shape[0]
    spatial_autonomy = np.sum( np.where(hourly_autonomy > percentage_area, 1, 0)) / prediction_array.shape[1]

    return spatial_autonomy, hourly_autonomy, comfort_hours