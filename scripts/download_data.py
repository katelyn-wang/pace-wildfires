import sys
import earthaccess

sys.path.append(".")
from src.downloader.pace_data_downloader import PaceDataDownloader


if __name__=='__main__':
    """
    Use this script to download PACE data from EarthAccess.

    Notes about the data:
    - OCI has a lot of data products
    - HARP2 and SPEXOne only have Level 0 and Level 1A-C data (no data products)
    - NRT: Near Real Time
    """
    # Time Span
    january_dates = ("2025-01-01", "2025-01-31")
    wider_dates = ("2025-01-01", "2025-05-01")

    # AOI Bounding Box (Pacific Palisades Fire & Coast of Pacific Ocean)
    pacific_pal_bbox = (-118.75, 33.90, -118.45, 34.15)
    socal_bbox = (-122.28, 36.74, -115.26, 36.74)

    # Earthdata login
    auth = earthaccess.login(persist=True)

    ### Uncomment to print out the short names (dataset IDs) for each instrument:
    PaceDataDownloader.print_short_names_for_instrument("oci")
    # PaceDataDownloader.print_short_names_for_instrument("harp2")
    # PaceDataDownloader.print_short_names_for_instrument("spexone")
    # PaceDataDownloader.print_short_names_for_instrument("modis")


    # Can change the bounding box area and/or time span
    downloader = PaceDataDownloader(bounding_box=pacific_pal_bbox, time_span=wider_dates)


    ### Uncomment below to download data from different datasets:

    ## Biogeochemical Data
    # downloader.download_data("PACE_OCI_L2_BGC_NRT", max_count=150, version=3.0)

    ## Apparent Optical Properties Data
    # downloader.download_data("PACE_OCI_L2_AOP_NRT", max_count=150)

    ## Land Vegetation Indices
    # downloader.download_data("PACE_OCI_L2_LANDVI_NRT", max_count=150)

    ## HARP2 Level 1C Data
    # downloader.download_data("PACE_HARP2_L1C_SCI", max_count=30)

    ## SPEXOne Level 1C Data
    # downloader.download_data("PACE_SPEXONE_L1C_SCI", max_count=30)

    ## Aqua MODIS Data
    # downloader.download_data("MODISA_L2_OC", max_count=150)
