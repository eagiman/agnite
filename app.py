import streamlit as st
from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
import spectra
import model
import plotly.express as px
import  streamlit_toggle as tog

# Configure page
st.set_page_config(page_title="AGNITE", page_icon='assets/agnite.png', layout='wide')

# give title
st.header('Active Galactic Nuclei Interactive Tool for Exploration')
#st.write('It is going to say more here!')


# Initialize angle to 0
if 'angle' not in st.session_state:
    st.session_state['angle'] = 0
    st.session_state.angle = 0
    st.session_state.lines = True
    st.session_state['lines'] = True


mod = model.Model(r=800)
agn = spectra.AGN(st.session_state.angle)

def make_spec(angle, lines):
    df = agn.df
    fig = px.line(df, x='Wavelength', y='Flux', labels={
        "Wavelength": "Wavelength (&#197;)", "Flux": "Flux (erg cm<sup>-2</sup> s<sup>-1</sup> &#197;<sup>-1</sup>)"})
    if lines:
        agn.plot_lines(fig)
    return fig


def make_sed(angle):
    df = agn.get_sed()
    fig = px.scatter(df, x='Frequency', y='Density', labels={
        'Frequency': 'Frequency (Hz)', 'Density': 'Flux Density (Jy)'}, log_x=True, log_y=True)
    return fig


@st.cache_data()
def run(angle, lines, path=None):

    agn.rotate(st.session_state.angle)
    spec = make_spec(angle, lines)
    sed = make_sed(angle)

    vals = {'spec': spec, 'sed': sed, 'type': agn.type, 'obj': agn.obj}
    # wave, flux = agn.get_spec()
    # fig, ax = plt.subplots(figsize=(16,5))
    # ax.plot(wave, flux)
    # ax.set_title(agn.type)
    #if st.session_state.lines:

    #return fig, agn.type, agn.obj
    return vals

@st.cache_data()
def get_model(angle):
    return mod.paste(angle)

# st.sidebar.image('/Users/annie/Desktop/Astr330/agnite/agn.png',
#                  use_column_width=True)
# st.sidebar.image(get_model(st.session_state.channel),
#                  use_column_width=True)


st.session_state.angle = st.sidebar.slider('Galaxy Viewing Angle',
                            min_value=-90, max_value=90)

st.sidebar.image(get_model(st.session_state.angle),
                 use_column_width=True)


metric1, metric2 = st.columns(2)

metric1.metric(label='AGN Type', value=run(st.session_state.angle, st.session_state['lines'])['type'])
metric2.metric(label='Object', value=run(st.session_state.angle, st.session_state['lines'])['obj'])

tab_spec, tab_sed = st.tabs(["Spectrum", "SED"])

with tab_spec:

    tog.st_toggle_switch(label="Display Emission Lines", key='lines', default_value=True)
    st.plotly_chart(run(st.session_state.angle, st.session_state['lines'])['spec'], use_container_width=True)

with tab_sed:

    st.plotly_chart(run(st.session_state.angle, st.session_state['lines'])['sed'], use_container_width=True)
