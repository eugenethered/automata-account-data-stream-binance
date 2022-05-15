import logging

import requests
from coreauth.Authenticator import Authenticator
from coreutility.collection.dictionary_utility import as_data


class BinanceAuthenticator(Authenticator):

    def __init__(self, options):
        super().__init__(options)
        self.auth_headers = self.build_auth_header()
        self.listen_key = None

    def should_update_url(self) -> bool:
        return True

    def update_url(self, url) -> str:
        return url.format(self.listen_key)

    async def authenticate(self):
        logging.info(f'authenticating... via auth url:{self.auth_url}')
        response = requests.post(self.auth_url, headers=self.auth_headers)
        data = response.json()
        self.listen_key = as_data(data, 'listenKey')
        logging.info('authentication complete')

    async def terminate(self):
        logging.info(f'terminating authentication... via auth url:{self.auth_url}')
        parameters = {'listenKey': self.listen_key}
        response = requests.delete(self.auth_url, headers=self.auth_headers, params=parameters)
        status = response.status_code
        logging.info(f'authentication terminated {status}')

    def build_auth_header(self):
        api_key = self.obtain_api_info()
        header = {'X-MBX-APIKEY': api_key}
        return header

    def obtain_api_info(self):
        return self.obtain_auth_value('API_KEY')
