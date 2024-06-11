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
import requests
import plotly.express as px
from api_keys import openweathermap_api_key, visualcrossing_api_key, vaimee_api_key

st.set_page_config(page_title="Agrifirm@AquaSim", layout="wide")

readme = load_config("config_readme.toml")


# Info
st.title("AquaSim Project - Farm: Chile - Tulips")


########################login################################
# Função para carregar imagem
def load_image(image_path):
    return Image.open(image_path)

def main():
    # Página de login
    st.sidebar.image(load_image("logo2.png"), use_column_width=True)

##############################fazendas e barra lateral#######################################

# Add the select bar in the sidebar
st.sidebar.image(load_image("logo1.png"), use_column_width=True)
display_links(readme["links"]["repo"], readme["links"]["other_link"])

with st.sidebar:
    st.markdown("<p style='text-align: center; font-size: 24px;'><b>Chile - Tulips</b></p>", unsafe_allow_html=True)
    farm_choice = "Chile - Tulip"



# Create a container in the main section for the weather data
#st.write("Weather Data")
container = st.container()

# fazendas que serao usadas no AquaSim
if farm_choice == "Chile - Tulip":
    farm_geojson_path = 'farms/chile.geojson'
    latitude, longitude = -40.189752825293375,-72.76902534843967
    farm_zoom = 14  # Zoom level for Chile - Tulip
    
    
############################soil map########################################


#st.write("Mapa de solo")

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


##############################################OpenWeatherMap#################################

openweathermap_api_key = 'cde2fcfca5966aeec3658751726d8f99'
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


################data e imagem do clima######################

import streamlit as st
from datetime import datetime

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

################i######################

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

################grafico com forecast de 5 dias ################################

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

###############################irrigation#######################

# Dicionário para mapear o nome da fazenda para o ID da API
farm_api_ids = {
    "Flevoland - Onion": "Flevoland_1682603796158",
    "Chile - Tulip": "unitChile1_nosensor_1697475160557"
}

