import streamlit as st
from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np
import copy
import spectra
import model

# give title
st.title('Active Galactic Nuclei Interactive Tool for Exploration')

# Test thingy
# col1, mid, col2 = st.columns([1,1,20])
# with col1:
#     st.image('agnite.png', width=60)
# with col2:
#     st.write('A Name')


# let user choose angle
st.header('Angle')
if 'angle' not in st.session_state:
    st.session_state['angle'] = 0

# get spectrum
# @st.cache_data()
# def spec(angle, path=None):
#     wave, flux = spectra.get_spec(angle)
#     wave, flux = spectra.no_zero(wave, flux)
#     fig, ax = plt.subplots(figsize=(16,5))
#     ax.plot(wave, flux)
#     return fig

@st.cache_data()
def spec(angle, path=None):
    agn = spectra.agn(angle)
    wave, flux = agn.get_spec()
    fig, ax = plt.subplots(figsize=(16,5))
    ax.plot(wave, flux)
    return fig

@st.cache_data()
def sed(angle, path=None):
    agn = spectra.agn(angle)
    freq, den = agn.get_sed()
    fig, ax = plt.subplots()
    ax.scatter(freq, den)
    plt.xscale('log')
    plt.yscale('log')
    return fig


st.sidebar.markdown('Choose Viewing Angle')

mod = model.Model(r=850)
@st.cache_data()
def get_model(angle):
    return mod.paste(angle)

# st.sidebar.image('/Users/annie/Desktop/Astr330/agnite/agn.png',
#                  use_column_width=True)
# st.sidebar.image(get_model(st.session_state.channel),
#                  use_column_width=True)


st.session_state.channel = st.sidebar.slider('Galaxy Viewing Angle',
                            min_value=-90, max_value=90)

st.sidebar.image(get_model(st.session_state.channel),
                 use_column_width=True)

st.pyplot(spec(st.session_state.channel))
st.pyplot(sed(st.session_state.channel))
