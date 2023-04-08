import streamlit as st
from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np
import copy
import spectra

# give title
st.title('AGNITE: Active Galactic Nuclei Interactive Tool for Exploration')

# let user choose angle
st.header('Angle')
if 'angle' not in st.session_state:
    st.session_state['angle'] = 0

# get spectrum
@st.cache_data()
def spec(angle, path=None):
    wave, flux = spectra.get_spec(angle)
    fig, ax = plt.subplots(figsize=(16,5))
    ax.plot(wave, flux)
    return fig



st.sidebar.markdown('Choose Settings')

st.session_state.channel = st.sidebar.slider('Galaxy Viewing Angle',
                            min_value=0, max_value=180)

st.pyplot(spec(st.session_state.channel))