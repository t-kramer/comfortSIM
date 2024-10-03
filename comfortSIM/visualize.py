# visualize results

import matplotlib.pyplot as plt
import numpy as np

from comfortSIM.metrics import calculate_spatial_autonomy

mm = 1 / (2.54 * 10)  # millimeters in inches

plt.rcParams["font.family"] = "Helvetica"
plt.rcParams.update({"font.size": 7})
plt.rcParams["axes.linewidth"] = 0.5
plt.rcParams["xtick.bottom"] = True
plt.rcParams["xtick.major.size"] = 3.5
plt.rcParams["xtick.major.width"] = 0.5

plt.rcParams["ytick.left"] = True
plt.rcParams["ytick.major.size"] = 3.5
plt.rcParams["ytick.major.width"] = 0.5

plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

plt.rcParams["axes.labelpad"] = 10


def plot_hourly_autonomy(predictions, algorithm, aspect=15):
    """
    Plots spatial Thermal Autonomy.

    Args:
        predictions (numpy.ndarray): A 2D array of predictions (e.g. ML, PMV) to plot.
        algorithm (str): The algorithm used to generate the predictions (e.g. 'Adaptive', 'PMV').
        aspect (int, optional): The aspect ratio of the plot. Defaults to 10.
    """
    plt.figure(dpi=300)
    plt.imshow(
        np.sort(predictions, axis=0)[::-1],
        cmap="bwr",
        interpolation="bicubic",
        aspect=aspect,
        alpha=0.75,
        vmax=1,
        vmin=-1,
    )

    plt.title(
        f"Model: {algorithm}, spatial Thermal Autonomy: {calculate_spatial_autonomy(predictions).annual_autonomy}",
        loc="left",
        fontsize=8,
    )

    plt.xlabel("Time [h]")
    plt.ylabel("Points")

    xticks = [
        0,  # JAN
        32 * 24,  # FEB
        60 * 24,  # etc.
        91 * 24,
        121 * 24,
        152 * 24,
        182 * 24,
        213 * 24,
        244 * 24,
        274 * 24,
        305 * 24,
        335 * 24,
    ]

    xlabels = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    plt.xticks(ticks=xticks, labels=xlabels)

    plt.show()


def plot_daily_autonomy(arr: np.array, days=365, colorbar=False):
    """

    Plots daily comfort conditions.

    Args:
        arr (np.array): Requires an array of 8760 hourly comfort condition values
        days (int, optional): Number of days to plot. Defaults to 365.
        colorbar (bool, optional): Option to include colorbar. Defaults to False.

    """

    if days == 365:
        xticks = [0, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
        xlabels = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        yticks = [-0.5, 5.5, 11.5, 17.5, 23.5]
        ylabels = [0, 6, 12, 18, 24]

    plt.figure(figsize=(8, 6), dpi=300)
    plt.imshow(
        arr.reshape((24, days), order="F"),
        cmap="binary_r",
        interpolation="nearest",
        aspect=5,
        origin="lower",
    )

    plt.xticks(ticks=xticks, labels=xlabels)
    plt.yticks(ticks=yticks, labels=ylabels)

    plt.xlabel("Time [d]")
    plt.ylabel("Time [h]")

    if colorbar:
        plt.colorbar(location="bottom")

    plt.show()
