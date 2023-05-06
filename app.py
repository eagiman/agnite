import streamlit as st
import numpy as np
import pandas as pd
import classes.spectra as spectra
import classes.model as model
import plotly.express as px
import streamlit_toggle as tog
from streamlit_extras.stateful_button import button as Button
from streamlit_extras.add_vertical_space import add_vertical_space

# Configure page
st.set_page_config(page_title="AGNITE", page_icon='classes/assets/agnite.png', layout='wide')

# Initialize angle to 0
if 'angle' not in st.session_state:
    st.session_state['angle'] = 0
    st.session_state.angle = 0

# Initialize display lines to True
if 'lines' not in st.session_state:
    st.session_state.lines = True
    st.session_state['lines'] = True

# Initialize default to narrow line galaxy
if 'default' not in st.session_state:
    st.session_state.default = 'Narrow Line Radio Galaxy'
    st.session_state['default'] = 'Narrow Line Radio Galaxy'

# Initialize about to False
if 'about' not in st.session_state:
    st.session_state['about'] = False

# Make columns for title and about button
col1, col2 = st.columns([8,1])

# Add about button
# Using Streamlit Extra's stateful button to track whether to display info or not
with col2:
    add_vertical_space(1)
    Button("About", key='about')

# give title
col1.header('Active Galactic Nuclei Interactive Tool for Exploration')

# Give about section
if st.session_state['about']:
    st.info("""
    This is a tool to explore the 
    [unified model](https://en.wikipedia.org/wiki/Active_galactic_nucleus?oldformat=true#Unification_of_AGN_species) 
    of active galactic nuclei (AGN). The spectra of AGN, the extremely luminous centers of most galaxies, differ greatly
    between types. The unified model states all AGN operate fundamentally the same way and these differences are due to 
    viewing angle. This app aims to help visualize this through displaying real AGN spectra and SEDs
    for different viewing angles and types.
    """)

# Create dictionary matching AGN type with default angle for use with selectbox
type = {
    'Blazar': 80,
    'Radio-Loud Quasar': 60,
    'Radio-Quiet Quasar': -80,
    'Broad Line Radio Galaxy': 30,
    'Narrow Line Radio Galaxy': 0,
    'Seyfert 1': -60,
    'Seyfert 2': -30
}

# Create dictionary matching AGN type with index to use for selectbox default
ind = {
    'Blazar': 0,
    'Radio-Loud Quasar': 1,
    'Radio-Quiet Quasar': 2,
    'Broad Line Radio Galaxy': 3,
    'Narrow Line Radio Galaxy': 4,
    'Seyfert 1': 5,
    'Seyfert 2': 6
}


# Create model and agn objects to initialize data and visualization
mod = model.Model(r=910)
agn = spectra.AGN(st.session_state.angle)


def make_spec(angle, lines):
    """
    Function for creating plotly figure displaying spectrum

    Args:
        lines (bool): Determine whether to display emission line markers

    Returns:
        fig (plotly figure): figure of spectrum with or without emission lines marked
    """
    df = agn.df
    fig = px.line(df, x='Wavelength', y='Flux', labels={
        "Wavelength": "Wavelength (&#197;)", "Flux": "Flux (erg cm<sup>-2</sup> s<sup>-1</sup> &#197;<sup>-1</sup>)"})
    if lines:
        agn.plot_lines(fig)
    return fig


def make_sed(angle):
    """
    Function for creating plotly figure displaying SED

    Returns:
        fig (plotly figure): figure of SED
    """
    df = agn.get_sed()
    fig = px.scatter(df, x='Frequency', y='Density', labels={
        'Frequency': 'Frequency (Hz)', 'Density': 'Flux Density (Jy)'}, log_x=True, log_y=True)
    return fig


@st.cache_data
def run(angle, lines):
    """
    Cached driver function to update plots as user input changes

    Args:
        lines (bool): Determine whether to display emission line markers

    Returns:
        Dictionary of spectrum figure, SED figure, AGN type string, and AGN object string
    """
    agn.rotate(st.session_state.angle)
    spec = make_spec(angle, lines)
    sed = make_sed(angle)

    vals = {'spec': spec, 'sed': sed, 'type': agn.type, 'obj': agn.obj}

    return vals


@st.cache_data
def make_model(angle):
    """
    Cached function to update arrow orientation on visualization model

    Args:
        angle (int): Viewing angle in degrees

    Returns:
        (PIL Image): image with arrow pasted with updated location and angle
    """
    return mod.paste(angle)


# Add slider in sidebar for user to input angle
st.session_state.angle = st.sidebar.slider('Galaxy Viewing Angle',
                            min_value=-90, max_value=90, value=type[st.session_state['default']], format="%+d°\n")

# Display model in sidebar using cached function, so it updates with user input
st.sidebar.image(make_model(st.session_state.angle),
                 use_column_width='always')

# Add selectbox for user to view based on AGN type rather than angle, and set angle to default
st.sidebar.selectbox('AGN Type',
    ('Blazar', 'Radio-Loud Quasar', 'Radio-Quiet Quasar', 'Broad Line Radio Galaxy',
     'Narrow Line Radio Galaxy', 'Seyfert 1', 'Seyfert 2'), key='default', index=ind[st.session_state['default']])

# Set up columns for metrics
metric1, metric2 = st.columns(2)

# Create metrics displaying current AGN type and Obejct name
metric1.metric(label='AGN Type', value=run(st.session_state.angle, st.session_state['lines'])['type'])
metric2.metric(label='Object', value=run(st.session_state.angle, st.session_state['lines'])['obj'])

# Create tabs for viewing spectrum and SED
tab_spec, tab_sed = st.tabs(["Spectrum", "SED"])

# Display spectrum and toggle button for displaying emission lines in spectrum tab
with tab_spec:

    tog.st_toggle_switch(label="Display Emission Lines", key='lines', default_value=True)
    st.plotly_chart(run(st.session_state.angle, st.session_state['lines'])['spec'], use_container_width=True)

# Display SED in sed tab
with tab_sed:

    st.plotly_chart(run(st.session_state.angle, st.session_state['lines'])['sed'], use_container_width=True)