# Função para fazer a chamada à API e retornar os dados em um DataFrame
def get_api_data(farm_choice):
    farm_api_id = farm_api_ids.get(farm_choice)
    if farm_api_id is None:
        return None
    url = f"https://api.criteria.vaimee.com/v1/criteria/forecast/{farm_api_id}"
    headers = {
        "accept": "application/json",
        "x-api-key": vaimee_api_key  # Use a chave importada da variável
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return pd.DataFrame(data["forecast"])
    
    

# Função para formatar os dados para plotar o gráfico
def format_data_for_plot(df):
    df["dt_txt"] = pd.to_datetime(df["dt_txt"]).dt.strftime("%Y-%m-%d")
    df = df[["dt_txt", "IrrigationNeeds","SurfaceWaterContent", "SoilWaterContent15", "SoilWaterContent30", 
             "SoilWaterContent50", "WaterPotential15", "WaterPotential30", "WaterPotential50", "Et0", "LeafAreaIndex", "RootDepth", 
             ]]
    df["SoilWaterContent15"] = pd.to_numeric(df["SoilWaterContent15"], errors='coerce') * 100  # Convertendo para numérico e multiplicando por 100
    df["SoilWaterContent30"] = pd.to_numeric(df["SoilWaterContent30"], errors='coerce') * 100  # Convertendo para numérico e multiplicando por 100
    df["SoilWaterContent50"] = pd.to_numeric(df["SoilWaterContent50"], errors='coerce') * 100  # Convertendo para numérico e multiplicando por 100
    return df

             
# Função para plotar o gráfico
def plot_graph(data, parameter, graph_type):
    fig = go.Figure()
    if graph_type == "line":
        fig.add_trace(go.Scatter(x=data["dt_txt"], y=data[parameter], mode="lines+markers", connectgaps=True))
    elif graph_type == "bar":
        fig.add_trace(go.Bar(x=data["dt_txt"], y=data[parameter]))
    fig.update_layout(title=f"{parameter} - Forecast for the next 3 days", xaxis_title="Dia-Mês", yaxis_title=get_yaxis_label(parameter))
    st.plotly_chart(fig)

# Função para obter o rótulo do eixo y de acordo com o parâmetro
def get_yaxis_label(parameter):
    labels = {
        "IrrigationNeeds": "Irrigation water needs [mm]",
        "SurfaceWaterContent": "Surface water content [mm]",
        "SoilWaterContent15": "Volumetric water content [%]",
        "SoilWaterContent30": "Volumetric water content [%]",
        "SoilWaterContent50": "Volumetric water content [%]",
        "WaterPotential15": "Water potential [kPa]",
        "WaterPotential30": "Water potential [kPa]",
        "WaterPotential50": "Water potential [kPa]",
        "RootDepth": "Root depth [m]",
        "Et0": "Reference evapotranspiration [mm]",
        "LeafAreaIndex": "Leaf area index [m2 m-2]"
    }
    return labels.get(parameter, "Valor")

# Carregar os dados da API
api_data = get_api_data(farm_choice)

# Adicionar um botão para carregar os gráficos
if st.sidebar.button("CRITERIA - 3 days forecast"):
    for parameter in ["IrrigationNeeds","SurfaceWaterContent", "SoilWaterContent15", "SoilWaterContent30", 
                      "SoilWaterContent50", "WaterPotential15", "WaterPotential30", "WaterPotential50", "Et0", "LeafAreaIndex", "RootDepth"]:
        formatted_data = format_data_for_plot(get_api_data(farm_choice))
        plot_graph(formatted_data, parameter, "line")
        js = '''
        <script>
        var body = window.parent.document.querySelector(".main");
        console.log(body);
        body.scrollTop = 0;
        </script>
        '''
        st.components.v1.html(js)


###############################irrigation - first page#######################

#st.write("Irrigation forecast - next 3 days")

formatted_data1 = format_data_for_plot(api_data)

def plot_line_chart(data, parameter):
    fig = go.Figure(go.Scatter(x=data["dt_txt"], y=data[parameter], mode="lines+markers", name=parameter))
    fig.update_layout(title=f"{parameter} - Forecast for the next 3 days", xaxis_title="Dia-Mês", yaxis_title=get_yaxis_label(parameter))
    st.plotly_chart(fig)
    
plot_line_chart(formatted_data1, "IrrigationNeeds")

######################################################


###############################botao de reflesh#######################

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

########################################################temperature pelo VisualCrossing###################################

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
    
    # Visibility
    visibility = [day['visibility'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=visibility, title='24 Hours Visibility Data')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Visibility')
    st.plotly_chart(fig, use_container_width=True)

    # Pressure
    pressure = [day['pressure'] for day in data['days']]
    fig = px.line(x=[day['datetime'] for day in data['days']], y=pressure, title='24 Hours Pressure Data')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Pressure (Pa)')
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


    # Sun Data
    sundata = [[day['datetime'], (datetime.fromtimestamp(day['sunriseEpoch']).strftime('%H:%M:%S')),
                (datetime.fromtimestamp(day['sunsetEpoch']).strftime('%H:%M:%S'))] for day in data['days']]
    sundata.insert(0, ["DATE", "SUN RAIS", "SUN SET"])
    fig = go.Figure(data=[go.Table(header=dict(values=["DATE", "SUN RAIS", "SUN SET"]), cells=dict(values=sundata))])
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



###########################side bar##########################################

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
    
###########################soil moisture by csv file############################

# Carregar os dados do arquivo CSV
df = pd.read_csv("soil-moisture.csv")

def plot_soil_moisture():
    # Criar o gráfico com Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['VWC_15_Agurotech'], mode='lines', name='VWC_15_Agurotech'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['VWC_30_Agurotech'], mode='lines', name='VWC_30_Agurotech'))

    fig.update_layout(title='Soil Moisture Values',
                      xaxis_title='Date',
                      yaxis_title='Soil Moisture',
                      template='plotly_dark')

    # Exibir o gráfico
    st.plotly_chart(fig)
    
if st.sidebar.button("Soil Moisture Sensor - Realtime"):
    plot_soil_moisture()
    js = '''
    <script>
    var body = window.parent.document.querySelector(".main");
    console.log(body);
    body.scrollTop = 0;
    </script>
    '''
st.components.v1.html(js)
    
###############################barra lateral#######################

    


if __name__ == "__main__":
    main()

