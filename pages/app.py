#######################################AQUASIM AGRIFIRM PROJECT##################
#######################################AUTHOR: FILIPE SALLES#####################
####################################EMAIL: F.DEOLIVEIRASALLES-AT-AGRIFIRM.COM####
#################################################################################


import streamlit as st
import plotly.graph_objects as go
from utils import *
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
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
import requests
import plotly.express as px
from api_keys import openweathermap_api_key, visualcrossing_api_key, vaimee_api_key, agurotech_api_key, agromonitoring_api_key

from retry_requests import retry
import requests_cache
import openmeteo_requests

import pytz

################################Title############################################
#################################################################################

st.set_page_config(page_title="Agrifirm@AquaSim", layout="wide")

readme = load_config("config_readme.toml")


# Info
st.title("AquaSim Project")

#################################################################################
#################################################################################



###########################Login webpage#########################################
#################################################################################

# Função para carregar imagem
def load_image(image_path):
    return Image.open(image_path)

def main():
    # Página de login
    st.sidebar.image(load_image("logo2.png"), use_column_width=True)
    
#################################################################################
#################################################################################





##############################Farms and lateral bar##############################
#################################################################################

##############################fazendas e barra lateral#######################################

# Add the select bar in the sidebar
st.sidebar.image(load_image("logo1.png"), use_column_width=True)
display_links(readme["links"]["repo"], readme["links"]["other_link"])
    
    
with st.sidebar:
    st.write("When choosing the farm below, the data on the main page will be updated to the farm.")
    st.write("Select your farm:")
    farm_choice = st.selectbox("", ("Schoonoord - Sugar Beet", "Schoonoord - Starch Potato", "Vijfhuizen - Tulip", "Lelystad (Fertigation trail) - Onions", "Erlecom - Potato", "Erlecom - Onion", "Veendam - Onion", "Hengelo (Corridor) - Soy and Faba","Mitselwier - Hybrid Potato"))
    st.write("")
    st.write("Available data about the farm click below.")
    	
# Create a container in the main section for the weather data
#st.write("Weather Data")
container = st.container()

# fazendas que serao usadas no AquaSim
if farm_choice == "Laverdonk":
    farm_geojson_path = 'farms/laverdonk.geojson'
    latitude, longitude = 51.636741, 5.481757
    farm_zoom = 15  # Zoom level
elif farm_choice == "Schoonoord - Sugar Beet":
    farm_geojson_path = 'farms/schoonoord-1-sugar-beat.geojson'
    latitude, longitude = 52.82462830324437, 6.8124085664749146
    farm_zoom = 15  # Zoom level    
elif farm_choice == "Schoonoord - Starch Potato":
    farm_geojson_path = 'farms/schoonoord-2-starch-potato.geojson'
    latitude, longitude = 52.826289, 6.813798
    farm_zoom = 15  # Zoom level 
elif farm_choice == "Vijfhuizen - Tulip":
    farm_geojson_path = 'farms/tulip.geojson'
    latitude, longitude = 52.345163, 4.693297
    farm_zoom = 15  # Zoom level    
elif farm_choice == "Lelystad (Fertigation trail) - Onions":
    farm_geojson_path = 'farms/lelystad-onion.geojson'
    latitude, longitude = 52.540013, 5.5593078
    farm_zoom = 15  # Zoom level 
elif farm_choice == "Mitselwier - Hybrid Potato":
    farm_geojson_path = 'farms/mitselwier-hybrid-potato.geojson'
    latitude, longitude = 53.373020, 6.073236
    farm_zoom = 16  # Zoom level 
elif farm_choice == "Hengelo (Corridor) - Soy and Faba":
    farm_geojson_path = 'farms/hengelo-soy-faba.geojson'
    latitude, longitude = 52.065633, 6.271922
    farm_zoom = 17  # Zoom level 
elif farm_choice == "Erlecom - Potato":
    farm_geojson_path = 'farms/erlecom-potato.geojson'
    latitude, longitude = 51.838302, 5.971706
    farm_zoom = 15  # Zoom level 
elif farm_choice == "Erlecom - Onion":
    farm_geojson_path = 'farms/erlecom-onion.geojson'
    latitude, longitude = 51.847648, 5.975258 
    farm_zoom = 15  # Zoom level
elif farm_choice == "Veendam - Onion":
    farm_geojson_path = 'farms/veendam.geojson'
    latitude, longitude = 53.05827, 6.90554 
    farm_zoom = 15  # Zoom level 
    
    
    
#################################################################################
#################################################################################

    
    
    
    
