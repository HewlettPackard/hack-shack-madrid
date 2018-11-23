import sys
from pprint import pprint
from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

CONFIG = {
    "api_version": 600,
    "ip": "10",
    "credentials": {
        "userName": "administrator",
        "password": "password"
    }
}

#mac = sys.argv[1]

config = try_load_from_file(CONFIG)

oneview_client = OneViewClient(config)

all_servers = oneview_client.server_hardware.get_all()
#pprint(dict(all_servers[0].get_firmware()))

def SPS(fwcomponent):
    return 'SPS' in fwcomponent['componentName']

for server in all_servers:
    fw = oneview_client.server_hardware.get_firmware(server['uri'])
    sps = filter(SPS, fw['components'])
    print('Server {} is running SPS firmware {}'.format(server['name'],sps[0]['componentVersion']))
    

        