import os
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime


def plot_variable(file_path: Path, var_of_interest: str, var_label: str, plot_title: str,
                  color_map='viridis', transformation=None):
    """
    Plots a variable of interest from the data from the file path with the specified parameters.
    Saves the image of the plot in a subdirectory titled as the variable of interest.

    Params:
        file_path (Path): the path to the downloaded PACE data file
        var_of_interest (str): the variable of interest from the data to be plotted
        var_label (str): the label for the colorbar
        plot_title (str): the title for the plot
        color_map (str): the color map for the plot (ex. viridis, cividis, plasma)
        transformation (function): a transformation to be applied to the data (ex. np.log)
    """
    # Open the file and extract relevant information
    ds = open_file_as_xr(file_path, var_of_interest)
    date_str = _extract_date_from_file(file_path)
    
    var = ds[var_of_interest]
    if transformation:
        var = transformation(var)
    lon = ds['longitude']
    lat = ds['latitude']

    # Create the plot
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    plt.pcolormesh(lon, lat, var, cmap=color_map, shading='auto', transform=ccrs.PlateCarree())

    # Add a coordinate grid and coastlines to the plot
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    gl.top_labels = False  # Remove top labels
    gl.right_labels = False  # Remove right labels

    # Label the plot
    plt.colorbar(label=var_label)
    plt.title(f"{plot_title} {date_str}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Save the plot in a subdirectory
    dir = _create_image_subdir(var_of_interest)
    plt.savefig(dir / date_str)
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
