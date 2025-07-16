# Analyzing the 2025 LA Wildfires using NASA's PACE Data

## Overview

This repository is used to help analyze the effects of the 2025 Los Angeles Wildfires on the environment (land, ocean, and atmosphere). It uses data from NASA's Plankton, Aerosol, Cloud ocean Ecosystem (PACE) satellite, focusing on the Ocean Color Instrument (OCI) to see how the wildfires affected chlorophyll-a concentrations in the ocean, pollutants in the atmophere, and land vegetation. Additional weather, air quality index, and chlorophyll-a data were used to suppliment the analysis.

## Setup

- Clone the repository

- Set up a virtual environment and install the dependencies in `requirements.txt`

### Downloading Data
- Create an earthaccess account to download the data (https://urs.earthdata.nasa.gov/users/new)

- Uncomment code to download PACE data in `scripts/download_data.py`. The data should be downloaded into a `/data/` directory.

- Download weather data from the National Oceanic and Atmosphere Admistration (NOAA) Climate Data Online Search using the following search terms and add the downloaded CSV file to the `/data/` directory:
    - Weather Observation Type/Dataset: Daily Summaries
    - Date Range: 2025-01-01 to 2025-05-01
    - Search For: Stations
    - Enter a Search Term: Santa Monica Municipal Airport, CA US
- Download Air Quality Index (AQI) data from the United States Environmental Protection Agency (EPA) for PM2.5, PM10, NO2, CO, and Ozone in 2025 from the Los Angeles-North Main Street local station
    - Add the files to the `/data/` directory (https://www.epa.gov/outdoor-air-quality-data/download-daily-data) and name them `LA_CO_2025.csv`, `LA_NO2_2025.csv`, `LA_ozone_2025.csv`, `LA_PM10_2025.csv`, `LA_PM25_2025.csv`.

## Visualizations

To create visualizations of NASA PACE data, run the following scripts to generate visualizations in the `/images/` directory:

- Run the `scripts/plot_{...}_data.py` files to generate images of each variable over the area of interest.

- Run the `scripts/overlay_plot.py` file to generate overlay plots of land vegetation, chlorophyll, and aerosol data.

- In `scripts/create_gif.py`, create GIFs of the images in a particular directory by changing the path passed in to the `create_gif` function.

## Notebooks

The `la_fires_analysis.ipynb` notebook analyzes PACE OCI data from the BGC (biogechemcial), AOP (apparent optical properties), and LANDVI (land vegetation indices) suites.

The `weather_analysis.ipynb` notebook analyzes the NOAA weather data, looking at preciptation, wind, smoke, and temperature before, during, and after the fires.

The `aqi_data_analysis.ipynb` notebook looks at pollutants related to the fire with data downloaded from the EPA.

The `combined_analysis.ipynb` notebook analyzes weather, air quality, and satellite data together to get a better picture of the effects of the wildfires on the surrounding environment.