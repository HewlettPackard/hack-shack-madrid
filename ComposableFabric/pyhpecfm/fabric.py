#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_switches(cfmclient, ports=False):
    """Get Composable Fabric switches.

    """
    path = 'switches'
    if ports:
        path += '?ports=true'

    return cfmclient.get(path).json().get('result')


def get_ports(cfmclient, switch_uuid):
    """
    Get Composable Fabric switch ports.

    :param switch_uuid: switch_uuid: UUID of switch from which to fetch port data
    :return: list of Dictionary objects where each dictionary represents a port on a
    Composable Fabric Module
    :rtype: list
    """
    if switch_uuid:
        path = 'ports?switches={}&type=access'.format(switch_uuid)
        return cfmclient.get(path).json().get('result')
    else:
        return []


def update_ports(cfmclient, port_uuids, field, value):
    """
    Function to update various attributes of composable fabric module ports
    :param port_uuids: list of str where each string represents a single unique port in a
    composable fabric
    :param field: str specific field which is desired to be modified (case-sensitive)
    :param value: str specific field which sets the new desired value for the field
    :return: dict which contains count, result, and time of the update
    :rtype: dict
    """
    if port_uuids:
        data = [{
            'uuids': port_uuids,
            'patch': [
                {
                    'path': '/{}'.format(field),
                    'value': value,
                    'op': 'replace'
                }
            ]
        }]
        cfmclient.patch('ports', data)
