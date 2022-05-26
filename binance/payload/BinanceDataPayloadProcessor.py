import logging
from typing import List

from config.report.holder.ConfigReporterHolder import ConfigReporterHolder
from coreutility.collection.dictionary_utility import as_data
from coreutility.json.json_utility import as_json
from data.message.DataMessageProcessor import DataMessageProcessor
from data.payload.DataPayloadProcessor import DataPayloadProcessor


class BinanceDataPayloadProcessor(DataPayloadProcessor):

    def __init__(self, message_processors: List[DataMessageProcessor]):
        self.log = logging.getLogger(__name__)
        self.message_processors = message_processors

    def process_payload(self, payload):
        json_data = as_json(payload)
        self.log.debug(f'Payload received:{json_data}')
        payload_data = as_data(json_data, 'data')
        data_value = self.listen_data_value(payload_data)
        for message in payload_data:
            self.process_payload_message(message, data_value)

    def process_payload_message(self, payload_message, data_value):
        for message_processor in self.message_processors:
            if message_processor.get_listen_data() == data_value:
                message_processor.process_message(payload_message)
        self.post_payload_process()

    @staticmethod
    def listen_data_value(data):
        return as_data(data, 'e')

    def post_payload_process(self):
        self.log.debug('post payload processing')
        ConfigReporterHolder().delay_missing_storing()
