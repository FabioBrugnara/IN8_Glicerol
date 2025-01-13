import numpy as np
import pandas as pd

E2k = lambda E: 2*np.pi*np.sqrt(E/81.8)
k2E = lambda K: 81.8*K**2/(2*np.pi)**2
l2k = lambda l: 2*np.pi/l
k2l = lambda K: 2*np.pi/K
l2E = lambda l: k2E(l2k(l))
E2l = lambda E: k2l(E2k(E))

def get_spec(data, c, const='Q'):
    if const =='Q':
        return data[data.Q == c]
    elif const == 'E':
        return data[data.E == c]
    else:
        raise ValueError('const must be Q or E')
    

################### Convolution of an analytical function with a gaussian ###################

def gauss_conv(x, params, f, sigma, bound=4, conv_res = 0.1):
    """
    Convolution of a function f with a gaussian of width sigma
    """

    gauss = lambda x, sigma: 1/(np.sqrt(2*np.pi)*sigma) * np.exp(-x**2/(2*sigma**2))

    lim = np.max(np.abs(x))+bound*sigma
    E_min, E_max = -lim, lim

    X = np.linspace(E_min, E_max, int((E_max-E_min)/conv_res))
    Y = f(X, *params)
    Y_conv = np.convolve(Y, gauss(X, sigma), mode='same') * (conv_res)

    return np.interp(x, X, Y_conv)