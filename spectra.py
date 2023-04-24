from astropy.io import fits
from astroquery.ipac.ned import Ned

def no_zero(wave, flux):
    """
    Function that gets rid of 0 values in wavelength and flux arrays

    Args:
        wave (ndarray): rest wavelength
        flux (ndarray): flux density

    Returns:
       ndarray: rest wavelength without 0 values
       ndarray: flux density where resting wavelength is not 0
    """
    ind = wave > 0
    return wave[ind], flux[ind]


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
    data = fits.open(path + file)[1].data
    wavefull = data['Rest-wavelength']
    fluxfull = data['Flux density']
    wave, flux = no_zero(wavefull, fluxfull)
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
    angle += 90
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
        # Also 360
        num = '0474'
    # TODO: add Sy 1.2, 1.5, 1.7, 1.8, 1.9
    elif (angle >= 90) & (angle < 135):
        type = 'sy2'
        # Also 10, 49,
        num = '0007'
    elif (angle >= 135) & (angle < 160):
        type = 'sy1'
        num = '0002'
    elif (angle >= 160) & (angle <= 180):
        type = 'radio-quiet quasar'
        num = '1146'

    path = '/Users/annie/Downloads/BASS_DR1_fits.zip/'
    file = 'BASS_DR1_' + num + '.fits'

    return open_spec(path, file)

class agn:

    def __init__(self, angle, path='/Users/annie/Downloads/BASS_DR1_fits.zip/BASS_DR1_'):
        angle += 90
        self.angle = angle
        self.path = path

        if (angle >= 0) & (angle < 15):
            type = 'Blazar'
            num = '0545'
            obj = 'PKS 1127-14'
        elif (angle >= 15) & (angle < 45):
            type = 'Radio-Loud Quasar'
            num = '0715'
            obj = '2MASX J14174289+6141523'
        elif (angle >= 45) & (angle < 70):
            type = 'Broad Line Radio Galaxy'
            num = '1110'
            obj = '4C 50.55'
        elif (angle >= 70) & (angle < 90):
            type = 'Narrow Line Radio Galaxy'
            # Maybe also 474? But that's a Seyfert 1 which doesn't make sense?
            # Also 360
            num = '0474'
            obj = 'VII Zw 292'
        # TODO: add Sy 1.2, 1.5, 1.7, 1.8, 1.9
        elif (angle >= 90) & (angle < 135):
            type = 'Seyfert 2'
            # Also 10, 49,
            num = '0007'
            obj = '2MASX J00091156-0036551'
        elif (angle >= 135) & (angle < 160):
            type = 'Seyfert 1'
            num = '0002'
            obj = 'Fairall 1203'
        elif (angle >= 160) & (angle <= 180):
            type = 'Radio-Quiet Quasar'
            num = '1146'
            obj = 'Mrk 304'

        self.type = type
        self.num = num
        self.obj = obj

    def get_spec(self):
        """
        Function to get rest wavelength and flux density out of FITS file

        Args:
            path: pathname
            file: filename

        Returns:
            wave: rest wavelength
            flux: flux density
        """
        data = fits.open(self.path + self.num + '.fits')[1].data
        wavefull = data['Rest-wavelength']
        fluxfull = data['Flux density']
        wave, flux = no_zero(wavefull, fluxfull)
        return wave, flux

    def get_sed(self):
        agn = Ned.get_table(self.obj, table='photometry')
        freq = agn['Frequency']
        den = agn['Flux Density']
        return freq, den

