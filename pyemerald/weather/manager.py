import os
from pathlib import Path


class WeatherManager:

    @staticmethod
    def path_to_tmy_okc_epw_file() -> str:
        this_file_path = Path(os.path.realpath(__file__))
        this_file_dir = this_file_path.parent
        return this_file_dir / 'resources' / 'okc.epw'