############################Soil map#############################################
#################################################################################


# Display the map in the central part of the page
farm_map = folium.Map(location=[latitude, longitude], zoom_start=farm_zoom)

# Try to load and display the GeoJson file
try:
    with open(farm_geojson_path, 'r') as f:
        data = f.read()
    folium.GeoJson(data).add_to(farm_map)
    folium_static(farm_map)
except ValueError:
    st.write("Cannot render the selected farm.")

#################################################################################
#################################################################################






##############################################OpenWeatherMap#####################
#################################################################################


base_url = "http://api.openweathermap.org/data/2.5/forecast?"

complete_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweathermap_api_key}&units=metric"
response = requests.get(complete_url)
x = response.json()

#GLOBALS

y = x["main"]
print(y)
current_temp = y["temp"]
max_temp = round((y["temp_max"]))
min_temp = round(y["temp_min"])
humidity = y["humidity"]
pressure = y["pressure"]
feels = y["feels_like"]
#sea = round(y["sea_level"])



def get_temp():
    return(str(current_temp)+" °C")


def get_temp_min():
    return(str(min_temp)+" °C")


def get_temp_max():
    return(str(max_temp)+" °C")

def get_humidity():
    return(str(humidity))

def get_pressure():
    return(str(pressure))

def get_feel():
    return(str(feels)+"°C")
    
    

#Autorefresh:
#count = st_autorefresh(interval=5000, limit=100, key="fizzbuzzcounter")

#################################################################################
#################################################################################


################Day and weather image############################################
#################################################################################


#Time
nowTime = datetime.now()
current_time = nowTime.strftime("%H:%M:%S")
today = datetime.today().strftime("Day - %d/%m/%Y")

# Obter o ícone do clima e a descrição
weather_icon = x['weather'][0]['icon']
weather_description = x['weather'][0]['description']

# Abrir a imagem correspondente ao ícone do clima
image_path = f"icons/{weather_icon}.png"
img = Image.open(image_path)

# Criar duas colunas
col1, col2 = st.columns(2)

# Exibir a imagem na primeira coluna
col2.image(img, width=115)

# Exibir o campo de data na segunda coluna
col1.metric("", today)

# Adicionar uma linha horizontal
st.markdown('<hr style="border-top: 1px solid #f63366">', unsafe_allow_html=True)



# Row A
with st.container():
    a1, a2 = st.columns(2)
    a1.metric("Temperature", f"{get_temp()}")
    a2.metric("Time", current_time)

# Row B
with st.container():
    b1, b2 = st.columns(2)
    b1.metric("Humidity", f"{get_humidity()}"+"%")
    b2.metric("Feels like", f"{get_feel()}")

# Row C
with st.container():
    c1, c2 = st.columns(2)
    c1.metric("Highest temperature", f"{get_temp_max()}")
    c2.metric("Lowest temperature", f"{get_temp_min()}")
    
#################################################################################
#################################################################################







###################################IRRIGATION CRITERIA-1D########################
#################################################################################

# Dicionário para mapear o nome da fazenda para o ID da API
farm_api_ids = {
    "Schoonoord - Sugar Beet": "Schoonoord-springbeet-Unit",
    "Schoonoord - Starch Potato": "Schoonoord-potato-Unit",
    "Vijfhuizen - Tulip": "Vijfhuizen-tulip-Unit",
    "Lelystad (Fertigation trail) - Onions": "Lelystad-onion-Unit",
    "Erlecom - Potato": "Erlecom-potato-Unit",
    "Erlecom - Onion": "Erlecom-onion-Unit",
    "Veendam - Onion": "Veendam-onion-Unit",
    "Mitselwier - Hybrid Potato": "Mitselwier-potato-Unit",
    "Hengelo (Corridor) - Soy and Faba": "Hengelo-soy-Unit"
}

# Função para fazer a chamada à API e retornar os dados em um DataFrame
def get_api_data(farm_choice):
    farm_api_id = farm_api_ids.get(farm_choice)
    if farm_api_id is None:
        return None
    url = f"https://api.agrifirm.agora.vaimee.com/units/https%3A%2F%2Fvaimee.com%23{farm_api_id}/forecast"
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {vaimee_api_key}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return pd.DataFrame(data['output'])

