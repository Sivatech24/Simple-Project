import streamlit as st
import pandas as pd

# Function to load CSV files from GitHub
def load_data(url):
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Error loading data from {url}: {e}")
        return None

# GitHub raw CSV links
plant_1_generation_url = 'https://raw.githubusercontent.com/Sivatech24/DataSetsForTheModel/0deb87623911b017969be1ab482da725a0ae720c/DataSetsCsvFiles/Plant_1_Generation_Data.csv'
plant_1_weather_url = 'https://raw.githubusercontent.com/Sivatech24/DataSetsForTheModel/0deb87623911b017969be1ab482da725a0ae720c/DataSetsCsvFiles/Plant_1_Weather_Sensor_Data.csv'
plant_2_generation_url = 'https://raw.githubusercontent.com/Sivatech24/DataSetsForTheModel/0deb87623911b017969be1ab482da725a0ae720c/DataSetsCsvFiles/Plant_2_Generation_Data.csv'
plant_2_weather_url = 'https://raw.githubusercontent.com/Sivatech24/DataSetsForTheModel/0deb87623911b017969be1ab482da725a0ae720c/DataSetsCsvFiles/Plant_2_Weather_Sensor_Data.csv'

# Load datasets
st.title('Solar Power Plant Data Overview')

st.subheader('Plant 1 Generation Data')
plant_1_generation_data = load_data(plant_1_generation_url)
if plant_1_generation_data is not None:
    st.write(plant_1_generation_data)

st.subheader('Plant 1 Weather Sensor Data')
plant_1_weather_data = load_data(plant_1_weather_url)
if plant_1_weather_data is not None:
    st.write(plant_1_weather_data)

st.subheader('Plant 2 Generation Data')
plant_2_generation_data = load_data(plant_2_generation_url)
if plant_2_generation_data is not None:
    st.write(plant_2_generation_data)

st.subheader('Plant 2 Weather Sensor Data')
plant_2_weather_data = load_data(plant_2_weather_url)
if plant_2_weather_data is not None:
    st.write(plant_2_weather_data)

# Display summary statistics
st.subheader('Summary Statistics')

if plant_1_generation_data is not None:
    st.write("Plant 1 Generation Data Summary:")
    st.write(plant_1_generation_data.describe())

if plant_1_weather_data is not None:
    st.write("Plant 1 Weather Sensor Data Summary:")
    st.write(plant_1_weather_data.describe())

if plant_2_generation_data is not None:
    st.write("Plant 2 Generation Data Summary:")
    st.write(plant_2_generation_data.describe())

if plant_2_weather_data is not None:
    st.write("Plant 2 Weather Sensor Data Summary:")
    st.write(plant_2_weather_data.describe())
