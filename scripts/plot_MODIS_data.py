
import os
import sys
import numpy as np
from pathlib import Path

sys.path.append(".")
from src.plotting.plotting_functions import plot_variable, print_metadata


def plot_MODISA_data(data_directory: Path, verbose=True):
    """
    Plots chlorophyll-a concentrations Aqua MODIS data in the given directory.

    Params:
        bgc_directory: a path to a directory containing PACE OCI L2 BGC downloaded data
        verbose (bool): writes print statements about the progress if set to True
    """
    for file in os.listdir(data_directory):
        file_path = data_directory / file
        try:
            plot_variable(file_path, "chlor_a", "Log of Chlorophyll-a (mg/m³)",
                "Chlorophyll-a Concentration", transformation=np.log, vmin=-6, vmax=6, padding=0)
            if verbose:
                print("File:", file_path.name)
                print(" Plotting chlorophyll-a")
        except Exception as e:
            print("Error processing", file_path.name)
            continue

if __name__ == '__main__':

    # Following this tutorial: https://oceancolor.gsfc.nasa.gov/resources/docs/tutorials/notebooks/modis-explore-l2/

    file_path = Path("data\\MODISA_L2_OC\\AQUA_MODIS.20250109T222001.L2.OC.nc")
    print_metadata(file_path)

    data_dir = Path("data\\MODISA_L2_OC")

    plot_MODISA_data(data_dir)