# Função para formatar os dados para plotar o gráfico
def format_data_for_plot(df):
    df["ptime"] = pd.to_datetime(df["ptime"]).dt.strftime("%Y-%m-%d")
    #df["irrigationNeeds"] = pd.to_numeric(df["irrigationNeeds"], errors='coerce')
    df["soilWaterContent15"] = pd.to_numeric(df["soilWaterContent15"], errors='coerce') * 100
    df["soilWaterContent30"] = pd.to_numeric(df["soilWaterContent30"], errors='coerce') * 100
    df["soilWaterContent50"] = pd.to_numeric(df["soilWaterContent50"], errors='coerce') * 100
    return df



# Dicionário de títulos personalizados
custom_titles = {
    #"irrigationNeeds": "Necessidades de Irrigação - Previsão para os próximos 3 dias",
    "surfaceWaterContent": "Surface Water Content - Forecast for the next 3 days",
    "soilWaterContent15": "Soil Water Content at 15cm - Forecast for the next 3 days",
    "soilWaterContent30": "Soil Water Content at 30cm - Forecast for the next 3 days",
    "soilWaterContent50": "Soil Water Content at 50cm - Forecast for the next 3 days",
    "waterPotential15": "Water potential at 15cm - Forecast for the next 3 days",
    "waterPotential30": "Water potential at 30cm - Forecast for the next 3 days",
    "waterPotential50": "Water potential at 50cm - Forecast for the next 3 days",
    "rootDepth": "Root Depth - Forecast for the next 3 days",
    "et0": "Reference Evapotranspiration - Forecast for the next 3 days",
    "leafAreaIndex": "Leaf Area Index - Forecast for the next 3 days"
}


# Função para plotar o gráfico
def plot_graph(data, parameter, graph_type):
    fig = go.Figure()
    if graph_type == "line":
        fig.add_trace(go.Scatter(x=data["ptime"], y=data[parameter], mode="lines+markers", connectgaps=True))
    elif graph_type == "bar":
        fig.add_trace(go.Bar(x=data["ptime"], y=data[parameter]))
    fig.update_layout(
        title=custom_titles.get(parameter, f"Irrigation water needs [mm] - Forecast for the next 3 days"),
        xaxis_title="Day-Month",
        yaxis_title=get_yaxis_label(parameter)
    )
    st.plotly_chart(fig)

# Função para obter o rótulo do eixo y de acordo com o parâmetro
def get_yaxis_label(parameter):
    labels = {
        "irrigationNeeds": "Irrigation water needs [mm]",
        "surfaceWaterContent": "Surface water content [mm]",
        "soilWaterContent15": "Volumetric water content [%]",
        "soilWaterContent30": "Volumetric water content [%]",
        "soilWaterContent50": "Volumetric water content [%]",
        "waterPotential15": "Water potential [kPa]",
        "waterPotential30": "Water potential [kPa]",
        "waterPotential50": "Water potential [kPa]",
        "rootDepth": "Root depth [m]",
        "et0": "Reference evapotranspiration [mm]",
        "leafAreaIndex": "Leaf area index [m2 m-2]"
    }
    return labels.get(parameter, "Valor")

# Carregar os dados da API
api_data = get_api_data(farm_choice)

# Adicionar um botão para carregar os gráficos
if st.sidebar.button("CRITERIA Simulation - 3 days forecast"):
    formatted_data = format_data_for_plot(get_api_data(farm_choice))
    for parameter in ["irrigationNeeds", "surfaceWaterContent", "soilWaterContent15", "soilWaterContent30", "soilWaterContent50", "waterPotential15", "waterPotential30", "waterPotential50", "et0", "leafAreaIndex", "rootDepth"]:
        plot_graph(formatted_data, parameter, "line")
        
#################################################################################
#################################################################################        

###############################irrigation - first page###########################
#################################################################################

#st.write("Irrigation forecast - next 3 days")

formatted_data1 = format_data_for_plot(api_data)

def plot_line_chart(data, parameter):
    fig = go.Figure(go.Scatter(x=data["ptime"], y=data[parameter], mode="lines+markers", name=parameter))
    fig.update_layout(title=f"Irrigation Needs - Forecast for the next 3 days", xaxis_title="Day-Month", yaxis_title=get_yaxis_label(parameter))
    st.plotly_chart(fig)
    
plot_line_chart(formatted_data1, "irrigationNeeds")

#################################################################################
#################################################################################







################Plot for weather 5 days forecast ################################
#################################################################################

# URL da API
complete_url_forecast = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&appid={openweathermap_api_key}&units=metric&exclude=current,minutely,hourly,alerts"

# Request
response_forecast = requests.get(complete_url_forecast)

# JSON
z = response_forecast.json()

# Forecast
forecast = z["daily"]

# Dias da semana
days = [forecast[i]["dt"] for i in range(5)]

