import setuptools

setuptools.setup(
    name='agnite',
    version='0.1.0',
    description='Active Galactic Nuclei Interactive Tool for Exploration',
    url='https://github.com/eagiman/agnite',
    author='Annie Giman',
    author_email='annie.giman@yale.edu',
    license='MIT',
    packages=['agnite'],
    install_requires=['numpy','Pillow','streamlit','pandas','plotly',
                      'streamlit_toggle','streamlit_extras','astroquery','astropy']
)
