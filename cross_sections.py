##########################################
##### Attenuation leghts calculation #####
##########################################

NA = 6.02214076e23 # Avogadro's number

M = {} # Molar mass
M['H2O'] = 18.01528 # g/mol
M['D2O'] = 20.0276
M['C3D8O3']  = 99.98
M['C3H8O3'] = 92.09382

### Liquid molar densities ###
rho = {} # moles/cm^3
rho['gly'] = lambda T: -2.076146803104599e-08 * T**2 + 2.9401571051129395e-06 * T + 0.014600038465097229
rho['d2'] = 1.11 / M['D2O'] # heavy water density = 1.11 g/cm^3, M in g/mol
rho['h2'] = 1 / M['H2O'] # water density = 1 g/cm^3, M in g/mol

### Cross sections ###

# Bound total scattering cross section [barn]
sigma = {}
sigma['D'] = 7.64 + 0.000519 # barn
sigma['H'] = 82.02 + 0.3326 # barn
sigma['O'] = 4.232 + 0.00019 # barn
sigma['C'] = 5.551 + 0.0035 # barn

# Heavy water cross section
sigma['d2'] = lambda E: 1.53112713e+01 - 3.87942317e-02*E + 1.12174957e-04*E**2

# Build other molecular cross sections
sigma['Dnb'] = lambda E: (sigma['d2'](E)-sigma['O'])/2
sigma['gly'] = lambda E: 8*sigma['Dnb'](E) + 3*sigma['C'] + 3*sigma['O']

# Attenuation coefficient
mu = {}
mu['d2'] = lambda E: sigma['d2'](E)*1e-24 * rho['d2'] * NA
mu['gly'] = lambda E, T: sigma['gly'](E) *1e-24 * rho['gly'](T) * NA