# Temperaturas
temperatures = [forecast[i]["temp"]["day"] for i in range(5)]
min_temperatures = [forecast[i]["temp"]["min"] for i in range(5)]
max_temperatures = [forecast[i]["temp"]["max"] for i in range(5)]

# Figura
fig = go.Figure()

# Temperatura média
fig.add_trace(go.Scatter(
    x=days,
    y=temperatures,
    mode='lines',
    name='Avg Temp',
    line=dict(color='black')
))

# Temperatura mínima
fig.add_trace(go.Scatter(
    x=days,
    y=min_temperatures,
    mode='lines',
    name='Min Temp',
    line=dict(color='rgb(26, 118, 255)')
))

# Temperatura máxima
fig.add_trace(go.Scatter(
    x=days,
    y=max_temperatures,
    mode='lines',
    name='Max Temp',
    line=dict(color='rgb(255, 65, 54)')
))

# Layout
fig.update_layout(
    title='Forecast Temperatures for Next 5 Days',
    xaxis=dict(
        title='Day of Week',
        titlefont_size=16,
        tickfont_size=14,
        tickvals=days,
        ticktext=[datetime.utcfromtimestamp(day).strftime('%A') for day in days]
    ),
    yaxis=dict(
        title='Temperature (C)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=1.0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
)

# Gráfico
st.plotly_chart(fig, use_container_width=True)

#################################################################################
#################################################################################



############################Data from Agurotech soil moisture sensor#############
#################################################################################


# Função para obter os dados do sensor
def get_sensor_data(farm_choice):
    farm_api_agurotech_ids = {
        #"Laverdonk":  "A70102A00112",
        "Schoonoord - Sugar Beet": "A70202A01004",
        "Schoonoord - Starch Potato": "A70102A00333",
        "Vijfhuizen - Tulip": "A70102A00517",
        "Lelystad (Fertigation trail) - Onions": "A70102A00311",
        "Mitselwier - Hybrid Potato": "A70102A00112",
        "Hengelo (Corridor) - Soy and Faba": "A70102A00060",
        "Erlecom - Potato": "A70102A00450",
        "Erlecom - Onion": "A70202A00883",
        "Veendam - Onion": "A70202A01013"
    }
    sensor_id = farm_api_agurotech_ids.get(farm_choice)
    if sensor_id is None:
        return None
    url = f'https://api.agurotech.com/v1/farms/P22du/sensor-data?sensor-id={sensor_id}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {agurotech_api_key}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['sensorData']

# Adicionando o botão para carregar os gráficos
if st.sidebar.button("Agurotech - Soil Moisture Sensor (realtime)"):
    sensor_data = get_sensor_data(farm_choice)

    if sensor_data is not None:
        dates = [datetime.strptime(entry['dateTime'], "%Y-%m-%dT%H:%M:%SZ") for entry in sensor_data if entry['depth'] == 15]
        vwc_values_15cm = [entry['vwc'] for entry in sensor_data if entry['depth'] == 15]
        vwc_values_30cm = [entry['vwc'] for entry in sensor_data if entry['depth'] == 30]

        # Encontrando os limites dos valores
        min_value = min(min(vwc_values_15cm), min(vwc_values_30cm))
        max_value = max(max(vwc_values_15cm), max(vwc_values_30cm))

        # Adicionando distanciamento de 5% nos valores mínimos e máximos
        min_value -= 0.5 * (max_value - min_value)
        max_value += 0.5 * (max_value - min_value)

        # Criando o gráfico com Plotly
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=dates, y=vwc_values_15cm, mode='lines', name='Depth 15cm', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=dates, y=vwc_values_30cm, mode='lines', name='Depth 30cm', line=dict(color='blue')))

        fig.update_layout(
            title='Agurotech Soil Moisture Sensor Data',
            xaxis=dict(title='Date Time'),
            yaxis=dict(title='Volumetric Water Content (%)', side='left', range=[min_value, max_value]),
            legend=dict(x=1, y=1.1)
        )

        st.plotly_chart(fig)
    else:
        st.write("Sensor data not available for the selected farm.")
        
js = '''
<script>
var body = window.parent.document.querySelector(".main");
console.log(body);
body.scrollTop = 0;
</script>
'''
st.components.v1.html(js)

#################################################################################
#################################################################################




############################NDVI - SATELLITE - Agromonitoring####################
#################################################################################

