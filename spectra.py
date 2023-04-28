from astropy.io import fits
from astroquery.ipac.ned import Ned
import numpy as np
import pandas as pd

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

    path = 'assets/BASS_DR1_fits.zip/'
    file = 'BASS_DR1_' + num + '.fits'

    return open_spec(path, file)


class AGN:
    """
        The AGN class stores data related to AGN data for chosen viewing angle

        Args:
            angle (int): Viewing angle in degrees

        Attributes:
            angle (int): Viewing angle in degrees
            path (str): Path to fits files
            im (PIL Image): Simple AGN model image
            type (str): Type of AGN
            num (str): Swift BAT object ID number as a 4 digit string
            obj (str): General name of object used as example for AGN type
            wave (ndarray): Wavelength values in Angstrom
            flux (ndarray): Flux values in erg/cm^2/s/A
            df (DataFrame): Wavelength and Flux in a Pandas DataFrame
            lines (dict): Dictionary of emission lines for object
        """
    def __init__(self, angle, path='assets/BASS_fits/BASS_DR1_'):

        self.angle = angle
        self.path = path

        if (angle >= 75) & (angle <= 90):
            self.type = 'Blazar'
            self.num = '0619'
            self.obj = '3C 273'
        elif (angle >= 45) & (angle < 75):
            self.type = 'Radio-Loud Quasar'
            self.num = '0715'
            self.obj = '2MASX J14174289+6141523'
        elif (angle >= 20) & (angle < 45):
            self.type = 'Broad Line Radio Galaxy'
            self.num = '1110'
            self.obj = '4C 50.55'
        elif (angle >= 0) & (angle < 20):
            self.type = 'Narrow Line Radio Galaxy'
            # Maybe also 474? But that's a Seyfert 1 which doesn't make sense?
            # Also 360
            self.num = '0474'
            self.obj = 'VII Zw 292'
        # TODO: add Sy 1.2, 1.5, 1.7, 1.8, 1.9
        elif (angle >= -45) & (angle < 0):
            self.type = 'Seyfert 2'
            # Also 10, 49,
            self.num = '0007'
            self.obj = '2MASX J00091156-0036551'
        elif (angle >= -70) & (angle < -45):
            self.type = 'Seyfert 1'
            self.num = '0002'
            self.obj = 'Fairall 1203'
        elif (angle >= -90) & (angle < -70):
            self.type = 'Radio-Quiet Quasar'
            #num = '1146'
            self.num = '0016'
            #obj = 'Mrk 304'
            self.obj = '[HB89] 0026+129'

        data = fits.open(self.path + self.num + '.fits')[1].data
        wave_full = data['Rest-wavelength']
        flux_full = data['Flux density']
        self.wave, self.flux = no_zero(wave_full, flux_full)
        self.df = pd.DataFrame({"Wavelength": self.wave, "Flux": self.flux})
        self.get_lines()

    def rotate(self, angle):
        """
        Method to refresh attributes for new viewing angle

        Args:
            angle (int): Viewing angle in degrees
        """
        self.angle = angle

        if (angle >= 75) & (angle <= 90):
            self.type = 'Blazar'
            self.num = '0619'
            self.obj = '3C 273'
        elif (angle >= 45) & (angle < 75):
            self.type = 'Radio-Loud Quasar'
            self.num = '0715'
            self.obj = '2MASX J14174289+6141523'
        elif (angle >= 20) & (angle < 45):
            self.type = 'Broad Line Radio Galaxy'
            self.num = '1110'
            self.obj = '4C 50.55'
        elif (angle >= 0) & (angle < 20):
            self.type = 'Narrow Line Radio Galaxy'
            # Maybe also 474? But that's a Seyfert 1 which doesn't make sense?
            # Also 360
            self.num = '0474'
            self.obj = 'VII Zw 292'
            # TODO: add Sy 1.2, 1.5, 1.7, 1.8, 1.9
        elif (angle >= -45) & (angle < 0):
            self.type = 'Seyfert 2'
            # Also 10, 49,
            self.num = '0007'
            self.obj = '2MASX J00091156-0036551'
        elif (angle >= -70) & (angle < -45):
            self.type = 'Seyfert 1'
            self.num = '0002'
            self.obj = 'Fairall 1203'
        elif (angle >= -90) & (angle < -70):
            self.type = 'Radio-Quiet Quasar'
            # num = '1146'
            self.num = '0016'
            # obj = 'Mrk 304'
            self.obj = '[HB89] 0026+129'

        data = fits.open(self.path + self.num + '.fits')[1].data
        wave_full = data['Rest-wavelength']
        flux_full = data['Flux density']
        self.wave, self.flux = no_zero(wave_full, flux_full)
        self.df = pd.DataFrame({"Wavelength": self.wave, "Flux": self.flux})
        self.get_lines()

    def get_spec(self):
        """
        Method to get rest wavelength and flux density out of FITS file

        Returns:
            wave: rest wavelength
            flux: flux density
        """
        return self.wave, self.flux

    def get_sed(self):
        """
        Method to query frequency and density from NED and return dataframe for plotting SED

        Returns:
            df (DataFrame): Pandas DataFrame containing object's frequency and density values
        """
        agn = Ned.get_table(self.obj, table='photometry')
        freq = agn['Frequency']
        den = agn['Flux Density']
        df = pd.DataFrame({'Frequency': freq, 'Density': den})
        return df

    def get_lines(self):
        """
        Method to obtain emission lines for object based on type and set attribute self.lines
        """

        if self.type == "Blazar":
            lines = {
                "O3b": (5006.843, r"[OIIIb]"),
                "H-beta": (4861.333, r"Hβ"),
                "H-gamma": (4341.69, r"Hγ"),
                "Fe5": (4180.600, r"[FeV]"),
            }

        elif self.type == "Radio-Loud Quasar":
            lines = {
                "H-alpha": (6562.819, r"Hα"),
                "N2": (6585.23, r"[NII]"),
                "O3a": (4958.911, r"[OIIIa]"),
                "O3b": (5006.843, r"[OIIIb]"),
                "H-beta": (4861.333, r"Hβ"),
                "O2a": (3728.38, r"[OIIa]"),
                "Ne3": (3868.760, r"[NeIIIa]"),
                "S2a": (6716.440, r"[SIIa]"),
                "S2b": (6730.810, r"[SIIb]")
            }

        elif self.type == "Broad Line Radio Galaxy":
            lines = {
                "H-alpha": (6562.819, r"Hα"),
                "He1": (5877.25, r"He I"),
                "H-beta": (4861.333, r"Hβ"),
                "O3a": (4958.911, r"[OIIIa]"),
                "O3b": (5006.843, r"[OIIIb]"),
                "H1": (7065.196, r"H I")
            }

        elif self.type == "Narrow Line Radio Galaxy":
            lines = {
                "H-beta": (4861.333, r"Hβ"),
                "O3a": (4958.911, r"[OIIIa]"),
                "O3b": (5006.843, r"[OIIIb]"),
                "H-alpha": (6562.819, r"Hα"),
                "N2": (6585.23, r"[NII]"),
                "S2": (6718.32, r"[SII]"),
                "O1": (6300.304, r"[OI]")
            }

        elif self.type == "Seyfert 2":
            lines = {
                "O2b": (3729.86, r"[OIIb]"),
                "Ne3": (3868.760, r"[NeIIIa]"),
                "H-beta": (4861.333, r"Hβ"),
                "O3a": (4958.911, r"[OIIIa]"),
                "O3b": (5006.843, r"[OIIIb]"),
                "N1": (5200.257, r"[NI]"),
                "S2": (6718.32, r"[SII]"),
                "O1": (6363.776, r"[OI]"),
                "Fe7": (6087.000, r"[FeVII]"),
                "H-gamma": (4340.471, r"Hγ"),
                "Cl3a": (5517.709, r"ClIIIa"),
                "Cl3b": (5537.873, r"ClIIIb"),
                "Ar3": (7135.790, r"[ArIII]"),
                "O2": (7330.730, r"[OII]")
                # "Fe10": (6374.510, r"[FeX")
            }

        elif self.type == "Seyfert 1":
            lines = {
                "Ne3": (3869.86, r"[NeIII]"),
                "He2": (4685.710, r"[HeII]"),
                "H-beta": (4861.333, r"Hβ"),
                "O3a": (4958.911, r"[OIIIa]"),
                "O3b": (5006.843, r"[OIIIb]"),
                "Fe2": (5276.002, r"[FeII]"),
                "He1": (5877.25, r"He I"),
                "H-alpha": (6562.819, r"Hα"),
                "N2": (6585.23, r"[NII]"),
                "Fe10": (6374.510, r"[FeX"),
                #"O1": (6363.776, r"[OI]"),
                "S2": (6718.32, r"[SII]"),
                "O1": (6300.304, r"[OI]")
            }

        elif self.type == "Radio-Quiet Quasar":
            lines = {
                "He2": (4685.710, r"[HeII]"),
                "H-beta": (4861.333, r"Hβ"),
                "O3a": (4958.911, r"[OIIIa]"),
                "O3b": (5006.843, r"[OIIIb]"),
                "H-gamma": (4341.69, r"Hγ"),
                "O3": (4363.210, r"[OIII]"),
                "Fe2": (5169.033, r"Fe II")

            }

        self.lines = lines

    def plot_lines(self, fig):
        """
        Method to plot emission lines over spectrum in plotly

        Args:
            fig (Figure): Plotly Figure to overplot lines onto
        """

        lines = self.lines

        if self.type == "Blazar":
            for key in lines:
                fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                              line_dash='dot', annotation_textangle=-90, annotation_position="top left")

        if self.type == "Radio-Loud Quasar":
            for key in lines:
                if key == "O3b" or key == "S2b":
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                                  line_dash='dot', annotation_textangle=-90, annotation_position="top right")
                else:
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                              line_dash='dot', annotation_textangle=-90, annotation_position="top left")

        if self.type == "Broad Line Radio Galaxy":
            for key in lines:
                if key == "O3b":
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                                  line_dash='dot', annotation_textangle=-90, annotation_position="top right")
                else:
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                              line_dash='dot', annotation_textangle=-90, annotation_position="top left")

        if self.type == "Narrow Line Radio Galaxy":
            for key in lines:
                if (key == "O3b") or (key == "H-alpha") or (key == "S2"):
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                                  line_dash='dot', annotation_textangle=-90, annotation_position="top right")
                else:
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                              line_dash='dot', annotation_textangle=-90, annotation_position="top left")

        if self.type == "Seyfert 2":
            for key in lines:
                if (key == "O3b") or (key == "Cl3b"):
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                                  line_dash='dot', annotation_textangle=-90, annotation_position="top right")
                else:
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                              line_dash='dot', annotation_textangle=-90, annotation_position="top left")

        if self.type == "Seyfert 1":
            for key in lines:
                if (key == "O3b") or (key == "H-alpha"):
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                                  line_dash='dot', annotation_textangle=-90, annotation_position="top right")
                else:
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                              line_dash='dot', annotation_textangle=-90, annotation_position="top left")

        if self.type == "Radio-Quiet Quasar":
            for key in lines:
                if key == "O3":
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                                  line_dash='dot', annotation_textangle=-90, annotation_position="top right")
                else:
                    fig.add_vline(lines[key][0], annotation_text=lines[key][1], line_color='grey', line_width=1,
                              line_dash='dot', annotation_textangle=-90, annotation_position="top left")