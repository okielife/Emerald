import distutils.cmd
import os
import tempfile
import urllib.request
from subprocess import check_call
import sys
from pyemerald.geometry.data import DataManager


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
            ep_install_path = "/eplus/installs/EnergyPlus-9-3-0/"
        else:
            file_name = 'EnergyPlus-9.3.0-baff08990c-Linux-x86_64.tar.gz'
            url = 'https://github.com/NREL/EnergyPlus/releases/download/v9.3.0/%s' % file_name
            extract_dir = tempfile.mkdtemp()
            ep_tar_path = os.path.join(extract_dir, file_name)
            _, headers = urllib.request.urlretrieve(url, ep_tar_path)
            print("*Downloaded E+ to: " + ep_tar_path)
            extract_command = ['tar', '-xzf', file_name, '-C', extract_dir]
            check_call(extract_command, cwd=extract_dir)
            print("*E+ extracted, contents of extract dir follow")
            check_call(['ls'], cwd=extract_dir)
            ep_install_path = os.path.join(extract_dir, 'EnergyPlus-9-3-0')

        sys.path.insert(0, ep_install_path)
        # noinspection PyUnresolvedReferences
        from pyenergyplus.api import EnergyPlusAPI

        d = DataManager()
        full_idf_string = ''
        full_idf_string += d.header_data_string()
        full_idf_string += d.zone_data_string()
        full_idf_string += d.material_data_string()
        full_idf_string += d.construction_data_string()
        full_idf_string += d.surface_string()
        full_idf_string += d.hvac_data_string()
        full_idf_string += d.footer_data_string()
        idf_run_dir = tempfile.mkdtemp(".idf")
        idf_path = os.path.join(idf_run_dir, 'emerald.idf')
        with open(idf_path, 'w') as f:
            f.write(full_idf_string)

        api = EnergyPlusAPI()
        print("Running in: " + idf_run_dir)
        api.runtime.run_energyplus(['-d', idf_run_dir, '-D', idf_path])
        # api.runtime.run_energyplus(['-w', '/eplus/epw/okc.epw', '-d', '/tmp/', '/tmp/test.idf'])
        # check_call(['/eplus/installs/EnergyPlus-9-3-0/PostProcess/ReadVarsESO'], cwd='/tmp')
