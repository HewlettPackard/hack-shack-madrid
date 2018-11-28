# -*- coding: utf-8 -*-
"""
This module is used for testing the functions within the pyawair.objects module.
"""

from unittest import TestCase
from unittest import mock
from pyhpecfm.auth import CFMClient
from pyhpecfm.fabric import *

#TODO TAKE OUT HARDCODED DATA LATER
client= CFMClient('10.167.1.5', 'admin', 'plexxi')

class TestGetSwitches(TestCase):
    """
    Test Case for pyhpecfm.fabric get_switches function
    """

    def test_get_switches(self):
        """
        """
        test_switches = get_switches(client)
        my_attributes = ['fabric_uuid', 'fitting_number', 'ip_gateway', 'hostip_state', 'ip_address_v6', 'uuid', 'ip_mode', 'ip_gateway_v6', 'health', 'mac_address', 'ip_mode_v6', 'serial_number', 'status', 'description', 'ip_address', 'model', 'hw_revision', 'sw_version', 'name', 'ip_mask', 'configuration_number', 'operational_stage', 'ip_mask_v6']
        self.assertIs(type(test_switches), list)
        self.assertIs(type(test_switches[0]), dict)
        for i in test_switches[0].keys():
            self.assertIn(i, my_attributes)

class TestGetPorts(TestCase):
    """
    Test case for pyhpecfm.fabric get_ports function
    """
    def test_get_switches(self):
        """
        """
        test_switches = get_switches(client)
        test_switch = test_switches[0]['uuid']
        ports_list = get_ports(client, test_switch)
        my_attributes = ['native_vlan', 'description', 'speed_group', 'ungrouped_vlans', 'link_state', 'switch_uuid', 'admin_state', 'form_factor', 'port_security_enabled', 'vlans', 'speed', 'switch_name', 'fec', 'read_only', 'port_label', 'uuid', 'is_uplink', 'vlan_group_uuids', 'name', 'permitted_qsfp_modes', 'silkscreen', 'type', 'bridge_loop_detection', 'qsfp_mode']
        self.assertIs(type(ports_list), list)
        self.assertIs(type(ports_list[0]), dict)
        for i in ports_list[0].keys():
            self.assertIn(i, my_attributes)


class TestUpdatePorts(TestCase):
    """
    Test
    case for pyhpecfm.fabric update_ports function
    """
    def setUp(self):
        test_switches = get_switches(client)
        test_switch = test_switches[0]['uuid']
        port_list = get_ports(client, test_switch)
        target_port = [port_list[0]['uuid']]
        update_ports(client, target_port, 'admin_state', 'enabled')
        port_list = get_ports(client, test_switch)
        self.assertEqual(port_list[0]['admin_state'], 'enabled')
    def test_disable_port(self):
        target_port = [port_list[0]['uuid']]
        update_ports(client, target_port, 'admin_state', 'disabled')
        port_list = get_ports(client, test_switch)
        self.assertEqual(port_list[0]['admin_state'], 'disabled')




