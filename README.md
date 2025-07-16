# Analyzing the 2025 LA Wildfires using NASA's PACE Data

## Overview

This repository is used to help analyze the effects of the 2025 Los Angeles Wildfires on the environment (land, ocean, and atmosphere). It uses data from NASA's Plankton, Aerosol, Cloud ocean Ecosystem (PACE) satellite, focusing on the Ocean Color Instrument (OCI) to see how the wildfires affected chlorophyll-a concentrations in the ocean, pollutants in the atmophere, and land vegetation. Additional weather, air quality index, and chlorophyll-a data were used to suppliment the analysis.

The fires started on January 7th, 2025, and were contained on January 31, 2025. Analysis was mainly done in the Pacific Palisades with bounding box: (-118.75, 33.9, -118.45, 34.15), using data from January to May of 2025.
<img width="1320" height="1080" alt="image" src="https://github.com/user-attachments/assets/fa050514-2da6-4a18-8d3f-656dd402769a" />

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

- The `la_fires_analysis.ipynb` notebook analyzes PACE OCI data from the BGC (biogechemcial), AOP (apparent optical properties), and LANDVI (land vegetation indices) suites.

- The `weather_analysis.ipynb` notebook analyzes the NOAA weather data, looking at preciptation, wind, smoke, and temperature before, during, and after the fires.

- The `aqi_data_analysis.ipynb` notebook looks at pollutants related to the fire with data downloaded from the EPA.

- The `combined_analysis.ipynb` notebook analyzes weather, air quality, and satellite data together to get a better picture of the effects of the wildfires on the surrounding environment.

## Overlay Plots
Overlay images of NDVI (land vegetation), and aerosol optical thickness, and chlorophyll-a over time. Chlorophyll-a concentrations seem to decrease and then increase.
<img width="5304" height="3268" alt="image" src="https://github.com/user-attachments/assets/2da43f00-7f26-4507-b245-6ec3c733465e" />

## Weather Data
There were a few days of precipitation in late January and a few days in February, March, and April.

<img width="985" height="490" alt="image" src="https://github.com/user-attachments/assets/580774b1-34bb-4954-9fea-5f46a13a453a" />

Winds are typically in the South / Southwest direction, but on the day the fires started, there were abnormally strong winds in the North direction.

<img width="568" height="569" alt="image" src="https://github.com/user-attachments/assets/845ebe5b-ca64-4eab-97dd-c485c593da03" />
<img width="1064" height="470" alt="image" src="https://github.com/user-attachments/assets/4881a6ff-8f5d-460d-8eb1-4cb818e2aef1" />

## Pollutants
Concentrations of CO, NO2, Ozone, PM10, and PM2.5 on a log-scale. There are large increases in particulate matter concentrations after the start of the fire and decreases during rainy periods.

<img width="1389" height="590" alt="image" src="https://github.com/user-attachments/assets/c6b04bb2-68ac-40d2-a1f6-30299f7947b3" />

## PACE Data
### Chlorophyll-a Concentrations
Trends in the smoothed average of PACE and MODIS chlorophyll-a concentrations. Chlorophyll declines initially after the fire, possibly due to atmospheric pollutants blocking sunlight, and increases after rains, likely due to runoff entering the ocean.

<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/35642262-3706-4167-8970-42aa9ebad0c6" />

### Chlorophyll-a and Particulate Matter Concentrations
A time series connected plot of chlorophyll-a and particulate matter concentrations in January. The loop from January 7-18 indicates a delayed effect of particulate matter (smoke) decreasing photosynthesis and chlorophyll-a levels.

<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/4c801a25-5362-40a6-b908-e26032f8c863" />

### Land Vegetation Indices
A time series plot of daily measurements of land vegetation indices. NDVI declines during the fire and NDII and NDWI spike during rain events.

<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/379a295a-584c-43be-bf14-200779ec87f9" />

Changes in NDVI Over Time. During the fire, there is a noticeable decline in vegetation in the fire zone (red circle). A few months later in April, the vegetation is still in recovery.

<img width="1467" height="429" alt="image" src="https://github.com/user-attachments/assets/54e607d3-1005-4b39-abc2-3a6d760c53b2" />

## Summary of Findings
The wildfire spanned from January 7 to 31, and several rain events occurred between January and April. Particulate matter levels in the atmosphere rose sharply, peaking on January 8, and returned to pre-fire levels within approximately a week. The presence of smoke likely reduced sunlight reaching the ocean surface, leading to a delayed decline in chlorophyll-a concentrations. Toward the end of the fire and in the weeks following, a combination of south/southwest winds and rainfall likely transported nutrient-rich runoff into the ocean, stimulating phytoplankton growth and contributing to a rise in chlorophyll-a concentrations. This runoff may have also supported early regrowth of land vegetation. While some vegetation has shown signs of recovery, the affected areas remain in the early stages of post-fire regeneration.


