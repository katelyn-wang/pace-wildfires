import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from scipy.ndimage import gaussian_filter1d
from matplotlib import animation
import cartopy.crs as ccrs
import earthaccess
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

sys.path.append(".")
from src.plotting.plotting_functions import plot_variable, print_metadata, _extract_date_from_file

class HARP2:
    def __init__(self, file):
        self.prod = xr.open_dataset(file)
        self.view = xr.open_dataset(file, group="sensor_views_bands").squeeze()
        self.geo = xr.open_dataset(file, group="geolocation_data").set_coords(["longitude", "latitude"])
        self.obs = xr.open_dataset(file, group="observation_data").squeeze()
        self.dataset = xr.merge((self.prod, self.obs, self.geo))

        self.angles = self.view["sensor_view_angle"]
        self.wavelengths = self.view["intensity_wavelength"]

        # Create a directory in images to save the visualizations to
        date_str = _extract_date_from_file(file)
        harp2_dir = Path("images") / file.parent.name
        os.makedirs(harp2_dir, exist_ok=True)
        self.save_dir = harp2_dir / date_str
        os.makedirs(self.save_dir, exist_ok=True)

    def create_visualizations(self):
        """Call the plot functions to create visualizations for the file"""
        # self.angle_wavelength_plot()
        self.iqu_plot()
        self.plot_degree_of_linear_polarization()
        self.mean_dolp_by_view_angle()
        self.plot_radiance_reflection()
        self.mean_reflectance_check()
        self.create_animation()

    def angle_wavelength_plot(self):
        fig, (ax_angle, ax_wavelength) = plt.subplots(2, 1, figsize=(14, 7))
        ax_angle.set_ylabel("View Angle (degrees)")
        ax_angle.set_xlabel("Index")
        ax_wavelength.set_ylabel("Wavelength (nm)")
        ax_wavelength.set_xlabel("Index")
        plot_data = [
            (0, 10, "green", "^", "green"),
            (10, 70, "red", "*", "red"),
            (70, 80, "black", "s", "NIR"),
            (80, 90, "blue", "o", "blue"),
        ]
        for start_idx, end_idx, color, marker, label in plot_data:
            ax_angle.plot(
                np.arange(start_idx, end_idx),
                self.angles[start_idx:end_idx],
                color=color,
                marker=marker,
                label=label,
            )
            ax_wavelength.plot(
                np.arange(start_idx, end_idx),
                self.wavelengths[start_idx:end_idx],
                color=color,
                marker=marker,
                label=label,
            )
        ax_angle.legend()
        ax_wavelength.legend()
        # plt.show()
        plt.savefig(self.save_dir / "angle_wavelength.png")
        plt.close()

    # Understanding Polarimetry
    def iqu_plot(self):
        stokes = self.dataset[["i", "q", "u"]]

        green_nadir_idx = np.argmin(np.abs(self.angles[:10].values))
        red_nadir_idx = 10 + np.argmin(np.abs(self.angles[10:70].values))
        blue_nadir_idx = 80 + np.argmin(np.abs(self.angles[80:].values))

        rgb_stokes = stokes.isel(
            {
                "number_of_views": [red_nadir_idx, green_nadir_idx, blue_nadir_idx],
            }
        )

        rgb_stokes = (rgb_stokes - rgb_stokes.min()) / (rgb_stokes.max() - rgb_stokes.min())
        rgb_stokes = rgb_stokes ** (3 / 4)

        window = rgb_stokes["i"].notnull().all("number_of_views")
        crop_rgb_stokes = rgb_stokes.where(
            window.any("bins_along_track") & window.any("bins_across_track"),
            drop=True,
        )
        crs_proj = ccrs.PlateCarree(-170)
        crs_data = ccrs.PlateCarree()

        fig, ax = plt.subplots(1, 3, figsize=(16, 5), subplot_kw={"projection": crs_proj})
        fig.suptitle(f'{self.prod.attrs["product_name"]} RGB')

        for i, (key, value) in enumerate(crop_rgb_stokes.items()):
            ax[i].pcolormesh(value["longitude"], value["latitude"], value, transform=crs_data)
            ax[i].gridlines(draw_labels={"bottom": "x", "left": "y"}, linestyle="--")
            ax[i].coastlines(color="grey")
            ax[i].set_title(key.upper())

        # plt.show()
        plt.savefig(self.save_dir / "IQU.png")
        plt.close()

    # DoLP: Degree of Linear Polarization
    def plot_degree_of_linear_polarization(self):
        green_nadir_idx = np.argmin(np.abs(self.angles[:10].values))
        red_nadir_idx = 10 + np.argmin(np.abs(self.angles[10:70].values))
        blue_nadir_idx = 80 + np.argmin(np.abs(self.angles[80:].values))

        stokes = self.dataset[["i", "q", "u"]]

        rgb_stokes = stokes.isel(
            {
                "number_of_views": [red_nadir_idx, green_nadir_idx, blue_nadir_idx],
            }
        )

        rgb_stokes = (rgb_stokes - rgb_stokes.min()) / (rgb_stokes.max() - rgb_stokes.min())
        rgb_stokes = rgb_stokes ** (3 / 4)

        window = rgb_stokes["i"].notnull().all("number_of_views")
        crop_rgb_stokes = rgb_stokes.where(
            window.any("bins_along_track") & window.any("bins_across_track"),
            drop=True,
        )

        crs_proj = ccrs.PlateCarree(-170)
        crs_data = ccrs.PlateCarree()

        rgb_dolp = self.dataset["dolp"].isel(
            {
                "number_of_views": [red_nadir_idx, green_nadir_idx, blue_nadir_idx],
            }
        )
        window = rgb_stokes["i"].notnull().all("number_of_views")
        crop_rgb_dolp = rgb_dolp.where(
            window.any("bins_along_track") & window.any("bins_across_track"),
            drop=True,
        )
        crop_rgb = xr.merge((crop_rgb_dolp, crop_rgb_stokes))

        fig, ax = plt.subplots(1, 2, figsize=(16, 8), subplot_kw={"projection": crs_proj})
        fig.suptitle(f'{self.prod.attrs["product_name"]} RGB')

        for i, (key, value) in enumerate(crop_rgb[["i", "dolp"]].items()):
            ax[i].pcolormesh(value["longitude"], value["latitude"], value, transform=crs_data)
            ax[i].gridlines(draw_labels={"bottom": "x", "left": "y"}, linestyle="--")
            ax[i].coastlines(color="grey")
            ax[i].set_title(key.upper())

        # plt.show()
        plt.savefig(self.save_dir / "degree_of_linear_polarization.png")
        plt.close()

    # Mean DoLP by View Angle
    def mean_dolp_by_view_angle(self):
        dolp_mean = self.dataset["dolp"].mean(["bins_along_track", "bins_across_track"])
        dolp_mean = (dolp_mean - dolp_mean.min()) / (dolp_mean.max() - dolp_mean.min())

        fig, ax = plt.subplots(figsize=(16, 6))
        wv_uq = np.unique(self.wavelengths.values)
        plot_data = [("b", "o"), ("g", "^"), ("r", "*"), ("k", "s")]
        for wv_idx in range(4):
            wv = wv_uq[wv_idx]
            wv_mask = self.wavelengths.values == wv
            c, m = plot_data[wv_idx]
            ax.plot(
                self.angles.values[wv_mask],
                dolp_mean[wv_mask],
                color=c,
                marker=m,
                markersize=7,
                label=str(wv),
            )
        ax.legend()
        ax.set_xlabel("Nominal View Angle (°)")
        ax.set_ylabel("DoLP")
        ax.set_title("Mean DoLP by View Angle")
        # plt.show()
        plt.savefig(self.save_dir / "mean_dolp_by_view_angle.png")
        plt.close()

    # Radiance to Reflection helper conversion function
    def rad_to_refl(rad, f0, sza, r):
        """Convert radiance to reflectance.
        
        Args:
            rad: Radiance.
            f0: Solar irradiance.
            sza: Solar zenith angle.
            r: Sun-Earth distance (in AU).

        Returns: Reflectance.
        """
        return (r**2) * np.pi * rad / np.cos(sza * np.pi / 180) / f0

    def plot_radiance_reflection(self):
        refl = HARP2.rad_to_refl(
            rad=self.dataset["i"],
            f0=self.view["intensity_f0"],
            sza=self.dataset["solar_zenith_angle"],
            r=float(self.dataset.attrs["sun_earth_distance"]),
        )

        red_nadir_idx = 10 + np.argmin(np.abs(self.angles[10:70].values))

        fig, ax = plt.subplots(1, 2, figsize=(16, 8))
        ax[0].imshow(self.dataset["i"].sel({"number_of_views": red_nadir_idx}), cmap="gray")
        ax[0].set_title("Radiance")
        ax[1].imshow(refl.sel({"number_of_views": red_nadir_idx}), cmap="gray")
        ax[1].set_title("Reflectance")
        # plt.show()
        plt.savefig(self.save_dir / "radiance_reflection.png")
        plt.close()

    # Mean reflectance for each view angle and spectral channel -- flatness as a sanity check
    def mean_reflectance_check(self):
        refl = HARP2.rad_to_refl(
            rad=self.dataset["i"],
            f0=self.view["intensity_f0"],
            sza=self.dataset["solar_zenith_angle"],
            r=float(self.dataset.attrs["sun_earth_distance"]),
        )

        fig, ax = plt.subplots(figsize=(16, 6))
        wv_uq = np.unique(self.wavelengths.values)
        plot_data = [("b", "o"), ("g", "^"), ("r", "*"), ("black", "s")]
        refl_mean = refl.mean(["bins_along_track", "bins_across_track"])
        for wv_idx in range(4):
            wv = wv_uq[wv_idx]
            wv_mask = self.wavelengths.values == wv
            c, m = plot_data[wv_idx]
            ax.plot(
                self.angles.values[wv_mask],
                refl_mean[wv_mask],
                color=c,
                marker=m,
                markersize=7,
                label=str(wv),
            )

        ax.legend()
        ax.set_xlabel("Nominal View Angle (°)")
        ax.set_ylabel("Reflectance")
        ax.set_title("Mean Reflectance by View Angle")
        # plt.show()
        plt.savefig(self.save_dir / "mean_reflectance_check.png")
        plt.close()

    def create_animation(self):
        refl = HARP2.rad_to_refl(
            rad=self.dataset["i"],
            f0=self.view["intensity_f0"],
            sza=self.dataset["solar_zenith_angle"],
            r=float(self.dataset.attrs["sun_earth_distance"]),
        )
        # Get reflectances of red channel and normalize
        refl_red = refl[..., 10:70]
        refl_pretty = (refl_red - refl_red.min()) / (refl_red.max() - refl_red.min())
        # mild Gaussian for animation smoothness
        refl_pretty.data = gaussian_filter1d(refl_pretty, sigma=0.5, truncate=2, axis=2)
        # Brighten
        refl_pretty = refl_pretty ** (2 / 3)
        # Append all but first and last frame in reverse order to get bounce effect
        frames = np.arange(refl_pretty.sizes["number_of_views"])
        frames = np.concatenate((frames, frames[-1::-1]))

        fig, ax = plt.subplots()
        im = ax.imshow(refl_pretty[{"number_of_views": 0}], cmap="gray")

        def update(i):
            im.set_data(refl_pretty[{"number_of_views": i}])
            return im

        an = animation.FuncAnimation(fig=fig, func=update, frames=frames, interval=30)
        filename = f'{self.save_dir}/harp2_red_anim_{self.dataset.attrs["product_name"].split(".")[1]}.gif'
        an.save(filename, writer="pillow")
        plt.close()


def visualize_harp2_data(data_dir: Path, verbose=True):
    """Loop through a directory with HARP2 data files and create visualizations for them"""
    for file in os.listdir(data_dir):
        if verbose: print("Processing", file)
        file_path = data_dir / file
        HARP2(file_path).create_visualizations()


if __name__ == '__main__':
    """
    Created HARP2 class to create visualizations for HARP2 data
    using code from HARP2 Basic Visualization Tutorial:
    https://oceancolor.gsfc.nasa.gov/resources/docs/tutorials/notebooks/harp2-basic-visualizations/

    Assumes HARP2 data (PACE_HARP2_L1C_SCI) is downloaded from scripts/download_data.py
    """
    harp2_dir = Path("data/PACE_HARP2_L1C_SCI")
    visualize_harp2_data(harp2_dir)
    
