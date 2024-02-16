# This file contains the post-processing functions for the comfortSIM package.

import numpy as np
import matplotlib.pyplot as plt

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




def plot_sta(predictions, algorithm, width=10):
    """
    Plots spatial Thermal Autonomy.

    Args:
        predictions (numpy.ndarray): A 2D array of predictions (e.g. ML, PMV) to plot.
        algorithm (str): The algorithm used to generate the predictions (e.g. 'ML', 'PMV').
        width (int, optional): The width of the plot. Defaults to 10.
    """
    plt.figure(figsize=(width,0.5*width), dpi=500)
    plt.imshow(np.sort(predictions, axis=0), cmap='bwr_r',interpolation='bicubic', aspect=2, alpha=0.75, vmax=1,vmin=-1)
    plt.title(f"Model: {algorithm}, spatial Thermal Autonomy: {compute_sta(predictions)[0].round(decimals=2)}", font='Helvetica')
    plt.xlabel("Time [h]")
    plt.ylabel("Grid points [-]")

    xticks = [15.5*24,      #JAN
              (32+15.5)*24, #FEB
              (60+15.5)*24, #etc.
              (91+15.5)*24,
              (15.5+121)*24,
              (15.5+152)*24,
              (15.5+182)*24,
              (15.5+213)*24,
              (15.5+243)*24,
              (15.5+274)*24,
              (15.5+304)*24,
              (15.5+334)*24]
    
    xlabels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    plt.xticks(ticks=xticks,labels=xlabels)

    plt.show()




def daily_plot(arr:np.array, days=365, colorbar=False):
    """_summary_

    Args:
        arr (np.array): Requires an array of 8760 hourly comfort condition values
        colorbar (bool, optional): Option to include colorbar. Defaults to False.
    """

    if days == 365:
        xticks = [0, 32, 60,91,121,152,182,213,243,274,304,334]
        xlabels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        yticks = [-0.5,5.5,11.5,17.5,23.5]
        ylabels = [0,6,12,18,24]

    plt.figure(figsize=(8,6), dpi=300)
    plt.imshow(arr.reshape((24,days),order='F'), cmap='binary_r', interpolation='nearest', aspect=5, origin='lower')
    # plt.colorbar(location='bottom')

    plt.xticks(ticks=xticks,labels=xlabels,fontsize=7, font='Helvetica')
    plt.yticks(ticks=yticks,labels=ylabels,fontsize=7, font='Helvetica')

    plt.xlabel('Time [d]', font='Helvetica')
    plt.ylabel('Time [h]', font='Helvetica')
    
    if colorbar:
        plt.colorbar(location='bottom')
    
    plt.show()