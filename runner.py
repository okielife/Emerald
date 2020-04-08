from datetime import datetime
import distutils.cmd
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
        if os.path.exists("/eplus/installs/EnergyPlus-9-3-0/"):
            # if I am running locally, just use my local install
            ep_install_path = "/eplus/installs/EnergyPlus-9-3-0/"
        else:
            file_name = 'EnergyPlus-9.3.0-baff08990c-Linux-x86_64.tar.gz'
            url = 'https://github.com/NREL/EnergyPlus/releases/download/v9.3.0/%s' % file_name
            extract_dir = Path(tempfile.mkdtemp())
            ep_tar_path = extract_dir / file_name
            _, headers = urllib.request.urlretrieve(url, ep_tar_path)
            extract_command = ['tar', '-xzf', file_name, '-C', extract_dir]
            check_call(extract_command, cwd=extract_dir)
            ep_install_path = extract_dir / 'EnergyPlus-9.3.0-baff08990c-Linux-x86_64'

        sys.path.insert(0, str(ep_install_path))
        # noinspection PyUnresolvedReferences
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

        # run the IDF using the EnergyPlus API (cool!)
        api = EnergyPlusAPI()
        print("Running in: " + str(idf_run_dir))
        return_val = api.runtime.run_energyplus(
            ['-w', str(WeatherManager.path_to_tmy_okc_epw_file()), '-d', str(idf_run_dir), str(idf_path)]
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
