import sys
import earthaccess

sys.path.append(".")
from src.downloader.pace_data_downloader import PaceDataDownloader


if __name__=='__main__':
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
    PaceDataDownloader.print_short_names_for_instrument("oci")
    PaceDataDownloader.print_short_names_for_instrument("harp2")
    PaceDataDownloader.print_short_names_for_instrument("spexone")

    downloader = PaceDataDownloader(bounding_box=pacific_pal_bbox, time_span=january_dates)

    ### Download data for a short_name:
    # downloader.download_data("PACE_OCI_L2_BGC_NRT", version=3.0, max_count=30)
    # downloader.download_data("PACE_OCI_L3M_CHL_NRT")
    # downloader.download_data("PACE_OCI_L2_AOP_NRT")
    # downloader.download_data("PACE_HARP2_L1C_SCI", max_count=1)
    # downloader.download_data("PACE_OCI_L2_LANDVI", max_count=1)
    # downloader.download_data("PACE_OCI_L2_LANDVI_NRT")