import streamlit as st
from time import sleep
#from navigation import make_sidebar
import streamlit as st
import plotly.graph_objects as go
from utils import *
import time
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
#from streamlit_autorefresh import st_autorefresh
from streamlit_folium import folium_static
import folium
import requests
import matplotlib.pyplot as plt
import requests
import json
from windrose import WindroseAxes
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image

st.set_page_config(page_title="Agrifirm@AquaSim", layout="wide")

####################
def make_sidebar():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>Smart Irrigation Tool</h1>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.sidebar.image(load_image("logo1.png"), use_column_width=True)
        st.sidebar.image(load_image("logo2.png"), use_column_width=True)
        st.sidebar.markdown("<p style='text-align: center;'><a href='mailto:f.deoliveirasalles@agrifirm.com'>Contact: Filipe Salles</a></p>", unsafe_allow_html=True)
################################

def load_image(image_path):
    return Image.open(image_path)


make_sidebar()

st.title("Welcome to the Agrifirm@AquaSim project")


#st.write("Please log in to continue (username `test`, password `test`).")

# Lista de dicionários contendo usuários e senhas
#users = [
#    {"username": "test", "password": "test"},
#    {"username": "filipe", "password": "filipe"},
#    {"username": "user", "password": "user"}
#]

# Entrada de nome de usuário e senha
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Verificação de login
if st.button("Log in", type="primary"):
    # Verifica se o nome de usuário e a senha correspondente estão no dicionário de usuários
    if username == "test" and password == "test":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    if username == "u.thissen@agrifirm.com" and password == "Thissen":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    if username == "h.vollaard@agrifirm.com" and password == "Vollaard":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    if username == "j.teeuwen@agrifirm.com" and password == "Teeuwen":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")
        
    if username == "b.mulder@agrifirm.com" and password == "Mulder":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    if username == "j.warmerdam@agrifirm.com" and password == "Warmerdam":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")
        
    if username == "h.r.vanderstruik@agrifirm.com" and password == "Struik":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")
        
    if username == "k.overheul@agrifirm.com" and password == "Overheul":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    if username == "l.bin@cebecoagro.nl" and password == "Bin":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")
        
    if username == "s.jeuken@agrifirm.com" and password == "Jeuken":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")
        
    if username == "b.berkhout@agrifirm.com" and password == "Berkhout":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    if username == "m.schoorl@agrifirm.com" and password == "Schoorl":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")
        
    if username == "r.vandortmont@agrifirm.com" and password == "Dortmont":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")
        
    if username == "l.vandijk@agrifirm.com" and password == "Dijk":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    if username == "a.kielak@agrifirm.com" and password == "Butterbach":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    if username == "i.vaneck@agrifirm.com" and password == "Eck":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    if username == "w.cuperus@agrifirm.com" and password == "Cuperus":
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/app.py")

    
#    elif username == "Flevoland" and password == "Flevoland":
#        st.session_state.logged_in = True
#        st.success("Logged in successfully!")
#        sleep(0.5)
#        st.switch_page("pages/farm1.py")
#    elif username == "Chile" and password == "Chile":
#        st.session_state.logged_in = True
#        st.success("Logged in successfully!")
#        sleep(0.5)
#        st.switch_page("pages/farm2.py")
    else:
        st.error("Incorrect username or password")
        
