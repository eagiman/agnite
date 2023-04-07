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
    st.session_state['angle'] = 1

# get spectrum
@st.cache_data()
def get_spec(type, path=None):
    if type==1:
        path = 'https://ned.ipac.caltech.edu/spc1/1995/1995ApJS...98..477H/NGC_4151:S:B:hfs1995.txt'
    elif type==2:
        path = 'https://ned.ipac.caltech.edu/spc1/1995/1995ApJS...98..477H/NGC_1068:S:B:hfs1995.txt'
    data = ascii.read(path, names=['wave','flux'])
    #return data['wave'], data['flux']
    fig, ax = plt.subplots(figsize=(16,5))
    ax.plot(data['wave'], data['flux'])
    return fig

    #return plt.plot(data['wave'], data['flux'])


st.sidebar.markdown('Choose Settings')
# angle = st.sidebar.slider('Choose Seyfert Galaxy Type',
#                             min_value=1, max_value=2, value=1)

st.session_state.channel = st.sidebar.slider('Choose Seyfert Galaxy Type',
                            min_value=1, max_value=2)

st.pyplot(get_spec(st.session_state.channel))