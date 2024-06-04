import numpy as np

E2k = lambda E: 2*np.pi*np.sqrt(E/81.8)
k2E = lambda K: 81.8*K**2/(2*np.pi)**2
l2k = lambda l: 2*np.pi/l
k2l = lambda K: 2*np.pi/K
l2E = lambda l: k2E(l2k(l))
E2l = lambda E: k2l(E2k(E))