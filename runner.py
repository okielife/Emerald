# sys.path.insert(0, "/eplus/installs/EnergyPlus-9-3-0/")
from house.data import DataManager
from pyenergyplus.api import EnergyPlusAPI
from subprocess import check_call

d = DataManager()
full_idf_string = ''
full_idf_string += d.header_data_string()
full_idf_string += d.zone_data_string()
full_idf_string += d.material_data_string()
full_idf_string += d.construction_data_string()
full_idf_string += d.surface_string()
full_idf_string += d.hvac_data_string()
full_idf_string += d.footer_data_string()
with open('/tmp/test.idf', 'w') as f:
    f.write(full_idf_string)

api = EnergyPlusAPI()
api.runtime.run_energyplus(['-w', '/eplus/epw/okc.epw', '-d', '/tmp/', '/tmp/test.idf'])
check_call(['/eplus/installs/EnergyPlus-9-3-0/PostProcess/ReadVarsESO'], cwd='/tmp')
