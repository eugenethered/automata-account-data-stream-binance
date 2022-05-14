from coreauth.repository.AuthRepository import AuthRepository
from cache.holder.RedisCacheHolder import RedisCacheHolder

if __name__ == '__main__':

    options = {
        'REDIS_SERVER_ADDRESS': '192.168.1.90',
        'REDIS_SERVER_PORT': 6379,
        'AUTH_INFO_KEY': 'binance:auth:info'
    }

    RedisCacheHolder(options)

    repository = AuthRepository(options)

    auth_info = {
        'API_KEY': '<YOUR-API_KEY>',
        'API_SECRET': '<YOUR-API_SECRET>'
    }

    repository.store(auth_info)
