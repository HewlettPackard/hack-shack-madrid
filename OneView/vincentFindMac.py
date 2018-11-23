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

all_sp = oneview_client.server_profiles.get_all()

def search_mac(mac):
    for sp in all_sp:
        for conn in sp['connectionSettings']['connections']:
            if conn['mac'] == mac:
                print('Found {} ! in server profile {name}'.format(mac,**sp))
                server = oneview_client.server_hardware.get_by('serverProfileUri',sp['uri'])
                print('Assigned to {name}, OS name: {serverName}'.format(**server[0]))
                return

search_mac(sys.argv[1])
        