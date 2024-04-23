import numpy as np


def wrap_to_pi(x):
    x = x - np.floor(x / (2 * np.pi)) * 2 * np.pi - np.pi
    return x
