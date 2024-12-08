import os
import sys

from collections import namedtuple
from time import sleep

import paho.mqtt.client as mqtt

from workflow.api_http_client.api_client import http_client
from workflow.production_run.lector61x_v2d611d_mmsce4 import LectorQrCodeReader
from workflow.production_run.rapid_transfer_link import RapidTransferLink
from workflow.production_run import logger, ProductionCore
from workflow.production_run.lector61x_v2d611d_mmsce4 import LectorQrCodeReader

logger.getChild('mqtt')


class MQTTClient(ProductionCore):
    def __init__(self, data_record_id=0):
        super().__init__()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_configs = self._get_production_run_params()
        self._topics = self.mqtt_configs.mqtt.get('topics')
        self._data_record_id = data_record_id
    
    def extract_keys(self, nested_dict, parent_key=''):
        """
        Recursively extract keys from a nested dictionary.
        :param nested_dict: The dictionary to process
        :param parent_key: Used to keep track of the parent keys for nested structures
        :return: A set of keys
        """
        keys = set()
        for key, value in nested_dict.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            keys.add(full_key)
            if isinstance(value, dict):
                keys.update(self.extract_keys(value, full_key))
        return keys

    @property
    def mqtt_messages(self):
        keys = self.extract_keys(self.mqtt_topic_production)
        for k in keys:
            logger.debug(k)

        MQTTMessages = namedtuple(
            'MQTTMsg',
            field_names=[
                'start_scan',
                'scan_done',
                'wood_id',
                'wood_id_cw',
                'wood_id_cb',
                'data_request',
                'publish_data',
                'blue_ack_cw',
                'blue_ack_cb',
                'blue_req_cw',
                'blue_req_cb',
                'clamp_b',
                'rapid_fetched_cw',
                'rapid_fetched_cb',
                'rapid_needed_cw',
                'rapid_needed_cb',
            ]
        )

    @property
    def mqtt_broker_configs(self):
        return self.mqtt_configs.mqtt.get('broker_info')

    @property
    def hostname(self):
        return self.mqtt_broker_configs.get('hostname')
    
    @property
    def port(self):
        return self.mqtt_broker_configs.get('port')
    
    @property
    def mqtt_topic_production(self):
        return self._topics.get('production')
    
    @property
    def mqtt_topic_status_flags(self):
        return self._topics.get('status_flags')

    @property
    def data_record_id(self):
        return self._data_record_id

    @data_record_id.setter
    def set_data_record_id(self, new_id: int):
        self._data_record_id = new_id

    def on_connect(self, resutl_code):
        logger.info('Connected with resutl code: {0}'.format(resutl_code))
    
    def on_subscribe(self, result_code_list, properties=None):
        if result_code_list[0].is_failure:
            logger.error(f"Broker rejected you subscription: {result_code_list[0]}")
        else:
            f"Broker granted the following QoS: {result_code_list[0].value}"
    
    def on_message(self, msg):
        topic = msg.topic
        logger.info(f"Topic: {topic}")
        
        # MQTT Topics
        msg_processor_to_plc = self.mqtt_topic_production['from_plc_to_PC']
        msg_plc_to_processor = self.mqtt_topic_production['from_PC_to_plc']   
        msg_scan_done = self.mqtt_topic_production['lector']['scanDone']
        msg_topic_wood_id = self.mqtt_topic_production['lector']['woodID']
        msg_topic_clamp_b = self.mqtt_topic_production['']

        if topic == self.mqtt_topic_production.get('lector').get('scanStart'):
            logger.info('scanStart')
            lector = LectorQrCodeReader()
            qr_code_data = lector.read_qr_code()
            while qr_code_data == lector.get_no_read_item():
                qr_code_data = lector.read_qr_code()

            self.client.publish(msg_scan_done, qr_code_data, qos=2)
            self.client.publish(msg_topic_wood_id, qr_code_data, qos=2, retain=True)

        if topic == msg_processor_to_plc['blue']['request_part_data']:
            logger.info(f"Topic: BLUE data request")
            fetch_data = http_client.wood_bundle_data(self.data_record_id)
            logger.info(f"Topic: {topic}")
            logger.info(f"ID: {self.data_record_id}")
            sleep(1)
            logger.info('sending data')
            self.client.publish(msg_plc_to_processor['blue']['request_part_data'])

        if topic == msg_topic_wood_id:
            logger.info(f'Topic: woodID')
            try:
                self.set_data_record_id(int(msg.payload))
            except ValueError as e:
                logger.error(e)
        
