import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.arguments.command_line_arguments import option_arg_parser

from accountdata.BinanceAccountDataStream import BinanceAccountDataStream

if __name__ == '__main__':
    command_line_arg_parser = option_arg_parser()
    args = command_line_arg_parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logging.info(f'Binance Account Data Stream starting with URL {args.url} OPTIONS {args.options}')

    RedisCacheHolder(args.options)

    data_stream = BinanceAccountDataStream(args.url, args.options)
    data_stream.receive_data()
