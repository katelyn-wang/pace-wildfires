import os
import sys
import numpy as np
from pathlib import Path

sys.path.append(".")
from src.plotting.plotting_functions import plot_variable, print_metadata

def plot_AOP_data(aop_directory: Path, verbose=True):
    """
    Plots Aerosol Optical Thickness (AOT), NFLH, Angstrom, and AVW
    for all the downloaded Level 2 AOP data in the given directory.

    Params:
        aop_directory: a path to a directory containing PACE OCI L2 AOP downloaded data
        verbose (bool): writes print statements about the progress if set to True
    """
    for file in os.listdir(aop_directory):
        file_path = aop_directory / file
        if verbose:
            print("File:", file_path.name)
            print(" Plotting AOT")
        plot_variable(file_path, "aot_865", "AOT at 865 nm", "Aerosol optical thickness at 865 nm",
                      color_map="inferno", vmin=0, vmax=0.35)

        # if verbose: print(" Plotting Rrs")
        # plot_variable(file_path, "Rrs", "Remote Reflectance (sr^-1)", "Remote Sensing Reflectance",
        #               color_map="ocean")

        if verbose: print(" Plotting NFLH")
        plot_variable(file_path, "nflh", "Normalized Fluorescence Line Height (W m^-2 um^-1 sr^-1)",
            "Normalized Fluorescence Line Height (NFLH)", color_map="turbo")
        
        if verbose: print(" Plotting angstrom")
        plot_variable(file_path, "angstrom", "Aerosol Angstrom exponent (443-865nm)",
            "Aerosol Angstrom exponent", color_map="coolwarm")
        
        if verbose: print(" Plotting avw")
        plot_variable(file_path, "avw", "Apparent Visible Wavelenth (400-700nm)",
            "Apparent Visible Wavelength", color_map="coolwarm")


if __name__ == '__main__':
    """
    This script assumes the relevant data is already downloaded using `download_data.py`
    (Data with the shortname 'PACE_OCI_L2_AOP_NRT')

    PACE: Plankton, Aerosol, Cloud, and ocean Ecosystem
    OCI: Ocean Color Instrument
    AOP: Apparent Optical Properties

    Level 2 AOP Data Products:
        aop_865: Aerosol Optical Thickness at 865 nm
        angstrom: Aerosol Angstrom Exponent
        Rrs: Remote Sensing Reflectance
        nflh: Normalized Flourescent Line Height
        avw: Apparent Visible Wavelength
    """

    aop_file = Path("data\\PACE_OCI_L2_AOP_NRT\\PACE_OCI.20250104T202321.L2.OC_AOP.V3_0.NRT.nc")
    print_metadata(aop_file)

    # plot_variable(aop_file, "Rrs", "Remote Sensing Reflectance (sr^-1)", "Remote Sensing Reflectance")
    # plot_variable(aop_file, "aot_865", "AOT at 865 nm", "Aerosol optical thickness at 865 nm", color_map="inferno")

    # Plot OCI Level 2 AOP data:
    aop_dir = Path("data\\PACE_OCI_L2_AOP_NRT")
    plot_AOP_data(aop_dir)
