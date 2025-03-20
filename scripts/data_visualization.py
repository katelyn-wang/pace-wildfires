import os
import sys
import earthaccess
import matplotlib.pyplot as plt
import xarray as xr

from pathlib import Path
from datetime import datetime

sys.path.append(".")
from src.downloader.pace_data_downloader import PaceDataDownloader


def _create_image_subdir(subdir_name: str):
    """
    Helper function to create a subdirectory in the /images folder to save figures in.

    Args:
        subdir_name (str): the name for the subdirectory
    Returns:
        Path: The path to the subdirectory
    """
    images_dir = Path("images")
    os.makedirs(images_dir, exist_ok=True)
    subdir = images_dir / subdir_name
    os.makedirs(subdir, exist_ok=True)
    return subdir

def plot_chlor_a(ds, date_str=""):
    chl_a = ds['chlor_a']  # Chlorophyll-a variable
    lat = ds['number_of_lines']
    lon = ds['pixels_per_line']

    plt.figure(figsize=(10, 6))
    plt.pcolormesh(lon, lat, chl_a, cmap='viridis', shading='auto')
    plt.colorbar(label=f"Chlorophyll-a (mg/m³)")
    plt.title(f"Chlorophyll-a Concentration {date_str}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    # plt.show()
    chlor_a_dir = _create_image_subdir("chlor_a")
    plt.savefig(chlor_a_dir / date_str)

def plot_particulate_organic_carbon(ds, date_str=""):
    poc = ds['poc']  # Particulate Organic Carbon variable
    lat = ds['number_of_lines']
    lon = ds['pixels_per_line']

    plt.figure(figsize=(10, 6))
    plt.pcolormesh(lon, lat, poc, cmap='cividis', shading='auto')
    plt.colorbar(label=f"Particulate Organic Carbon (mg/m³)")
    plt.title(f"POC Concentration {date_str}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    # plt.show()
    poc_dir = _create_image_subdir("poc")
    plt.savefig(poc_dir / date_str)

def plot_phytoplankton_carbon(ds, date_str=""):
    phyto_c = ds['carbon_phyto']
    lat = ds['number_of_lines']
    lon = ds['pixels_per_line']

    plt.figure(figsize=(10, 6))
    plt.pcolormesh(lon, lat, phyto_c, cmap='plasma', shading='auto')
    plt.colorbar(label=f"Phytoplankton Carbon (mg/m³)")
    plt.title(f"Phytoplankton Carbon Concentration {date_str}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    # plt.show()
    phyto_c_dir = _create_image_subdir("phyto_c")
    plt.savefig(phyto_c_dir / date_str)


def open_file_as_xr(file_path):
    # Make sure to include group="geophysical_data" to merge data from different layers!
    ds = xr.open_dataset(file_path, group="geophysical_data")
    # print(ds)
    return ds

def print_sizes_of_files(directory):
    for file_path in directory.iterdir():
        print(file_path)
        ds = xr.open_dataset(file_path, group="geophysical_data")
        ds_size = ds.nbytes / (1024 * 1024)
        print("size:", ds_size)

def _extract_date_from_file(file_path, output_format="%m-%d-%Y"):
    try:
        date_string = file_path.name.split(".")[1][:8]
        date_object = datetime.strptime(date_string, "%Y%m%d")
        formatted_date = date_object.strftime(output_format)
        return formatted_date
    except ValueError:
        return None

def plot_from_file(file_path, plot_funct=plot_chlor_a):
    ds = open_file_as_xr(file_path)
    date_str = _extract_date_from_file(file_path)
    plot_funct(ds, date_str)

def plot_BGC_data(bgc_directory: Path):
    for file in os.listdir(bgc_directory):
        file_path = bgc_directory / file
        plot_from_file(file_path, plot_chlor_a)
        plot_from_file(file_path, plot_particulate_organic_carbon)
        plot_from_file(file_path, plot_phytoplankton_carbon)


if __name__ == '__main__':
    """
    Notes about the data:
    - OCI has a lot of data products
    - HARP2 and SPEXOne only have Level 0 and Level 1A-C data (no data products)
    - NRT: Near Real Time
    """
    # Time Span
    january_dates = ("2025-01-01", "2025-01-31")

    # AOI Bounding Box (Pacific Palisades Fire & Coast of Pacific Ocean)
    pacific_pal_bbox = (-118.75, 33.90, -118.45, 34.15)
    socal_bbox = (-122.28, 36.74, -115.26, 36.74)

    # Earthdata login
    auth = earthaccess.login(persist=True)

    ### Uncomment to print out the short names for each instrument:
    # PaceDataDownloader.print_short_names_for_instrument("oci")
    # PaceDataDownloader.print_short_names_for_instrument("harp2")
    # PaceDataDownloader.print_short_names_for_instrument("spexone")

    downloader = PaceDataDownloader(bounding_box=pacific_pal_bbox, time_span=january_dates)

    ### Download data for a short_name:
    downloader.download_data("PACE_OCI_L2_BGC_NRT", version=3.0, max_count=30)
    # downloader.download_data("PACE_OCI_L3M_CHL_NRT")
    # downloader.download_data("PACE_OCI_L2_AOP_NRT")
    # downloader.download_data("PACE_HARP2_L1C_SCI", max_count=1)
    # downloader.download_data("PACE_OCI_L2_LANDVI", max_count=1)

    # Plot OCI Level 2 BGC data:
    # Plots for cholorophyll a, particulate organic carbon, and phytoplankton carbon
    bgc_dir = Path("data\\PACE_OCI_L2_BGC_NRT")
    plot_BGC_data(bgc_dir)

    """
    TODO:
    - move plotting functions into separate module
    - add documentation (doc strings)
    - download more data (increase max_count)
    - look into plotting AOP data
    - download and plot HARP2 and SPEXOne data
    """
