import numpy as np
from astropy.io import fits
from astropy.io import ascii
import matplotlib.pyplot as plt

# plot spectrum
def plot(wave, flux):
    plt.subplots(figsize=(16,5))
    plt.plot(wave, flux)
    plt.show()
    
# put wavelength in rest frame
def rest(wave, z):
    return wave/(1+z)

# make ascii table
def tab(file, names=['Wave', 'Flux']):
    return ascii.read(file, names=names)
    
# Seyfert 1 Spectrum Data
# NGC4151
sy1_path = 'https://ned.ipac.caltech.edu/spc1/1995/1995ApJS...98..477H/NGC_4151:S:B:hfs1995.txt'
#sy1 = ascii.read(sy1_path, names=['Wave', 'Flux'])
sy1 = tab(sy1_path)
#plot(rest(sy1['Wave'], 0.00333), sy1['Flux'])

# Seyfert 2 Spectrum Data
# NGC1068
sy2_path = 'https://ned.ipac.caltech.edu/spc1/1995/1995ApJS...98..477H/NGC_1068:S:B:hfs1995.txt'
sy2 = tab(sy2_path)

