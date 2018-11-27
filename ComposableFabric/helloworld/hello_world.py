# (C) Copyright 2018 Hewlett Packard Enterprise Development LP.
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import time
import sys

import pyhpecfm

CFM_HOST = '10.167.0.152'
SWITCH_NAME = 'connect-vs1'

# port number lists
ALL_PORT_NUMBERS = range(1, 49)
ODD_PORT_NUMBERS = range(1, 49, 2)
EVEN_PORT_NUMBERS = range(2, 49, 2)
PORT_BYTES = [range(1, 17, 2), range(17, 33, 2), range(33, 49, 2),
              range(2, 18, 2), range(18, 34, 2), range(34, 49, 2)]

# connect to the Composable Fabric Manager API
API = pyhpecfm.CFMClient(CFM_HOST, 'admin', 'plexxi')
API.connect()


def log_to_console(text):
    """Write text to stdout and flush.
        
    Arguments:
        text (str): string to write
    """
    sys.stdout.write(text)
    sys.stdout.flush()


def get_ascii_port_numbers(text):
    """Get up to six bytes of text to switch port numbers.

    Presumes all LEDs are currently off (ports disabled)
        
    Arguments:
        text (str): string to write

    Returns:
        list(int): List of switch port numbers
    """
    port_numbers = []
    # for each character, up to six, find the '1' port numbers
    for char_index in range(min(len(text), 6)):
        # buggy conversion of ascii character to binary string
        ascii = bin(ord(text[char_index])).replace('b', '')
        for bit_index in range(len(ascii)):
            if ascii[bit_index] == '1':
                port_numbers.append(PORT_BYTES[char_index][bit_index])

    return port_numbers


def main():
    # get all of the switches
    switches = API.get_switches()
    print('Found switches {}'.format(sorted([sw['name'] for sw in switches])))

    # build a dictionary of Composable Fabric switches by name
    switch_uuids = dict([(sw['name'], sw['uuid']) for sw in switches])

    # get the UUID for our switch
    switch_uuid = switch_uuids[SWITCH_NAME]

    # get all ports on this switch
    all_ports = API.get_ports(switch_uuid)

    # make a dictionary of port UUIDs by port number
    port_uuids_by_label = {}
    for port in all_ports:
        label = port['port_label']
        uuid = port['uuid']
        port_uuids_by_label[label] = uuid

    # or an idiomatic Python equivalent of the above for loop:
    port_uuids_by_label = dict([(p['port_label'], p['uuid']) for p in all_ports])

    # output the message five times
    for _ in range(5):
        log_to_console('Sending "hello world" to {}'.format(SWITCH_NAME))

        # disable all ports to start with a blank display
        log_to_console(' . ')
        port_uuids = [port_uuids_by_label[str(n)] for n in ALL_PORT_NUMBERS]
        API.update_ports(port_uuids, 'admin_state', 'disabled')
        log_to_console(' . ')
        time.sleep(6)
        log_to_console('hello')
        port_numbers = get_ascii_port_numbers('hello')
        port_uuids = [port_uuids_by_label[str(n)] for n in port_numbers]
        API.update_ports(port_uuids, 'admin_state', 'enabled')
        log_to_console(' . ')
        time.sleep(4)
        log_to_console(' . ')
        time.sleep(4)
        log_to_console(' . ')
        # disable all ports to start with a blank display
        port_uuids = [port_uuids_by_label[str(n)] for n in ALL_PORT_NUMBERS]
        API.update_ports(port_uuids, 'admin_state', 'disabled')
        log_to_console(' . ')
        time.sleep(6)
        log_to_console('world')
        port_numbers = get_ascii_port_numbers('world')
        port_uuids = [port_uuids_by_label[str(n)] for n in port_numbers]
        API.update_ports(port_uuids, 'admin_state', 'enabled')
        log_to_console(' . ')
        time.sleep(4)
        log_to_console(' . ')
        time.sleep(4)
        log_to_console('\n')


if __name__ == '__main__':
    main()
