import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder
from cache.provider.RedisCacheProviderWithHash import RedisCacheProviderWithHash
from config.report.holder.ConfigReporterHolder import ConfigReporterHolder
from core.environment.EnvironmentVariables import EnvironmentVariables
from logger.ConfigureLogger import ConfigureLogger

from binance.BinanceAccountDataStream import BinanceAccountDataStream


def start():
    ConfigureLogger()

    environment_variables = EnvironmentVariables()

    log = logging.getLogger('Binance Account Data Stream')
    log.info(f'Binance Account Data Stream starting with URL {environment_variables.url()}')

    RedisCacheHolder(environment_variables.options, held_type=RedisCacheProviderWithHash)

    ConfigReporterHolder(environment_variables.options)

    data_stream = BinanceAccountDataStream(environment_variables.url(), environment_variables.options)
    data_stream.receive_data()


if __name__ == '__main__':
    start()
