import os
import sys
import numpy as np
from pathlib import Path

sys.path.append(".")
from src.plotting.plotting_functions import plot_variable, print_metadata


def plot_BGC_data(bgc_directory: Path, verbose=True):
    """
    Plots chlorophyll-a, particulate organic carbon, and phytoplankton carbon concentrations
    for all the downloaded Level 2 BGC data in the given directory.

    Params:
        bgc_directory: a path to a directory containing PACE OCI L2 BGC downloaded data
    """
    for file in os.listdir(bgc_directory):
        file_path = bgc_directory / file
        if verbose:
            print("File:", file_path.name)
            print(" Plotting chlorophyll-a")
        plot_variable(file_path, "chlor_a", "Log of Chlorophyll-a (mg/m³)",
            "Chlorophyll-a Concentration", transformation=np.log)

        if verbose: print(" Plotting particulate organic carbon")
        plot_variable(file_path, "poc", "Particulate Organic Carbon (mg/m³)",
            "POC Concentration", color_map="cividis", transformation=np.log1p)

        if verbose: print(" Plotting phytoplankton carbon")
        plot_variable(file_path, "carbon_phyto", "Phytoplankton Carbon (mg/m³)",
            "Phytoplankton Carbon Concentration", color_map="plasma", transformation=np.log)


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
    # bgc_file = Path("data\\PACE_OCI_L2_BGC_NRT\\PACE_OCI.20250104T202321.L2.OC_BGC.V3_0.NRT.nc")
    # print_metadata(bgc_file)

    # Plot OCI Level 2 BGC data:
    # Plots for cholorophyll-a, particulate organic carbon, and phytoplankton carbon
    bgc_dir = Path("data\\PACE_OCI_L2_BGC_NRT")
    plot_BGC_data(bgc_dir)