# Dicionário para mapear o nome da fazenda para o ID do polígono na API Agromonitoring
farm_api_agromonitoring_ids = {
    "Laverdonk":  "66196c0e1a451adbd4bec94b",
    "Schoonoord - Sugar Beet": "63ce5acfb98f961fd8cbe0ef",
    "Schoonoord - Starch Potato": "66196c7f7a336611ae3e3c58",
    "Vijfhuizen - Tulip": "661677b06352a3973b2cdde4",
    "Lelystad (Fertigation trail) - Onions": "66196cf27a3366ab913e3c59",
    "Mitselwier - Hybrid Potato": "66196d8c7fc9dc340a7721e4",
    "Hengelo (Corridor) - Soy and Faba": "66196de993997db055bfe52f",
    "Erlecom - Potato": "66196e226419597814d6529b",
    "Erlecom - Onion": "66196e541a451a2cb4bec94c",
    "Veendam - Onion": "666848e06419595476d65e0a"
}

# Função para fazer a chamada de API e obter os valores do solo
def obter_valores_solo(farm_choice):
    polyid = farm_api_agromonitoring_ids.get(farm_choice)
    if polyid is None:
        return None
    # URL do endpoint da API
    url = f"http://api.agromonitoring.com/agro/1.0/soil?polyid={polyid}&appid={agromonitoring_api_key}"
    # Fazendo a requisição GET para obter o JSON
    response = requests.get(url)
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        json_data = response.json()
        return json_data
    else:
        return None

# Função para fazer a chamada de API e obter as URLs das imagens NDVI a partir do JSON
def obter_urls_ndvi(start, end, polyid):
    urls = []
    # URL do endpoint da API
    url = f"http://api.agromonitoring.com/agro/1.0/image/search?start={start}&end={end}&polyid={polyid}&appid={agromonitoring_api_key}"
    # Fazendo a requisição GET para obter o JSON
    response = requests.get(url)
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        json_data = response.json()
        # Iterando sobre os resultados para obter as URLs das imagens NDVI
        for item in json_data:
            dt = item["dt"]
            ndvi_url = item["image"]["ndvi"]
            # Convertendo o timestamp para formato de data
            data_formatada = datetime.utcfromtimestamp(dt).strftime('%d-%m-%Y')
            urls.append((ndvi_url, data_formatada))
    return urls

def obter_urls_ndwi(start, end, polyid):
    urls = []
    # URL do endpoint da API
    url = f"http://api.agromonitoring.com/agro/1.0/image/search?start={start}&end={end}&polyid={polyid}&appid={agromonitoring_api_key}"
    # Fazendo a requisição GET para obter o JSON
    response = requests.get(url)
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        json_data = response.json()
        # Iterando sobre os resultados para obter as URLs das imagens NDVI
        for item in json_data:
            dt = item["dt"]
            ndwi_url = item["image"]["ndwi"]
            # Convertendo o timestamp para formato de data
            data_formatada = datetime.utcfromtimestamp(dt).strftime('%d-%m-%Y')
            urls.append((ndwi_url, data_formatada))
    return urls
    
# Definindo a data final como a data atual
data_final = datetime.now()
# Definindo a data inicial como 60 dias antes da data final
data_inicial = data_final - timedelta(days=30)

# Convertendo as datas para timestamps UNIX
start = int(data_inicial.timestamp())
end = int(data_final.timestamp())

