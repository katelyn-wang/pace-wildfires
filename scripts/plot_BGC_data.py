import os
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime


def plot_chlor_a(ds: xr.Dataset, date_str: str=""):
    """
    Plots chlorophyll-a concentrations on a plot with latitude / longitude.
    Log transforms the chlorophyll concentration for better visualization.
    Saves an image of the plot in a subdirectory.

    Params:
        ds: an xarray dataset that includes merged data of the variable of interest
            with latitude and longitude coordinates
        date_str: a string in the format mm-dd-yyyy to indicate the date of the data
    """
    chlor_a = ds['chlor_a']  # Chlorophyll-a variable
    lon = ds['longitude']
    lat = ds['latitude']

    # log transform chlorophyll-a concentration
    log_chlor = np.log(chlor_a)

    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    plt.pcolormesh(lon, lat, log_chlor, cmap='viridis', shading='auto', transform=ccrs.PlateCarree())
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    gl.top_labels = False  # Remove top labels
    gl.right_labels = False  # Remove right labels

    plt.colorbar(label=f"Log of Chlorophyll-a (mg/m³)")
    plt.title(f"Chlorophyll-a Concentration {date_str}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    chlor_a_dir = _create_image_subdir('chlor_a')
    plt.savefig(chlor_a_dir / date_str)
    plt.close()

def plot_particulate_organic_carbon(ds: xr.Dataset, date_str: str=""):
    """
    Plots particulate organic carbon (POC) concentrations on a plot with latitude / longitude.
    Saves an image of the plot in a subdirectory.

    Params:
        ds: an xarray dataset that includes merged data of the variable of interest
            with latitude and longitude coordinates
        date_str: a string in the format mm-dd-yyyy to indicate the date of the data
    """
    poc = ds['poc']  # Particulate Organic Carbon variable
    lon = ds['longitude']
    lat = ds['latitude']

    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    plt.pcolormesh(lon, lat, poc, cmap='cividis', shading='auto', transform=ccrs.PlateCarree())
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    gl.top_labels = False  # Remove top labels
    gl.right_labels = False  # Remove right labels

    plt.colorbar(label=f"Particulate Organic Carbon (mg/m³)")
    plt.title(f"POC Concentration {date_str}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    poc_dir = _create_image_subdir("poc")
    plt.savefig(poc_dir / date_str)
    plt.close()

def plot_phytoplankton_carbon(ds: xr.Dataset, date_str: str=""):
    """
    Plots phytoplankton carbon concentrations on a plot with latitude / longitude.
    Saves an image of the plot in a subdirectory.

    Params:
        ds: an xarray dataset that includes merged data of the variable of interest
            with latitude and longitude coordinates
        date_str: a string in the format mm-dd-yyyy to indicate the date of the data
    """
    carbon_phyto = ds['carbon_phyto']
    lon = ds['longitude']
    lat = ds['latitude']

    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    plt.pcolormesh(lon, lat, carbon_phyto, cmap='plasma', shading='auto', transform=ccrs.PlateCarree())
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    gl.top_labels = False  # Remove top labels
    gl.right_labels = False  # Remove right labels

    plt.colorbar(label=f"Phytoplankton Carbon (mg/m³)")
    plt.title(f"Phytoplankton Carbon Concentration {date_str}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    carbon_phyto_dir = _create_image_subdir("carbon_phyto")
    plt.savefig(carbon_phyto_dir / date_str)
    plt.close()

def print_metadata(file_path: Path):
    """Prints data variables and attributes of a downloaded file of PACE data"""
    ds = xr.open_dataset(file_path, group="geophysical_data")
    print(ds.attrs)
    print(ds.variables)

def open_file_as_xr(file_path: Path, var_of_interest: str):
    """
    Given a file path to PACE data, creates an xarray dataset with a variable
    of interest merged with corresponding latitude and longitude coordinates.

    Params:
        file_path (Path): a file path to downloaded PACE data
        var_of_interest (str): A string of the variable of interest in the data

    Returns:
        dataset: an xarray dataset with the variable of interest and lat/lon coorindates
    """
    # Include group="geophysical_data" to merge data from different layers and access the variables
    ds = xr.open_dataset(file_path, group="geophysical_data")
    variable = ds[var_of_interest]

    # Open using group="navigation_data" to get the latitude and longitude
    dataset = xr.open_dataset(file_path, group="navigation_data")
    dataset = dataset.set_coords(("longitude", "latitude"))

    # Merge the coordinates and variable of interest
    dataset = xr.merge((variable, dataset.coords))
    # print(dataset)
    return dataset

def _create_image_subdir(subdir_name: str):
    """
    Helper function to create a subdirectory in the /images folder to save figures in.

    Params:
        subdir_name (str): the name for the subdirectory
    Returns:
        Path: The path to the subdirectory
    """
    images_dir = Path("images")
    os.makedirs(images_dir, exist_ok=True)
    subdir = images_dir / subdir_name
    os.makedirs(subdir, exist_ok=True)
    return subdir

def _extract_date_from_file(file_path: Path, output_format:str ="%m-%d-%Y"):
    """
    Given a file path for downloaded PACE data, extracts the date
    and returns it as a string with the specified output format.

    Params:
        file_path: the file path to downloaded PACE data
        output_format: the desired format of the returned date string

    Returns:
        str: a date string from the file with the specified format
    """
    try:
        date_string = file_path.name.split(".")[1][:8]
        date_object = datetime.strptime(date_string, "%Y%m%d")
        formatted_date = date_object.strftime(output_format)
        return formatted_date
    except ValueError:
        print(f"Error extracting the date from {file_path}")
        return None

def plot_from_file(file_path: Path, var: str, plot_funct=plot_chlor_a):
    """
    Plots a variable of interest from a data file using a specific plot function.

    Params:
        file_path: a path to the data file
        var: the variable of interest from the data to be plotted
        plot_funct: the plot function corresponding to the variable of interest
    """
    ds = open_file_as_xr(file_path, var)
    date_str = _extract_date_from_file(file_path)
    plot_funct(ds, date_str)

def plot_BGC_data(bgc_directory: Path):
    """
    Plots chlorophyll-a, particulate organic carbon, and phytoplankton carbon concentrations
    for all the downloaded Level 2 BGC data in the given directory.\\\

    Params:
        bgc_directory: a path to a directory containing PACE OCI L2 BGC downloaded data
    """
    for file in os.listdir(bgc_directory):
        file_path = bgc_directory / file
        print("Plotting chlorophyll-a")
        plot_from_file(file_path, 'chlor_a', plot_chlor_a)
        print("Plotting particulate organic carbon")
        plot_from_file(file_path, 'poc', plot_particulate_organic_carbon)
        print("Plotting phytoplankton carbon")
        plot_from_file(file_path, 'carbon_phyto', plot_phytoplankton_carbon)


if __name__ == '__main__':
    """
    This script assumes the relevant data is already downloaded using `download_data.py`
    (Data with the shortname 'PACE_OCI_L2_BGC_NRT')

    PACE: Plankton, Aerosol, Cloud, and ocean Ecosystem
    OCI: Ocean Color Instrument
    BGC: (Ocean) Biogeochemistry

    Level 2 BGC Data Products:
        chlor_a: Cholorophyll-a concentration
        poc: Particulate Organic Carbon
        carbon_phyto: Phytoplankton Carbon
    """

    ## Uncomment to view metadata about the BGC data
    # bgc_file = "data\\PACE_OCI_L2_BGC_NRT\\PACE_OCI.20250104T202321.L2.OC_BGC.V3_0.NRT.nc"
    # print_metadata(bgc_file)

    # TODO: make the colorbars all on the same scale

    # Plot OCI Level 2 BGC data:
    # Plots for cholorophyll-a, particulate organic carbon, and phytoplankton carbon
    bgc_dir = Path("data\\PACE_OCI_L2_BGC_NRT")
    plot_BGC_data(bgc_dir)
