import streamlit as st
import pandas as pd
import requests
import pandas as pd
import json
import plotly.graph_objects as go
from PIL import Image

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
API_KEY = "863fff0d246f7e05e8db2e753f6d5740"


def get_lat_lon_from_city(city: str, api_key: str) -> (float, float):
    params = {
        'q': city,
        'appid': api_key
    }
    response = requests.get(WEATHER_URL, params=params)
    data = response.json()
    
    if data.get('cod') == 200:  # Check if API call was successful
        return data['coord']['lat'], data['coord']['lon']
    else:
        return None, None

def get_weather_forecast(lat: float, lon: float, api_key: str) -> dict:
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'appid': api_key
    }
    response = requests.get(FORECAST_URL, params=params)
    return response.json()


def json_to_dataframe(json_data):
    # Extract the desired fields from the 'list' key in the JSON
    forecast_list = json_data['list']
    
    data = {
        'dt_txt': [entry['dt_txt'] for entry in forecast_list],
        'temp': [entry['main']['temp'] for entry in forecast_list],
        'temp_min': [entry['main']['temp_min'] for entry in forecast_list],
        'temp_max': [entry['main']['temp_max'] for entry in forecast_list],
        'description': [entry['weather'][0]['description'] for entry in forecast_list],
        'speed': [entry['wind']['speed'] for entry in forecast_list],
        'direction': [entry['wind']['deg'] if 'deg' in entry['wind'] else None for entry in forecast_list],
        'sea_level': [entry['main']['sea_level'] for entry in forecast_list if 'sea_level' in entry['main']],
        'grnd_level': [entry['main']['grnd_level'] for entry in forecast_list if 'grnd_level' in entry['main']]
    }
    
    # Handle cases where sea_level or grnd_level might be missing
    if 'sea_level' not in data:
        data['sea_level'] = [None] * len(forecast_list)
    if 'grnd_level' not in data:
        data['grnd_level'] = [None] * len(forecast_list)

    df = pd.DataFrame(data)
    df['direction'] = df.get('direction', pd.Series([None]*len(df))).apply(to_textual_description)
    return df

def getweather(city: str):
    params = {
        'q': city,
        'appid': API_KEY
    }
    result = requests.get(WEATHER_URL, params=params)
    
    if result.status_code == 200:
        json_data = result.json()
        country = json_data['sys']['country']
        temp = json_data['main']['temp'] - 273.15
        temp_feels = json_data['main']['feels_like'] - 273.15
        humid = json_data['main']['humidity']
        icon = json_data['weather'][0]['icon']
        lon = json_data['coord']['lon']
        lat = json_data['coord']['lat']
        des = json_data['weather'][0]['description']
        res = [country, round(temp,1), round(temp_feels,1), humid, lon, lat, icon, des]
        return res, json_data
    else:
        st.write("Error in search!")
        return None, None
    
def highlight_high_wind(val):
    """
    Highlights in red the values that are greater than 10.
    """
    color = 'red' if val > 5 else 'black'
    return 'color: %s' % color

def set_background(img_path):
    st.markdown(
        f"""
        <style>
        body {{
            background-image: url({img_path});
            background-size: cover;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
def to_textual_description(degree):
    if degree is None:
        return None
    if degree > 337.5:
        return 'Northerly'
    if degree > 292.5:
        return 'North Westerly'
    if degree > 247.5:
        return 'Westerly'
    if degree > 202.5:
        return 'South Westerly'
    if degree > 157.5:
        return 'Southerly'
    if degree > 122.5:
        return 'South Easterly'
    if degree > 67.5:
        return 'Easterly'
    if degree > 22.5:
        return 'North Easterly'
    return 'Northerly'

    
st.set_page_config(layout="wide")

#image1 = Image.open("C:\Users\sisma\Downloads\OpenWeather.png")

#st.image(image1)

# Call the function with the path of your image
set_background("C:\\Users\\sisma\\Documents\\maritime.jpeg")




st.title("Weather Forecast App")


# Define a dictionary of city groupings
city_groupings = {
    ("Kavala", "Thessaloniki"): ["Ierissos", "Stavros", "Thassos"],
    # You can add more groupings as needed
    # ("CityA", "CityB"): ["CityX", "CityY"],
}

cities_input = st.text_area("Enter City Names (comma separated):")

if cities_input:
    cities = [city.strip() for city in cities_input.split(',')]
    
    # Check if any city groupings match the user's input
    for city_pair, additional_cities in city_groupings.items():
        if all(city in cities for city in city_pair):
            cities.extend(additional_cities)

    # Remove duplicates if any
    cities = list(set(cities))



    #Lists to store latitudes and longitudes for the cities
    lats, lons = [], []
    for city in cities:
        lat, lon = get_lat_lon_from_city(city, API_KEY)
        if lat and lon:  # Check if coordinates are available
            lats.append(lat)
            lons.append(lon)
    
    # Convert coordinates to DataFrame and display on map
    coords_df = pd.DataFrame({'lat': lats, 'lon': lons})
    st.map(coords_df)
    for city in cities:
        
        res, json_data = getweather(city)
        col1, col2, col3, col4 = st.columns(4)
        if res:
            col1.subheader(city.capitalize())
            col2.success('Current: ' + str(res[1]))
            col3.info('Feels Like: ' + str(res[2]))
            col4.info('Humidity: ' + str(res[3]))
            col1.subheader('Status: ' + res[7])
            web_str = "![Alt Text](http://openweathermap.org/img/wn/" + str(res[6]) + "@2x.png)"
            col1.markdown(web_str)
            lat, lon = get_lat_lon_from_city(city, API_KEY)
        forecast_data = get_weather_forecast(lat, lon, API_KEY)
        
        
        formatted_json = json.dumps(forecast_data, indent=4)
        #st.code(formatted_json, language="json")
        df = json_to_dataframe(forecast_data)
        for index, row in df.iterrows():
            if row['speed'] > 5:
                st.warning(f"High wind speed alert for date {row['dt_txt']} in {city.capitalize()}! Speed: {row['speed']} m/s")
        styled_df = df.style.applymap(highlight_high_wind, subset=['speed']).render()

        with st.expander("Last 5 Days History Every 3 Hours"):
                st.dataframe(df)# Display the dataframe in Streamlit
                #st.write(styled_df, unsafe_allow_html=True)
       
        metric = st.selectbox("Select Metric for Chart", ["Temperature", "Wind Speed"], key=f"metric_select_{city}")
            
        if metric == "Temperature":
            temp = [entry['main']['temp'] for entry in forecast_data['list']]
            temp_min = [entry['main']['temp_min'] for entry in forecast_data['list']]
            temp_max = [entry['main']['temp_max'] for entry in forecast_data['list']]
            
            dates = [entry['dt_txt'] for entry in forecast_data['list']]
            
            df = pd.DataFrame({
                'Date': dates,
                'Temperature': temp,
                'Min Temperature': temp_min,
                'Max Temperature': temp_max
            })
            st.line_chart(df.set_index('Date'), use_container_width=True)
        elif metric == "Wind Speed":
            values = [entry['wind']['speed'] for entry in forecast_data['list']]
            dates = [entry['dt_txt'] for entry in forecast_data['list']]
            
            df = pd.DataFrame({
                'Date': dates,
                metric: values
            })
            st.line_chart(df.set_index('Date'), use_container_width=True)