# Adicionar um botão para carregar os gráficos na barra lateral
if st.sidebar.button("Satellite data - Agromonitoring"):

    
    # Obtém as URLs e datas das imagens NDVI a partir do endpoint da API
    polyid = farm_api_agromonitoring_ids.get(farm_choice)
    if polyid:
        urls_ndvi = obter_urls_ndvi(start, end, polyid)
    else:
        st.error("Polyid not found for selected farm.")
        urls_ndvi = []
    
    # Obtém as URLs e datas das imagens NDWI a partir do endpoint da API
    if polyid:
        urls_ndwi = obter_urls_ndwi(start, end, polyid)
    else:
        st.error("Polyid not found for selected farm.")
        urls_ndwi = []

    # Reverter a ordem das URLs para exibir o mapa mais recente primeiro
    urls_ndvi.reverse()
    
    # Reverter a ordem das URLs para exibir o mapa mais recente primeiro
    urls_ndwi.reverse()

    # Exibir as imagens NDVI em pares de 3 em 3
    st.header("Satellite data - Agromonitoring - NDVI-NDWI-SOIL-Last 30 days")

    st.subheader("Normalized Difference Vegetation Index (NDVI)")
    for i in range(0, len(urls_ndvi), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            if i < len(urls_ndvi):
                url, data_formatada = urls_ndvi[i]
                st.image(url, caption=f"Date: {data_formatada}", width=300)
        with col2:
            if i + 1 < len(urls_ndvi):
                url, data_formatada = urls_ndvi[i + 1]
                st.image(url, caption=f"Date: {data_formatada}", width=300)
        with col3:
            if i + 2 < len(urls_ndvi):
                url, data_formatada = urls_ndvi[i + 2]
                st.image(url, caption=f"Date: {data_formatada}", width=300)
           
                
    # Exibir as imagens NDWI em pares de 3 em 3
    st.subheader("Normalized Difference Water Index (NDWI)") 
    for i in range(0, len(urls_ndwi), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            if i < len(urls_ndwi):
                url, data_formatada = urls_ndwi[i]
                st.image(url, caption=f"Date: {data_formatada}", width=300)
        with col2:
            if i + 1 < len(urls_ndwi):
                url, data_formatada = urls_ndwi[i + 1]
                st.image(url, caption=f"Date: {data_formatada}", width=300)
        with col3:
            if i + 2 < len(urls_ndwi):
                url, data_formatada = urls_ndwi[i + 2]
                st.image(url, caption=f"Date: {data_formatada}", width=300)

    # Se os valores do solo forem obtidos com sucesso
    valores_solo = obter_valores_solo(farm_choice)
    if valores_solo:
        st.write("Soil Values:")
        day = datetime.utcfromtimestamp(valores_solo['dt']).strftime('%Y-%m-%d')
        t10_celsius = valores_solo.get('t10')
        moisture = valores_solo.get('moisture')
        t0_celsius = valores_solo.get('t0')
        
        if t10_celsius is not None:
            t10_celsius = t10_celsius - 273.15
        if t0_celsius is not None:
            t0_celsius = t0_celsius - 273.15

        # Criando as caixas simuladas com os valores dentro
        st.markdown(
            f"""
            <div style="background-color:#f0f0f0; padding:10px; border-radius:5px; text-align: center;">
                <h3 style="font-size: 20px;">Day: {day}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        if t10_celsius is not None:
            st.markdown(
                f"""
                <div style="background-color:#cce5ff; padding:10px; border-radius:5px; text-align: center;">
                    <h3 style="font-size: 20px;">Temperature on the 10 centimeters depth: {t10_celsius:.2f}°C</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        if moisture is not None:
            st.markdown(
                f"""
                <div style="background-color:#e6f2ff; padding:10px; border-radius:5px; text-align: center;">
                    <h3 style="font-size: 20px;">Soil moisture: {moisture:.3f} m³/m³</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        if t0_celsius is not None:
            st.markdown(
                f"""
                <div style="background-color:#b3d9ff; padding:10px; border-radius:5px; text-align: center;">
                    <h3 style="font-size: 20px;">Surface temperature: {t0_celsius:.2f}°C</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("Failed to obtain soil values. Check your connection or API key.")
        
        
js = '''
<script>
var body = window.parent.document.querySelector(".main");
console.log(body);
body.scrollTop = 0;
</script>
'''
st.components.v1.html(js)

        
#################################################################################
#################################################################################






###################################OPEN-METEO####################################
#################################################################################    

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import openmeteo_requests
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

if st.sidebar.button("Satellite data - Open-Meteo"):
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
    params = {
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain",
                   "evapotranspiration", "et0_fao_evapotranspiration", "soil_temperature_0cm",
                   "soil_temperature_6cm", "soil_temperature_18cm", "soil_moisture_0_to_1cm",
                   "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm",
                   "direct_radiation"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum",
                  "et0_fao_evapotranspiration"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                              end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                              freq=pd.Timedelta(seconds=hourly.Interval()), inclusive="left")
    }

    for i in range(len(params["hourly"])):
        variable_name = params["hourly"][i]
        values = hourly.Variables(i).ValuesAsNumpy()
        hourly_data[variable_name] = values

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Process daily data
    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                              end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                              freq=pd.Timedelta(seconds=daily.Interval()), inclusive="left")
    }

    for i in range(len(params["daily"])):
        variable_name = params["daily"][i]
        values = daily.Variables(i).ValuesAsNumpy()
        daily_data[variable_name] = values

    daily_dataframe = pd.DataFrame(data=daily_data)

    # Create subplots for grouped variables
    st.write("### Hourly Data")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=hourly_dataframe['date'], y=hourly_dataframe['evapotranspiration'], name='Evapotranspiration'))
    fig1.add_trace(go.Scatter(x=hourly_dataframe['date'], y=hourly_dataframe['et0_fao_evapotranspiration'], name='ET0 FAO Evapotranspiration'))
    fig1.update_layout(title_text='Evapotranspiration and Reference evapotranspiration (ET0/FAO) - per hour', xaxis_title='Days', yaxis_title='Millimeters (mm)')
    st.plotly_chart(fig1)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=hourly_dataframe['date'], y=hourly_dataframe['soil_temperature_0cm'], name='Soil Temperature 0cm'))
    fig2.add_trace(go.Scatter(x=hourly_dataframe['date'], y=hourly_dataframe['soil_temperature_6cm'], name='Soil Temperature 6cm'))
    fig2.add_trace(go.Scatter(x=hourly_dataframe['date'], y=hourly_dataframe['soil_temperature_18cm'], name='Soil Temperature 18cm'))
    fig2.update_layout(title_text='Soil temperature (satellite estimate)', xaxis_title='Days', yaxis_title='Celsius degree (°C)')
    st.plotly_chart(fig2)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=hourly_dataframe['date'], y=hourly_dataframe['soil_moisture_0_to_1cm'], name='Soil Moisture 0-1cm'))
    fig3.add_trace(go.Scatter(x=hourly_dataframe['date'], y=hourly_dataframe['soil_moisture_1_to_3cm'], name='Soil Moisture 1-3cm'))
    fig3.add_trace(go.Scatter(x=hourly_dataframe['date'], y=hourly_dataframe['soil_moisture_3_to_9cm'], name='Soil Moisture 3-9cm'))
    fig3.add_trace(go.Scatter(x=hourly_dataframe['date'], y=hourly_dataframe['soil_moisture_9_to_27cm'], name='Soil Moisture 9-27cm'))
    fig3.update_layout(title_text='Soil moisture (satellite estimate)', xaxis_title='Days', yaxis_title='Soil Moisture (m3/m3)')
    st.plotly_chart(fig3)
    
    st.write("### Daily Data")
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=daily_dataframe['date'], y=daily_dataframe['temperature_2m_max'], name='Temperature 2m Max'))
    fig4.add_trace(go.Scatter(x=daily_dataframe['date'], y=daily_dataframe['temperature_2m_min'], name='Temperature 2m Min'))
    fig4.update_layout(title_text='Temperature max and min (2m)', xaxis_title='Days', yaxis_title='Celsius degree (°C)')
    st.plotly_chart(fig4)

    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=daily_dataframe['date'], y=daily_dataframe['et0_fao_evapotranspiration'], name='ET0 FAO Evapotranspiration'))
    fig5.update_layout(title_text='Reference evapotranspiration (ET0/FAO) - per day', xaxis_title='Days', yaxis_title='Millimeters (mm)')
    st.plotly_chart(fig5)

    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(x=daily_dataframe['date'], y=daily_dataframe['precipitation_sum'], name='Precipitation Sum'))
    fig6.update_layout(title_text='Precipitation Sum', xaxis_title='Days', yaxis_title='Millimeters (mm)')
    st.plotly_chart(fig6)
    
    js = '''
    <script>
    var body = window.parent.document.querySelector(".main");
    console.log(body);
    body.scrollTop = 0;
    </script>
    '''
    st.components.v1.html(js)


    
    
