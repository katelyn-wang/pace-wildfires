import os
import sys
import numpy as np
from pathlib import Path

sys.path.append(".")
from src.plotting.plotting_functions import plot_variable, print_metadata


def plot_LANDVI_data(landvi_dir: Path, verbose=True):
    """
    Plots different land index plots for all the downloaded L2 LANDVI data in the given directory.

    Params:
        landvi_dir: a path to a directory containing PACE OCI L2 BGC downloaded data
        verbose (bool): writes print statements about the progress if set to True
    """
    for file in os.listdir(landvi_dir):
        file_path = landvi_dir / file
        if verbose:
            print("File:", file_path.name)
            print(" Plotting NDVI")
        plot_variable(file_path, "ndvi", "Normalized Difference Vegetation Index",
            "Normalized Difference Vegetation Index", color_map='YlGn', vmin=-1, vmax=1)

        if verbose: print(" Plotting EVI")
        plot_variable(file_path, "evi", "Enhanced Vegetation Index",
            "Enhanced Vegetation Index", color_map='YlGn', vmin=-1, vmax=1)

        if verbose: print(" Plotting NDWI")
        plot_variable(file_path, "ndwi", "Normalized Difference Water Index",
            "Normalized Difference Water Index", color_map="Blues", vmin=-1, vmax=1)
        
        if verbose: print(" Plotting NDII")
        plot_variable(file_path, "ndii", "Normalized Difference Infrared Index",
            "Normalized Difference Infrared Index", color_map="Blues", vmin=-1, vmax=1)

        if verbose: print(" Plotting PRI")
        plot_variable(file_path, "pri", "Photochemical Reflectance Index",
            "Photochemical Reflectance Index", color_map="cividis", vmin=-0.2, vmax=0.2)
        
        if verbose: print(" Plotting CCI")
        plot_variable(file_path, "cci", "Chlorophyll-Cartenoid Index",
            "Chlorophyll-Cartenoid Index", color_map="cividis", vmin=-0.3, vmax=0.3)
        
        if verbose: print(" Plotting CIRE")
        plot_variable(file_path, "cire", "Chlorophyll Index Red Edge",
            "Chlorophyll Index Red Edge", color_map="YlGn", vmin=0, vmax=5)

if __name__ == '__main__':
    """
    This script assumes the relevant data is already downloaded using `download_data.py`
    (Data with the shortname 'PACE_OCI_L2_LANDVI_NRT')

    PACE: Plankton, Aerosol, Cloud, and ocean Ecosystem
    OCI: Ocean Color Instrument
    LANDVI: Land Vegetation Indices

    Level 2 LANDVI Data Products:
    https://oceancolor.gsfc.nasa.gov/data/10.5067/PACE/OCI/L2/LANDVI/3.0
        ndvi: normalized difference vegetation index
        evi: enhanced vegetation index
        ndwi: normalized difference water index
        ndii: normalized difference infrared index
        pri: photochemical reflectance index
        cci: chlorophyll-cartenoid index
        cire: chlorophyll index red edge

        Less Relevant: ndsi, car, mari
    """

    ## Uncomment to view metadata about the LANDVI data
    file_path = Path("data\\PACE_OCI_L2_LANDVI_NRT\\PACE_OCI.20250104T202321.L2.LANDVI.V3_0.NRT.nc")
    # print_metadata(file_path)

    # Plot OCI Level 2 LANDVI data:
    landvi_dir = Path("data\\PACE_OCI_L2_LANDVI_NRT")
    plot_LANDVI_data(landvi_dir)
