import os
import sys
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.append(".")
from src.plotting.plotting_functions import open_file_as_xr, _extract_date_from_file, _create_image_subdir

def overlay_plot(bgc_file, aop_file, landvi_file, bgc_var="chlor_a", aop_var="aot_865", landvi_var="ndvi",
                 min_lon=-118.75, max_lon=-118.45, min_lat=33.99, max_lat=34.15, padding=1, zoomed_map=True,
                 cmaps = ['viridis', 'Greys', 'Greens'], alphas = [0.7, 0.4, 1], 
                 min_max_values = [(-0.6, 0.8), (0, 0.3), (-1, 1)]):
    """
    Creates an overlayed plot with variables from BGC, AOP, and LANDVI files.
    Assumes the files are from the same date/time and location.
    """
    # Load datasets
    bgc = open_file_as_xr(bgc_file, bgc_var)
    aop = open_file_as_xr(aop_file, aop_var)
    landvi = open_file_as_xr(landvi_file, landvi_var)

    lon = bgc['longitude'].values
    lat = bgc['latitude'].values

    bgc_values = np.log(bgc[bgc_var].values)
    aop_values = aop[aop_var].values
    landvi_values = landvi[landvi_var].values

    # Prepare map
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    if zoomed_map:
        min_lon -= padding
        max_lon += padding
        min_lat -= padding
        max_lat += padding

        # Create a mask for the bounding box
        lon_mask = (lon >= min_lon) & (lon <= max_lon)
        lat_mask = (lat >= min_lat) & (lat <= max_lat)

        # Apply the mask using array slicing
        valid_rows = np.where(lat_mask.any(axis=1))[0]  # Get valid row indices
        valid_cols = np.where(lon_mask.any(axis=0))[0]  # Get valid col indices

        # Subset the data using row and column indices
        lon = lon[np.min(valid_rows):np.max(valid_rows)+1, np.min(valid_cols):np.max(valid_cols)+1]
        lat = lat[np.min(valid_rows):np.max(valid_rows)+1, np.min(valid_cols):np.max(valid_cols)+1]
        bgc_values = bgc_values[np.min(valid_rows):np.max(valid_rows)+1, np.min(valid_cols):np.max(valid_cols)+1]
        aop_values = aop_values[np.min(valid_rows):np.max(valid_rows)+1, np.min(valid_cols):np.max(valid_cols)+1]
        landvi_values = landvi_values[np.min(valid_rows):np.max(valid_rows)+1, np.min(valid_cols):np.max(valid_cols)+1]

        ax.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree()) 

    meshes = []
    for var, cmap, alpha, min_max in zip([bgc_values, aop_values, landvi_values], cmaps, alphas, min_max_values):
        mesh = ax.pcolormesh(lon, lat, var, cmap=cmap, shading='auto', transform=ccrs.PlateCarree(),
                             alpha=alpha, vmin=min_max[0], vmax=min_max[1])
        meshes.append(mesh)

    # After the loop, add one colorbar for each layer
    for mesh, label in zip(meshes, [f'Log of {bgc_var}', aop_var, landvi_var]):
        cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', shrink=0.6, pad=0.02)
        cbar.set_label(label, fontsize=10)
        
    # Add coastlines, borders
    ax.coastlines()
    gl = ax.gridlines(draw_labels=True, linestyle="--", alpha=0.5)
    gl.top_labels = False  # Remove top labels
    gl.right_labels = False  # Remove right labels
    date_str = _extract_date_from_file(bgc_file)
    ax.set_title(f"{date_str} - BGC ({bgc_var}), AOP ({aop_var}), LANDVI ({landvi_var})")

    # Save the file
    save_dir = Path("images/BGC_AOP_LANDVI_Overlay")
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(save_dir / date_str)
    plt.close()


if __name__ == '__main__':
    # bgc_file = Path("data/PACE_OCI_L2_BGC_NRT/PACE_OCI.20250104T202321.L2.OC_BGC.V3_0.NRT.nc")
    # aop_file = Path("data/PACE_OCI_L2_AOP_NRT/PACE_OCI.20250104T202321.L2.OC_AOP.V3_0.NRT.nc")
    # landvi_file = Path("data/PACE_OCI_L2_LANDVI_NRT/PACE_OCI.20250104T202321.L2.LANDVI.V3_0.NRT.nc")
    # overlay_plot(bgc_file, aop_file, landvi_file)

    bgc_dir = Path("data/PACE_OCI_L2_BGC_NRT")
    aop_dir = Path("data/PACE_OCI_L2_AOP_NRT")
    landvi_dir = Path("data/PACE_OCI_L2_LANDVI_NRT")
    for bgc_file, aop_file, landvi_file in zip(bgc_dir.iterdir(), aop_dir.iterdir(), landvi_dir.iterdir()):
        try:
            overlay_plot(bgc_file, aop_file, landvi_file, padding=0)
        except Exception as e:
            print(f"Skipping file {bgc_file.name}: {e}")
            continue
