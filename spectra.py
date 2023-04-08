from astropy.io import fits


def open_spec(path, file):
    """
    Function to get rest wavelength and flux density out of FITS file

    Args:
        path: pathname
        file: filename

    Returns:
        wave: rest wavelength
        flux: flux density
    """
    data = fits.open(path + file)[1]
    wave = data['Rest-wavelength']
    flux = data['Flux density']
    return wave, flux


def get_spec(angle):
    """
    Function to get AGN classification based on approximate viewing angle.
    Uses rough definitions of Emma Alexander and data from BASS Data Release 1.

    Args:
        angle (int): Approximate AGN viewing angle

    Returns:
        wave (np array): rest wavelength
        flux (np array): flux density
    """
    if (angle >= 0) & (angle < 15):
        type = 'blazar'
        num = '0545'
    elif (angle >= 15) & (angle < 45):
        type = 'radio-loud quasar'
        num = '0715'
    elif (angle >= 45) & (angle < 70):
        type = 'broad line radio galaxy'
        num = '1110'
    elif (angle >= 70) & (angle < 90):
        type = 'narrow line radio galaxy'
        # Maybe also 474? But that's a Seyfert 1 which doesn't make sense?
        num = '0360'
    # TODO: add Sy 1.2, 1.5, 1.7, 1.8, 1.9
    elif (angle >= 90) & (angle < 135):
        type = 'sy2'
        num = '0005'
    elif (angle >= 135) & (angle < 160):
        type = 'sy1'
        num = '0002'
    elif (angle >= 160) & (angle <= 180):
        type = 'radio-quiet quasar'
        num = '1146'

    path = '/Users/annie/Downloads/BASS_DR1_fits.zip/'
    file = 'BASS_DR1_' + num + '.fits'

    return open_spec(path, file)
