import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder

from binance.auth.BinanceAuthenticator import BinanceAuthenticator

if __name__ == '__main__':

    options = {
        'REDIS_SERVER_ADDRESS': '10.104.71.60',
        'REDIS_SERVER_PORT': 6379,
        'AUTH_INFO_KEY': 'binance:auth:info',
        'AUTH_URL': 'https://api.binance.com/api/v3/userDataStream'
    }

    logging.basicConfig(level=logging.DEBUG)

    RedisCacheHolder(options)

    authenticator = BinanceAuthenticator(options)
    authenticator.authenticate()

    print(f'listen key -> {authenticator.listen_key}')
