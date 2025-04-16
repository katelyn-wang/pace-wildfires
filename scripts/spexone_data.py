import os
import sys
from pathlib import Path

from scipy.ndimage import gaussian_filter1d
from matplotlib import animation
import cartopy.crs as ccrs
import earthaccess
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

sys.path.append(".")
from src.plotting.plotting_functions import plot_variable, print_metadata


if __name__ == '__main__':
    """
    Only two granules downloaded -- will probably not use for now
    """
    # Open a file and print information
    file = Path("data\\PACE_SPEXONE_L1C_SCI\\PACE_SPEXONE.20250107T202910.L1C.V3.5km.nc")
    prod = xr.open_dataset(file)
    view = xr.open_dataset(file, group="sensor_views_bands").squeeze()
    geo = xr.open_dataset(file, group="geolocation_data").set_coords(["longitude", "latitude"])
    obs = xr.open_dataset(file, group="observation_data").squeeze()
    dataset = xr.merge((prod, obs, geo))
    print(dataset)
