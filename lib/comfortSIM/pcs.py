import numpy as np

class Environment:
    """
    A class used to represent an Environment.

    ...

    Attributes
    ----------
    parameters : list
        A list of parameters that define the environment.
    climate : np.array
        A 2D numpy array with shape (4,n) representing the climate data. 
        Each row corresponds to a different environmental factor (ta, rh, tr, vel).

    Methods
    -------
    
    """

    def __init__(self, parameters:list, climate:np.array):
        self.parameters = parameters
        self.climate = climate


class ComfortPreference:

    def __init__(self, preference:np.array):
        self.preference = preference    # np.array shape (1,n) with comfort preference prediction

    def predict_preference():
        # return prediction, implement use of ML here
        pass


class Device:
    def __init__(self, type, power:int, effect:np.array):
        self.type = type        # heater, cooler or fan
        self.power = power      # e.g. 200W
        self.effect = effect    # e.g. [2, 0, 1.2, 0] for effect on ta, rh, tr, vel

    def use_device(self, environment, comfort):
        # apply effect array to climate array according to comfort preference

        new_climate = np.copy(environment.climate)

        for i in range(len(comfort.preference)):

            effect_ratio = abs(comfort.preference[i])/1

            if self.type == 'fan' and comfort.preference[i] < 0:
                air_movement = effect_ratio * self.effect
                new_climate[:, i] += air_movement

            elif self.type == 'cooler' or self.type == 'fan' and comfort.preference[i] < 0:
                cooling = effect_ratio * self.effect
                new_climate[:, i] += cooling

            elif self.type == 'heater' and comfort.preference[i] > 0:
                heating = effect_ratio * self.effect
                new_climate[:, i] += heating

        environment.climate = new_climate   # update climate array

        # return new_climate    as alternative to updating climate array
        # pass