#################################################################################
#################################################################################    



###########################VisualCrossing Weather parameters#####################
#################################################################################

def Get_Weather(latitude,longitude):
    latitude = str(latitude)
    longitude = str(longitude)

    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'+latitude+'%2C'+longitude+'?unitGroup=metric&key='+visualcrossing_api_key+'&contentType=json'

    r = requests.get(url)

    data = r.json()

    # Top Section: Overview
    st.subheader(f'Location: {data["resolvedAddress"]}')
    st.subheader(f'Timezone: {data["timezone"]}')

    # Next 15 Days Temperature
    st.header("Next 15 Days Temperature")
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[day['datetime'] for day in data['days']],
        y=[day['tempmin'] for day in data['days']],
        name='Minimum',
        marker_color='black'
    ))

    fig.add_trace(go.Bar(
        x=[day['datetime'] for day in data['days']],
        y=[day['temp'] for day in data['days']],
        name='Average',
        marker_color='rgb(26, 118, 255)'
    ))

    fig.add_trace(go.Bar(
        x=[day['datetime'] for day in data['days']],
        y=[day['tempmax'] for day in data['days']],
        name='Maximum',
        marker_color='rgb(255, 65, 54)'
    ))

    fig.update_layout(
        title='Next 15 Days Temperature',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Temperature (C)',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=1.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    st.plotly_chart(fig, use_container_width=True)

    # prec
    dew = [day['precip'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=dew, title='Precipitation - Next 15 Days')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Precipitation (mm)')
    st.plotly_chart(fig, use_container_width=True)


    # Dew
    dew = [day['dew'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=dew, title='Dew Point - Next 15 Days')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Dew (C)')
    st.plotly_chart(fig, use_container_width=True)

    # Humidity
    humidity = [day['humidity'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=humidity, title='Air Humidity - Next 15 Days')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Humidity (%)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Solar Radiation
    solarradiation = [day['solarradiation'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=solarradiation, title='24 Hours Solar Radiation Data')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Solar Radiation')
    st.plotly_chart(fig, use_container_width=True)
    

    # Pressure
    pressure = [day['pressure'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=pressure, title='24 Hours Pressure Data')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Pressure (Pa)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Sun Data
    sundata = [[day['datetime'], (datetime.fromtimestamp(day['sunriseEpoch']).strftime('%H:%M:%S')),
                (datetime.fromtimestamp(day['sunsetEpoch']).strftime('%H:%M:%S'))] for day in data['days']]
    sundata.insert(0, ["DATE", "SUN RAIS", "SUN SET"])
    fig = go.Figure(data=[go.Table(header=dict(values=["DATE", "SUN RAIS", "SUN SET"]), cells=dict(values=sundata))])
    st.plotly_chart(fig, use_container_width=True)
    
    # Wind Speed
    windspeed = [day['windspeed'] for day in data['days']]
    winddir = [day['winddir'] for day in data['days']]
    fig = go.Figure()
    fig.add_trace(go.Barpolar(
        r=windspeed,
        theta=winddir,
        name='Wind Speed',
        marker_color='rgb(55, 83, 109)'
    ))
    fig.update_layout(
        title='Wind Speed (Km/h)',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(windspeed)]
            )
        ),
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)



    # Cloud Cover
#    cloudcover = [day['cloudcover'] for day in data['days']]
#    fig = go.Figure()
#    fig.add_trace(go.Pie(
#        labels=[f"Date: {day['datetime']}" for day in data['days']],
#        values=cloudcover,
#        title='15 Days Cloud Cover Data',
#        textinfo='label+percent',
#        hole=.3,
#        marker=dict(
#            colors=px.colors.sequential.RdBu
#        )
#    ))
#    st.plotly_chart(fig, use_container_width=True)


##############side bar##############


container.text_input("Latitude:", value=latitude)
container.text_input("Longitude:", value=longitude)

if st.sidebar.button("Weather - 15 days forecast"):
    Get_Weather(latitude, longitude)
    js = '''
    <script>
    var body = window.parent.document.querySelector(".main");
    console.log(body);
    body.scrollTop = 0;
    </script>
    '''
    st.components.v1.html(js)
    
#################################################################################
#################################################################################


    
###########################Soil moisture by csv file#############################
#################################################################################


# Carregar os dados do arquivo CSV
#df = pd.read_csv("soil-moisture.csv")

#def plot_soil_moisture():
#    # Criar o gráfico com Plotly
#    fig = go.Figure()
#    fig.add_trace(go.Scatter(x=df['Date'], y=df['VWC_15_Agurotech'], mode='lines', name='VWC_15_Agurotech'))
#    fig.add_trace(go.Scatter(x=df['Date'], y=df['VWC_30_Agurotech'], mode='lines', name='VWC_30_Agurotech'))
#
#    fig.update_layout(title='Soil Moisture Values',
#                      xaxis_title='Date',
#                      yaxis_title='Soil Moisture',
#                      template='plotly_dark')

    # Exibir o gráfico
#    st.plotly_chart(fig)
    
#if st.sidebar.button("Soil Moisture Values - METER"):
#    plot_soil_moisture()
#    js = '''
#    <script>
#    var body = window.parent.document.querySelector(".main");
#    console.log(body);
#    body.scrollTop = 0;
#    </script>
#    '''
#    st.components.v1.html(js)
    

################################OTHER SIMULATIONS################################
#################################################################################



#################################################################################
#################################################################################



###############################Reflesh button for OpenWeatherMap#################
#################################################################################

#Manually refresh button
st.sidebar.button("Update current weather")
js = '''
<script>
var body = window.parent.document.querySelector(".main");
console.log(body);
body.scrollTop = 0;
</script>
'''
st.components.v1.html(js)

#################################################################################
#################################################################################





#################################End of the code#################################
#################################################################################


if __name__ == "__main__":
    main()

