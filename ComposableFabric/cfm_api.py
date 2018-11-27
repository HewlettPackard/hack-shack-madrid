# -*- coding: utf-8 -*-
##########################################################################
#
# Copyright (c) 2018, HPE Inc. and its licensors.
#
# All rights reserved.
#
# Use and duplication of this software is subject to a separate license
# agreement between the user and HPE or its licensor.
#
##########################################################################

import requests
# noinspection PyUnresolvedReferences
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # pylint: disable=import-error
# noinspection PyUnresolvedReferences
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # pylint: disable=no-member


class CFMApiError(Exception):
    """Composable Fabric Manager API exception."""

    pass


class CFMAPI(object):
    """Bindings for the CFM REST API."""

    def __init__(self):
        """Initialize API instance."""
        self._host = '10.167.0.152'
        self._username = 'admin'
        self._password = 'plexxi'
        self._verify_ssl = False
        self._timeout = 30
        self._session = None
        self._token = None

    def connect(self, host=None):
        """Test connection to CFM REST API and update token."""
        self._session = None
        self._token = None

        if host:
            self._host = host

        with requests.session() as session:
            session.headers.update({'Accept': 'application/json; version=1.0'})
            session.headers.update({'Content-Type': 'application/json'})
            session.headers.update({'X-Auth-Username': '{}'.format(self._username)})
            session.headers.update({'X-Auth-Password': '{}'.format(self._password)})
            response = self._process_request(session, 'POST', 'auth/token').json()
            self._token = response.get('result')

        if self._token:
            self._session = requests.session()
            self._session.headers.update({'Accept': 'application/json; version=1.0'})
            self._session.headers.update({'Authorization': 'Bearer {}'.format(self._token)})
            self._session.headers.update({'X-Auth-Refresh-Token': 'true'})
        else:
            print 'Error getting authentication token'

    def get_switches(self, ports=False):
        """Get Composable Fabric switches.

        Arguments:
            ports (boolean): Include ports if true

        Returns:
            list(dict): List of switches
        """
        path = 'switches'
        if ports:
            path += '?ports=true'

        return self._get(path).json().get('result')

    def get_ports(self, switch_uuid):
        """Get Composable Fabric switch ports.
        
        Arguments:
            switch_uuid (str): UUID of switch from which to fetch port data
        """
        if switch_uuid:
            path = 'ports?switches={}&type=access'.format(switch_uuid)
            return self._get(path).json().get('result')
        else:
            return []

    def update_ports(self, port_uuids, field, value):
        """Update ports.
    
        Arguments:
            port_uuids (list[str]): Port UUIDs to update
            field (str): port property to update
            value (str): value for port property
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
        """Execute an API GET request.

        Arguments:
            path (str): API request path

        Returns:
            Response: The requests response object
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
        if self._session:
            return self._process_request(self._session, method, path, data)
        else:
            with requests.session() as session:
                session.headers.update({'Accept': 'application/json'})
                session.headers.update({'Authorization': '{}'.format(self._token)})
                return self._process_request(session, method, path, data)

    def _process_request(self, session, method, path, data=None):
        """Execute an API request with the supplied session.

        Arguments:
            session (requests.Session): The session to use to issue the HTTP request
            method (str): HTTP request type
            path (str): API request path
            data (dict): Data to send in dictionary format

        Returns:
            Response: The requests response object
        """
        url = 'https://{}/api/{}'.format(self._host, path)

        response = session.request(method=method,
                                   url=url,
                                   json=data,
                                   verify=self._verify_ssl,
                                   timeout=self._timeout)
        try:
            response.raise_for_status()
            return response
        except Exception as exception:
            raise exception
