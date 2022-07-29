from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash
from processrepo.ProcessRunProfile import ProcessRunProfile, RunProfile
from processrepo.repository.ProcessRunProfileRepository import ProcessRunProfileRepository

if __name__ == '__main__':

    options = {
        'REDIS_SERVER_ADDRESS': '10.104.71.60',
        'REDIS_SERVER_PORT': 6379,
        'PROCESS_RUN_PROFILE_KEY': 'binance:process:mv:run-profile'
    }

    RedisCacheHolder(options, held_type=RedisCacheProviderWithHash)

    process_run_profile = ProcessRunProfile('binance', 'account-data-stream', RunProfile.ASAP, True)

    repository = ProcessRunProfileRepository(options)
    repository.store(process_run_profile)

    print('Account Data Stream Process Run Profile stored!')
