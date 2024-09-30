# Weather Forecast App ☁️🌧️🌞

An interactive weather forecast application built using Streamlit and OpenWeatherMap API. This app allows users to search for weather information by entering city names and visualizes the weather forecast for the next few days with interactive charts and maps. It also provides alerts for specific conditions such as high wind speeds.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Information](#api-information)
- [City Groupings](#city-groupings)
- [Weather Alerts](#weather-alerts)
- [Project Structure](#project-structure)
- [Background Image Customization](#background-image-customization)
- [Future Improvements](#future-improvements)
- [Acknowledgments](#acknowledgments)

---

## Overview

The **Weather Forecast App** is designed to help users easily access current and forecasted weather data for multiple cities. By integrating OpenWeatherMap API, this app provides:
- Current weather details.
- Forecast for the next few days (every 3 hours).
- Visualization through line charts and maps.

![App Screenshot](https://your_image_url_here.png)

---

## Features

- **Current Weather Information**: Get the real-time temperature, "feels like" temperature, and humidity for any city.
- **Forecast Charts**: View temperature and wind speed forecasts for the upcoming days with line charts.
- **Wind Speed Alerts**: Warnings for high wind speeds above a certain threshold (5 m/s in this case).
- **City Groupings**: Automatically includes additional related cities based on predefined groupings.

---

## Installation

To run this application locally, please follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/weather-forecast-app.git
    cd weather-forecast-app
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

---

## Usage

1. Enter the city names separated by commas in the input box.
2. The app will fetch and display the current weather details, including temperature, humidity, and description.
3. Visualize the weather forecast for the next 5 days, updated every 3 hours, in the form of charts and maps.
4. Check for alerts related to high wind speeds.

---

## API Information

This app uses the **OpenWeatherMap API** to retrieve weather data. Make sure you have your own API key:

1. Register at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up).
2. Obtain your API key and replace it in the `API_KEY` variable in `app.py`.

---

## City Groupings

The app includes a unique feature where entering certain city combinations automatically adds related cities to the search:

For example:
- Entering `Kavala` and `Thessaloniki` together will also include `Ierissos`, `Stavros`, and `Thassos`.

To add more groupings, edit the `city_groupings` dictionary in `app.py`.

---

## Weather Alerts

A feature of this app is to display alerts based on weather conditions. The current setting provides warnings when:
- **Wind Speed**: If the wind speed is greater than 5 m/s, a warning will be displayed for that specific time period.

You can customize the alert threshold in the function `highlight_high_wind`.

---

## Project Structure

```markdown
- `app.py`                 : The main application code for the weather forecast app.
- `requirements.txt`       : Python dependencies required to run the app.
- `README.md`              : Project description and setup instructions.
- `assets/`                : Folder for storing background images or any other media files.
