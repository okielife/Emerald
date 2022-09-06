import math
import os
from pathlib import Path
from typing import List


class HourlyWeatherDataPoint:

    def __init__(self, time_stamp_line: str, lines_of_raw_hourly_data: List[str]):
        # I will be doing a raw average, for now at least
        # this will mean weird results for wind, but honestly, the model will likely be just fine :)
        year = time_stamp_line[5:9]
        month = time_stamp_line[10:12]
        day = time_stamp_line[13:15]
        relative_humidity_sum = 0.0
        air_temp_sum = 0.0
        wind_speed_sum = 0.0
        rain_sum = 0.0
        pressure_sum = 0.0
        solar_sum = 0.0
        num_valid_points = 0
        get_minutes = True
        minutes_line_one = None
        for raw_line in lines_of_raw_hourly_data:
            tokens = [x for x in raw_line.strip().split(' ') if x]
            if get_minutes:
                minutes_line_one = float(tokens[2])
                get_minutes = False
            relative_humidity_percent = float(tokens[3])  # 78
            if relative_humidity_percent < 0:
                continue
            num_valid_points += 1
            relative_humidity_sum += relative_humidity_percent
            air_temp_c = float(tokens[4])  # 2.7
            air_temp_sum += air_temp_c
            wind_speed_m_s = float(tokens[5])  # 6.6
            wind_speed_sum += wind_speed_m_s
            rain = float(tokens[11])  # 3.81
            rain_sum += rain
            press_mbar = float(tokens[12])  # 977.84
            pressure_sum += press_mbar
            solar_wm2 = float(tokens[13])  # 281
            solar_sum += solar_wm2
        self.average_relative_humidity = relative_humidity_sum / 12.0
        self.average_air_temp = air_temp_sum / 12.0
        self.average_dew_point = WeatherManager.dew_point(self.average_air_temp, self.average_relative_humidity)
        self.average_wind_speed = wind_speed_sum / 12.0
        self.average_rain = rain_sum / 12.0
        self.average_pressure = pressure_sum / 12.0
        self.average_solar = solar_sum / 12.0
        hour_line_one = int((minutes_line_one + 60.0) / 60.0)
        self.original_time_stamp = "%s.%s.%s:%s00 GMT" % (year, month, day, str(hour_line_one).zfill(2))

    def __str__(self):
        return "OrigDate=%s; T=%f; Solar=%f" % (self.original_time_stamp, self.average_air_temp, self.average_solar)


class EPWFile:
    def __init__(self, file_path: Path):
        self.header_lines = []
        self.data_rows = []
        with open(str(file_path)) as f_epw:
            for _ in range(8):
                self.header_lines.append(f_epw.readline().strip())
            for _ in range(8760):
                line_in = f_epw.readline().strip()
                tokens = line_in.split(',')
                self.data_rows.append(tokens)


