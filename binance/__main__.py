import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder
from config.report.holder.ConfigReporterHolder import ConfigReporterHolder
from core.arguments.command_line_arguments import url_option_arg_parser
from logger.ConfigureLogger import ConfigureLogger
from metainfo.MetaInfo import MetaInfo

from binance.BinanceAccountDataStream import BinanceAccountDataStream


def start():
    ConfigureLogger()

    meta_info = MetaInfo('persuader-technology-automata-account-data-stream-binance')

    command_line_arg_parser = url_option_arg_parser(meta_info)
    args = command_line_arg_parser.parse_args()

    log = logging.getLogger('Binance Account Data Stream')
    log.info(f'Binance Account Data Stream starting with URL {args.url} OPTIONS {args.options}')

    RedisCacheHolder(args.options)

    ConfigReporterHolder(args.options)

    data_stream = BinanceAccountDataStream(args.url, args.options)
    data_stream.receive_data()


if __name__ == '__main__':
    start()
