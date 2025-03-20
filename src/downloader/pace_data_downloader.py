import earthaccess
from pathlib import Path

class PaceDataDownloader:
    def __init__(self, bounding_box, time_span: tuple[str, str]):
        """
        bounding_box: (min longitude, min latitude, max longitude, max latitude)
        time_span: (start YYYY-mm-dd, end YYYY-mm-dd)
        """
        self.bbox = bounding_box
        self.tspan = time_span

    def print_short_names_for_instrument(instr="oci"):
        """
        Prints out the short names for a given instrument.
        Example instruments are 'oci', 'harp2', and 'spexone'
        """
        results = earthaccess.search_datasets(instrument=instr)
        for item in results:
            summary = item.summary()
            print(summary["short-name"])

    def download_data(self, short_name, max_count=20, save_dir=None):
        """
        Downloads data with the specified short name, bounding box, and time span.
        Saves the downloaded data to data/{short_name} by default if no directory is specified.
        """
        results = earthaccess.search_data(
            short_name=short_name,
            bounding_box=self.bbox,
            temporal=self.tspan,
            count=max_count,
        )

        if len(results) == 0:
            print("No results found")
            return
        else:
            print(f"Found {len(results)} results")
            print(results)

        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        if save_dir == None:
            save_dir = Path(f"data/{short_name}")

        save_dir.mkdir(exist_ok=True)
        paths = earthaccess.download(results, str(Path(save_dir)))
        print(paths)
