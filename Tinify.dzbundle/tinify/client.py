# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import platform
import requests
import requests.exceptions
from requests.compat import json
import traceback

import tinify
from .errors import ConnectionError, Error

class Client(object):
    API_ENDPOINT = 'https://api.tinify.com'
    USER_AGENT = 'Tinify/{0} Python/{1} ({2})'.format(tinify.__version__, platform.python_version(), platform.python_implementation())

    def __init__(self, key, app_identifier=None):
        self.session = requests.sessions.Session()
        self.session.auth = ('api', key)
        self.session.headers = {
            'user-agent': self.USER_AGENT + ' ' + app_identifier if app_identifier else self.USER_AGENT,
        }
        self.session.verify = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'cacert.pem')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self.session.close()

    def request(self, method, url, body=None, header={}):
        url = url if url.lower().startswith('https://') else self.API_ENDPOINT + url
        params = {}
        if isinstance(body, dict):
            if body:
                # Dump without whitespace.
                params['headers'] = {'Content-Type': 'application/json'}
                params['data'] = json.dumps(body, separators=(',', ':'))
        elif body:
            params['data'] = body

        try:
            response = self.session.request(method, url, **params)
        except requests.exceptions.Timeout as err:
            raise ConnectionError('Timeout while connecting', cause=err)
        except Exception as err:
            raise ConnectionError('Error while connecting: {0}'.format(err), cause=err)

        count = response.headers.get('compression-count')
        if count:
            tinify.compression_count = int(count)

        if response.ok:
            return response
        else:
            details = None
            try:
                details = response.json()
            except Exception as err:
                details = {'message': 'Error while parsing response: {0}'.format(err), 'error': 'ParseError'}
            raise Error.create(details.get('message'), details.get('error'), response.status_code)
