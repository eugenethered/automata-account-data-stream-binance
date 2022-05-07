import logging
from typing import List

from data.message.DataMessageProcessor import DataMessageProcessor
from data.payload.DataPayloadProcessor import DataPayloadProcessor
from utility.json_utility import as_json, as_data


class BinanceDataPayloadProcessor(DataPayloadProcessor):

    def __init__(self, message_processors: List[DataMessageProcessor]):
        self.message_processors = message_processors

    def process_payload(self, payload):
        json_data = as_json(payload)
        logging.debug(f'Payload received:{json_data}')
        stream = as_data(json_data, 'stream')
        payload_data = as_data(json_data, 'data')
        for message in payload_data:
            self.process_payload_message(message, stream)

    def process_payload_message(self, payload_message, stream):
        for message_processor in self.message_processors:
            if message_processor.get_listen_to_stream() == stream:
                message_processor.process_message(payload_message)