class WeatherManager:

    def __init__(self):
        this_file_path = Path(os.path.realpath(__file__))
        this_file_dir = this_file_path.parent
        self.resource_dir = this_file_dir / 'resources'

    @staticmethod
    def calculate_rh_at_t_t_dew(t: float, dew: float) -> float:
        temp_k = t + 273.15
        dew_k = dew + 273.15
        return 100 * (math.exp(5423 * ((1/273) - (1/dew_k))) / math.exp(5423 * ((1/273) - (1/temp_k))))

    @staticmethod
    def dew_point(temperature: float, relative_humidity: float) -> float:
        if relative_humidity > 50:
            return temperature - ((100 - relative_humidity)/5.0)
        for t in range(-40, 40):
            for tenth in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
                for hundredth in [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]:
                    for thousandth in [0.000, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009]:
                        this_dew = t + tenth + hundredth + thousandth
                        calculated_relative_humidity = WeatherManager.calculate_rh_at_t_t_dew(temperature, this_dew)
                        if abs(calculated_relative_humidity - relative_humidity) < 0.01:
                            return this_dew
        raise Exception("Could not find dew point")

    def path_to_tmy_okc_epw_file(self) -> Path:
        return self.resource_dir / 'okc.epw'

    def path_to_merged_epw_file(self) -> Path:
        return self.resource_dir / 'merged.epw'

    def parse_and_average_mesonet_data(self) -> List[HourlyWeatherDataPoint]:
        raw_data_dir = self.resource_dir / 'kingfisher2019'
        all_raw_files = sorted([x for x in raw_data_dir.iterdir() if x.is_file() and x.name.endswith('kin2.txt')])
        raw_hourly_data = []
        for raw_file in all_raw_files:
            with open(str(raw_file)) as f_raw:
                lines = f_raw.readlines()
                starting_line_num = 3
                for i in range(24):
                    raw_hourly_data.append(HourlyWeatherDataPoint(
                        lines[1],
                        lines[starting_line_num:starting_line_num+12]
                    ))
                    starting_line_num += 12
        # it looks like the data is not affected by daylight savings time, the sunrises the same hour through DST change
        # so just need to shift by 6 hours to get local time
        aligned_data = []
        for i in range(6, 8760):
            aligned_data.append(raw_hourly_data[i])
        # now take the 6 hours from Dec 30 as the last 6 hours of Dec 31 as an approximation
        for i in range(8736, 8742):
            aligned_data.append(raw_hourly_data[i])
        return aligned_data

    @staticmethod
    def merge_tmy_and_mesonet(mesonet: List[HourlyWeatherDataPoint], epw: EPWFile) -> str:
        epw_string = ''
        for head in epw.header_lines:
            epw_string += head + '\n'
        for i in range(8760):
            epw_hour = epw.data_rows[i]
            mesonet_hour = mesonet[i]
            new_tokens = [
                epw_hour[0], epw_hour[1], epw_hour[2], epw_hour[3], epw_hour[4], epw_hour[5],
                mesonet_hour.average_air_temp,
                mesonet_hour.average_dew_point,
                mesonet_hour.average_relative_humidity,
                mesonet_hour.average_pressure * 100,  # mesonet in kPa, EPW in Pa
                mesonet_hour.average_solar,  # TODO: Verify which of these needs the mesonet value
                epw_hour[11],
                epw_hour[12],
                epw_hour[13],
                epw_hour[14],
                epw_hour[15],
                epw_hour[16],
                epw_hour[17],
                epw_hour[18],
                epw_hour[19],
                epw_hour[20],
                epw_hour[21],
                epw_hour[22],
                epw_hour[23],
                epw_hour[24],
                epw_hour[25],
                epw_hour[26],
                epw_hour[27],
                epw_hour[28],
                epw_hour[29],
                epw_hour[30],
                epw_hour[31],
                0.0,
                epw_hour[33]
            ]
            epw_string += ','.join([str(x) for x in new_tokens]) + '\n'
        return epw_string


if __name__ == "__main__":
    # dp = WeatherManager.dew_point(35, 65)
    w = WeatherManager()
    mesonet_contents = w.parse_and_average_mesonet_data()
    epw_contents = EPWFile(w.path_to_tmy_okc_epw_file())
    new_contents = WeatherManager.merge_tmy_and_mesonet(mesonet_contents, epw_contents)
    with open('/tmp/new.epw', 'w') as f:
        f.write(new_contents)

# EPW Header
# 0: Year
# 1: Month
# 2: Day
# 3: Hour
# 4: Minute
# 5: DryBulb {C}
# 6: DewPoint {C}
# 7: RelHum {%}
# 8: Pressure {Pa}
# 9: Horizontal Radiation {Wh/m2}
# 10: Direct Radiation {Wh/m2}
# 11: Horizontal IR Intensity {Wh/m2}
# 12: Global Horizontal Radiation {Wh/m2}
# 13: Direct Normal Radiation {Wh/m2}
# 14: Diffuse Horizontal Radiation {Wh/m2}
# 15: Global Horizontal Illuminance {lux}
# 16: Direct Normal Illuminance {lux}
# 17: Diffuse Horizontal Illuminance {lux}
# 18: Zenith Luminance {Cd/m2}
# 19: Wind Direction {deg}
# 20: Wind Speed {m/s}
# 21: Total Sky Cover {.1}
# 22: Opaque Sky Cover {.1}
# 23: Visibility {km}
# 24: Ceiling Height {m}
# 25: Present Weather Observation,
# 26: Present Weather Codes
# 27: Precipitable Water {mm}
# 28: Aerosol Optical Depth {.001}
# 29: Snow Depth {cm}
# 30: Days Since Last Snow
# 31: Albedo {.01}
# 32: Liquid Precipitation Depth {mm}
# 33: Liquid Precipitation Quantity {hr}
