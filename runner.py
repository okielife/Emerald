from datetime import datetime
import distutils.cmd
from json import loads
import os
from pathlib import Path
from subprocess import check_call
import sys
import tempfile
import urllib.request
from pyemerald.model.model import Model
from pyemerald.model.processor import OutputProcessor
from pyemerald.validation.analyzer import ResultsAnalyzer
from pyemerald.validation.usage import ValidationManager
from pyemerald.weather.manager import WeatherManager


class Runner(distutils.cmd.Command):
    """A custom command to do Emerald stuff `setup.py run`"""

    description = 'Emerald blah'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if os.path.exists("/eplus/installs/EnergyPlus-22-1-0/"):
            # if I am running locally, just use my local install
            ep_install_path = "/eplus/installs/EnergyPlus-22-1-0/"
        else:
            file_name = 'EnergyPlus-22.1.0-ed759b17ee-Linux-Ubuntu20.04-x86_64.tar.gz'
            url = 'https://github.com/NREL/EnergyPlus/releases/download/v22.1.0/%s' % file_name
            extract_dir = Path(tempfile.mkdtemp())
            ep_tar_path = extract_dir / file_name
            _, headers = urllib.request.urlretrieve(url, ep_tar_path)
            extract_command = ['tar', '-xzf', file_name, '-C', extract_dir]
            check_call(extract_command, cwd=extract_dir)
            ep_install_path = extract_dir / 'EnergyPlus-22.1.0-ed759b17ee-Linux-Ubuntu20.04-x86_64'

        sys.path.insert(0, str(ep_install_path))
        from pyenergyplus.api import EnergyPlusAPI

        # set up a run dir
        this_file_path = Path(os.path.realpath(__file__))
        run_folder_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        idf_run_dir = this_file_path.parent / 'runs' / run_folder_name
        os.makedirs(idf_run_dir)

        # build out the IDF
        d = Model()
        full_idf_string = d.idf_string
        idf_path = idf_run_dir / 'emerald.idf'
        with open(idf_path, 'w') as f:
            f.write(full_idf_string)

        # initialize the API and generate a state object
        api = EnergyPlusAPI()
        state = api.state_manager.new_state()

        # register callbacks to allow weather data actuation
        search_start_index = 0
        got_handles = False
        oa_temp_actuator = -1
        dp_temp_actuator = -1
        rh_temp_actuator = -1

        weather_override_file = this_file_path.parent / 'pyemerald' / 'weather' / 'weather_underground' / '2019.json'
        with open(weather_override_file) as f:
            time_series_data = loads(f.read())['weather']

        def callback(s):
            nonlocal api, time_series_data, got_handles, oa_temp_actuator, dp_temp_actuator, rh_temp_actuator
            nonlocal search_start_index
            if not got_handles:
                if not api.exchange.api_data_fully_ready(s):
                    return
                get = api.exchange.get_actuator_handle
                oa_temp_actuator = get(s, "Weather Data", "Outdoor Dry Bulb", "Environment")
                dp_temp_actuator = get(s, "Weather Data", "Outdoor Dew Point", "Environment")
                rh_temp_actuator = get(s, "Weather Data", "Outdoor Relative Humidity", "Environment")
                if oa_temp_actuator == -1:
                    print("***Invalid handles, check spelling and sensor/actuator availability")
                    sys.exit(1)
                # once we've got the handles, let's write the available data
                with open('/tmp/available_data.csv', 'w') as f_data:
                    f_data.write(api.exchange.list_available_api_data_csv(s).decode('utf-8'))
                got_handles = True
            if api.exchange.warmup_flag(s):
                return
            current_sim_hours_into_year = api.exchange.current_sim_time(s)
            data_point_to_use = time_series_data[-1]  # assume the final item
            for i, data_point in enumerate(time_series_data):
                if i < search_start_index:
                    continue
                if data_point['time'] > current_sim_hours_into_year:
                    data_point_to_use = data_point
                    search_start_index = i
                    break
            if data_point_to_use['temp'] is not None:
                api.exchange.set_actuator_value(s, oa_temp_actuator, data_point_to_use['temp'])
            if data_point_to_use['dewPt'] is not None:
                api.exchange.set_actuator_value(s, dp_temp_actuator, data_point_to_use['dewPt'])
            if data_point_to_use['rh'] is not None:
                api.exchange.set_actuator_value(s, rh_temp_actuator, data_point_to_use['rh'])
            # eventually actuate these as well:
            # Diffuse Solar
            # Direct Solar
            # Wind Speed
            # Wind Direction

        api.runtime.callback_begin_zone_timestep_after_init_heat_balance(state, callback)
        print("Running in: " + str(idf_run_dir))
        return_val = api.runtime.run_energyplus(
            state, ['-w', str(WeatherManager().path_to_merged_epw_file()), '-d', str(idf_run_dir), str(idf_path)]
        )
        if return_val != 0:
            print("EnergyPlus failed - aborting")
            exit(return_val)

        # get EnergyPlus outputs
        sql_file = idf_run_dir / 'eplusout.sql'
        op = OutputProcessor(sql_file)
        print("EPLUS ELECTRICITY (kWh): ")
        print(op.monthly_electricity)

        # generate validation data
        v = ValidationManager()
        monthly_electricity = v.process_2019_raw_into_monthly()
        print("ACTUAL ELECTRICITY (kWh): ")
        print(monthly_electricity)

        # need gnuplot installed on the machine for this:
        r = ResultsAnalyzer(op.monthly_electricity, monthly_electricity)
        r.plot_electricity()
