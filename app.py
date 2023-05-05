import streamlit as st
from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spectra
import model
import plotly.express as px
import streamlit_toggle as tog
from streamlit_extras.stateful_button import button as Button
from streamlit_extras.add_vertical_space import add_vertical_space

# if 'sidebar_state' not in st.session_state:
#     st.session_state.sidebar_state = 'expanded'

# Configure page
#st.set_page_config(page_title="AGNITE", page_icon='assets/agnite.png', layout='wide', initial_sidebar_state=st.session_state.sidebar_state)
st.set_page_config(page_title="AGNITE", page_icon='assets/agnite.png', layout='wide')

# Initialize angle to 0
if 'angle' not in st.session_state:
    st.session_state['angle'] = 0
    st.session_state.angle = 0

if 'lines' not in st.session_state:
    st.session_state.lines = True
    st.session_state['lines'] = True

if 'default' not in st.session_state:
    st.session_state.default = 'Narrow Line Radio Galaxy'
    st.session_state['default'] = 'Narrow Line Radio Galaxy'

if 'about' not in st.session_state:
    st.session_state['about'] = False

col1, col2 = st.columns([8,1])

with col2:
    add_vertical_space(1)
    Button("About", key='about')

if st.session_state['about']:
    st.info("""
    This is a tool to explore the 
    [unified model](https://en.wikipedia.org/wiki/Active_galactic_nucleus?oldformat=true#Unification_of_AGN_species) 
    of active galactic nuclei (AGN). The spectra of AGN, the extremely luminous centers of most galaxies, differ greatly
    between types. The unified model states all AGN operate fundamentally the same way and these differences are due to 
    viewing angle. This app aims to help visualize this through displaying real AGN spectra and SEDs
    for different viewing angles and types.
    """)

# if st.session_state['about']:
#     st.session_state.sidebar_state = 'collapsed'
#     st.markdown("""---""")
#     info1, info2 = st.columns(2)
#     info2.image('assets/agn_tight.png')
#     st.markdown("""---""")
# else:
#     st.session_state.sidebar_state = 'expanded'

# give title
col1.header('Active Galactic Nuclei Interactive Tool for Exploration')
#st.write('It is going to say more here!')

# # Makes about section
# with st.expander('What are AGN?'):
#     col1, col2 = st.columns(2)
#     col2.image('assets/agn_tight.png')
#     col1.write("Hello!")


type = {
    'Blazar': 80,
    'Radio-Loud Quasar': 60,
    'Radio-Quiet Quasar': -80,
    'Broad Line Radio Galaxy': 30,
    'Narrow Line Radio Galaxy': 10,
    'Seyfert 1': -60,
    'Seyfert 2': -30
}

ind = {
    'Blazar': 0,
    'Radio-Loud Quasar': 1,
    'Radio-Quiet Quasar': 2,
    'Broad Line Radio Galaxy': 3,
    'Narrow Line Radio Galaxy': 4,
    'Seyfert 1': 5,
    'Seyfert 2': 6
}

mod = model.Model(r=910)
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


@st.cache_data
def run(angle, lines, path=None):

    agn.rotate(st.session_state.angle)
    spec = make_spec(angle, lines)
    sed = make_sed(angle)

    vals = {'spec': spec, 'sed': sed, 'type': agn.type, 'obj': agn.obj}

    return vals


@st.cache_data
def make_model(angle):
    return mod.paste(angle)

# st.sidebar.image('/Users/annie/Desktop/Astr330/agnite/agn.png',
#                  use_column_width=True)
# st.sidebar.image(get_model(st.session_state.channel),
#                  use_column_width=True)


st.session_state.angle = st.sidebar.slider('Galaxy Viewing Angle',
                            min_value=-90, max_value=90, value=type[st.session_state['default']], format="%+d°\n")

st.sidebar.image(make_model(st.session_state.angle),
                 use_column_width='always')
# st.sidebar.image(run(st.session_state.angle, st.session_state['lines'])['model'],
#                  use_column_width=True)

# if st.sidebar.button(label='Radio-Quiet Quasar', use_container_width=True):
#     st.session_state.angle = -80
#     st.session_state.default = -80
#
# if st.sidebar.button(label='Seyfert 1', use_container_width=True):
#     st.session_state.angle = -60
#     st.session_state.default = -80
#
# if st.sidebar.button(label='Seyfert 2', use_container_width=True):
#     st.session_state.angle = -30
#     st.session_state.default = -80
#
# if st.sidebar.button(label='Narrow Line Radio Galaxy', use_container_width=True):
#     st.session_state.angle = 10
#     st.session_state.default = -80
#
# if st.sidebar.button(label='Broad Line Radio Galaxy', use_container_width=True):
#     st.session_state.angle = 30
#
#
# if st.sidebar.button(label='Radio-Loud Quasar', use_container_width=True):
#     st.session_state.angle = 60
#
# if st.sidebar.button(label='Blazar', use_container_width=True):
#     st.session_state.angle = 80



# if st.sidebar.button(label='Blazar'):
#     st.session_state.angle = 80
#     default = 80

# if st.sidebar.button(label='Blazar'):
#     st.session_state.angle = 80
#     default = 80
#
# if st.sidebar.button(label='Blazar'):
#     st.session_state.angle = 80
#     default = 80

st.sidebar.selectbox('AGN Type',
    ('Blazar', 'Radio-Loud Quasar', 'Radio-Quiet Quasar', 'Broad Line Radio Galaxy',
     'Narrow Line Radio Galaxy', 'Seyfert 1', 'Seyfert 2'), key='default', index=ind[st.session_state['default']])


metric1, metric2 = st.columns(2)

metric1.metric(label='AGN Type', value=run(st.session_state.angle, st.session_state['lines'])['type'])
metric2.metric(label='Object', value=run(st.session_state.angle, st.session_state['lines'])['obj'])

tab_spec, tab_sed = st.tabs(["Spectrum", "SED"])

with tab_spec:

    tog.st_toggle_switch(label="Display Emission Lines", key='lines', default_value=True)
    st.plotly_chart(run(st.session_state.angle, st.session_state['lines'])['spec'], use_container_width=True)

with tab_sed:

    st.plotly_chart(run(st.session_state.angle, st.session_state['lines'])['sed'], use_container_width=True)
