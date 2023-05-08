
# AGNITE

## About
The Active Galactic Nuclei Interactive Tool for Exploration, or AGNITE, is a visualization tool for 
the [Unified Model of AGN](https://en.wikipedia.org/wiki/Active_galactic_nucleus?oldformat=true#Unification_of_AGN_species). 
AGNITE operates as a cloud-hosted web app allowing a user to explore how the optical spectrum and SED of AGN changes as the viewing angle changes. 

## Use <a name = "getting_started"></a>
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agnite.streamlit.app)

This project is fully web-accessible but 
can be installed locally as well through the following steps:

```bash
git clone https://github.com/eagiman/agnite.git
cd agnite
```

Ensure you have necessary packages by running

```bash
pip install streamlit
pip install -r requirements.txt
```

The app can now be run locally though

```bash
streamlit run app.py
```

## Acknowledgements
Thank you to Professor Marla Geha and Will Cerny, and
thank you to Audrey Whitmer for designing the obscured AGN model illustration used in this project.

---

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40AnnieGiman)](https://twitter.com/anniegiman)
