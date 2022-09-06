# Data is retrieved from Weather Underground via API calls
# Data is collected into an annual JSON file
# Wunderground JSON file structure is:
# {
#  "observations": [
#    {"valid_time_gmt": 1234567890, "temp": 0},
#    ...
#  ]
# }

from datetime import datetime
from json import dumps
import os
from pathlib import Path
import requests


class WeatherUnderground:
    """
    This class manages a few different things.  Initially it can be used to gather data from a location for a
    certain duration and store it locally.  After this has been retrieved once, this class allows a nice way to query
    into it to request data.
    """
    def __init__(self):
        pass

    def prepare_one_year_of_data_files(self, year: int, output_file_path: Path) -> None:
        """

        :param year:
        :param output_file_path:
        """
        site = 'KOKC:9:US'  # would be nice to find a closer one, but OKC is fine for now
        key = 'e1f10a1e78da46f5b10a1e78da96f525'  # this isn't a secret, will need to recreate each session
        base_url = f"https://api.weather.com/v1/location/{site}/observations/historical.json"
        month_nums = [x for x in range(1, 13)]
        days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        all_data_points = []
        start_of_year = datetime.strptime(f"{year}-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        for month in month_nums:
            start = f"{year}{month:02}01"
            end = f"{year}{month:02}{days_in_months[month-1]}"
            query_params = f"apiKey={key}&units=m&startDate={start}&endDate={end}"
            final_url = f"{base_url}?{query_params}"
            response = requests.get(final_url)
            if response.status_code != 200:
                pass  # fail lol
            data_points = response.json()['observations']
            for d in data_points:
                time_stamp = datetime.fromtimestamp(d['valid_time_gmt'])
                time_since_start_of_year = time_stamp - start_of_year
                hours_into_year = time_since_start_of_year.total_seconds() / 3600.0
                new_data_point = {'time': hours_into_year}
                for k in ['temp', 'dewPt', 'rh', 'pressure', 'precip_hrly', 'snow_hrly', 'vis', 'wspd', 'wdir']:
                    new_data_point[k] = d[k]
                all_data_points.append(new_data_point)
        with output_file_path.open('w') as output_file:
            output_file.write(dumps({'weather': all_data_points}, indent=2))


if __name__ == "__main__":
    this_file_path = Path(os.path.realpath(__file__))
    this_file_dir = this_file_path.parent
    data_files_dir = this_file_dir / 'weather_underground'
    data_files_dir.mkdir(exist_ok=True)
    WeatherUnderground().prepare_one_year_of_data_files(2019, Path(data_files_dir / '2019.json'))

