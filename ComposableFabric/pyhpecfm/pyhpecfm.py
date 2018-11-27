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

import requests

# the following removes the warnings for self-signed certificates
# noinspection PyUnresolvedReferences
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # pylint: disable=import-error
# noinspection PyUnresolvedReferences
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # pylint: disable=no-member

# Module level decorators

def notimplementedyet(func):
    def new_func(*args):
        msg = func.__name__ + " is not implemented yet."
        print(msg)
        return msg
    return new_func


class CFMApiError(Exception):
    """Composable Fabric Manager API exception."""
    pass


class CFMClient(object):
    """Bindings for the CFM REST API."""
    def __init__(self, host, username, password, verify_ssl=False, timeout=30):
        """
        Initialize API instance.
        :param host: str FQDN or IPv4 Address of the target CFM host
        :param username: str valid username with sufficient permissions on the CFM host
        :param password: str valid password for username var
        :param verify_ssl: bool verifies SSL certificate when communicating over HTTPS. Default
        value of False
        :param timeout: int defines the timeout value for when a API call will be marked as
        unresponsive
        """
        self._host = host
        self._username = username
        self._password = password
        self._verify_ssl = verify_ssl
        self._timeout = timeout
        self._session = None
        self._token = None

    def __del__(self):
        """Disconnect from API on instance destruction."""
        self.disconnect()

    def connect(self):
        """Connect to CFM API and retrieve token."""
        self._session = None
        self._token = None

        self._session = requests.session()
        self._session.headers.update({'Accept': 'application/json; version=1.0'})
        self._session.headers.update({'Content-Type': 'application/json'})
        self._session.headers.update({'X-Auth-Username': '{}'.format(self._username)})
        self._session.headers.update({'X-Auth-Password': '{}'.format(self._password)})

        response = self._call_api('POST', 'auth/token').json()
        self._token = response.get('result')
        if self._token:
            self._session = requests.session()
            self._session.headers.update({'Accept': 'application/json; version=1.0'})
            self._session.headers.update({'Authorization': 'Bearer {}'.format(self._token)})
            self._session.headers.update({'X-Auth-Refresh-Token': 'true'})
        else:
            print('Error getting authentication token')

    def disconnect(self):
        """Disconnect from CFM API and delete token."""
        # TODO (brian) add call to delete user token
        self._session = None
        self._token = None

    def get_switches(self, ports=False):
        """Get Composable Fabric switches.

        :param ports: bool Include ports if true. Default state is False
        :return: List of Dictionaries where each Dictionary represents a single switch object
        :rtype: list
        """
        path = 'switches'
        if ports:
            path += '?ports=true'

        return self._get(path).json().get('result')

    def get_ports(self, switch_uuid):
        """
        Get Composable Fabric switch ports.

        :param switch_uuid: switch_uuid: UUID of switch from which to fetch port data
        :return: list of Dictionary objects where each dictionary represents a port on a
        Composable Fabric Module
        :rtype: list
        """
        if switch_uuid:
            path = 'ports?switches={}&type=access'.format(switch_uuid)
            return self._get(path).json().get('result')
        else:
            return []

    def update_ports(self, port_uuids, field, value):
        """
        Function to update various attributes of composable fabric module ports
        :param port_uuids: str which represents a single unique port in a composable fabric
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
            self._patch('ports', data)
        
    def _get(self, path):
        """
        helper function used to issue HTTP get commands
        :param path: str which describes the desired path
        :return: requests.Response containing full response of API call
        :rtype: requests.Response
        """
        return self._call_api(method='GET', path=path)

    def _patch(self, path, data):

        """Execute an API PATCH request.

        Arguments:
            path (str): API request path
            data (dict): Data to send

        Returns:
            Response: The requests response object
        """
        return self._call_api(method='PATCH', path=path, data=data)

    def _post(self, path, data):
        """Execute an API POST request.

        Arguments:
            path (str): API request path
            data (dict): Data to send

        Returns:
            Response: The requests response object
        """
        return self._call_api(method='POST', path=path, data=data)

    def _call_api(self, method, path, data=None):
        """Execute an API request.

        Arguments:
            method (str): HTTP request type
            path (str): API request path
            data (dict): Data to send in dictionary format

        Returns:
            Response: The requests response object
        """
        url = 'https://{}/api/{}'.format(self._host, path)

        response = self._session.request(method=method,
                                   url=url,
                                   json=data,
                                   verify=self._verify_ssl,
                                   timeout=self._timeout)
        try:
            response.raise_for_status()
            return response
        except Exception as exception:
            raise exception
