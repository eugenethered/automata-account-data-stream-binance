import logging

import requests
from coreauth.Authenticator import Authenticator
from coreutility.collection.dictionary_utility import as_data


class BinanceAuthenticator(Authenticator):

    def __init__(self, options):
        super().__init__(options)
        self.listen_key = None

    def should_update_url(self) -> bool:
        return True

    def update_url(self, url) -> str:
        return url.format(self.listen_key)

    def authenticate(self):
        logging.info(f'authenticating... via auth url:{self.auth_url}')
        api_key = self.obtain_api_info()
        headers = {'X-MBX-APIKEY': api_key}
        response = requests.post(self.auth_url, headers=headers)
        data = response.json()
        self.listen_key = as_data(data, 'listenKey')
        logging.info(f'authentication complete via url:{self.auth_url}')

    def obtain_api_info(self):
        return self.obtain_auth_value('API_KEY')
