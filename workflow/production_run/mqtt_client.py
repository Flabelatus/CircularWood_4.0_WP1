import os
import sys

import json

from collections import namedtuple, defaultdict
from dataclasses import dataclass
from time import sleep

import paho.mqtt.client as mqtt

from generated_dataclasses import *
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
        self.mqtt_configs = self._get_production_run_params().mqtt
        self._topics = self.mqtt_configs.topics
        self._data_record_id = data_record_id
    
    @property
    def mqtt_nested_schema(self) -> Topics:
        return Topics(**self.mqtt_configs.topics)

    @property
    def mqtt_topic_production(self) -> Production:
        return Production(**self.mqtt_nested_schema.production)

    @property
    def mqtt_topic_status_flags(self) -> StatusFlags:
        return StatusFlags(**self.mqtt_nested_schema.status_flags)
    
    @property
    def mqtt_topic_general_production(self) -> General:
        return Production(**self.mqtt_nested_schema.production).general

    @property
    def mqtt_topic_wood_data(self) -> WoodData:
        return General(**self.mqtt_topic_general_production).wood_data

    @property
    def mqtt_topic_from_processor_to_plc(self) -> FromProcessorToPlc:
        return FromProcessorToPlc(**self.mqtt_topic_production.from_processor_to_plc)

    @property
    def mqtt_topic_from_plc_to_processor(self) -> FromPlcToProcessor:
        return FromPlcToProcessor(**self.mqtt_topic_production.from_plc_to_processor)

    @property
    def mqtt_topic_lector(self) -> Lector:
        return Lector(**self.mqtt_topic_production.lector)

    @property
    def mqtt_topic_pick_up(self) -> Pickup:
        return Pickup(**self.mqtt_topic_status_flags.pickup)

    @property
    def mqtt_topic_clamping(self) -> Clamping:
        return Clamping(**self.mqtt_topic_status_flags.clamping)

    @property
    def mqtt_broker_configs(self) -> BrokerInfo:
        return BrokerInfo(**self.mqtt_configs.broker_info)

    @property
    def hostname(self) -> str:
        return self.mqtt_broker_configs.hostname
    
    @property
    def port(self) -> str:
        return self.mqtt_broker_configs.port

    @property
    def data_record_id(self):
        """
        The ID of the material in the production in this case Wood
        
        Returns:
            (int): The primary key ID of the record in the database
        """
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
        msg_processor_to_plc = self.mqtt_topic_from_processor_to_plc
        msg_plc_to_processor = self.mqtt_topic_from_plc_to_processor   
        msg_scan_done = self.mqtt_topic_lector.scan_done

        if topic == self.mqtt_topic_production.get('lector').get('scan_start'):
            logger.info('scan_start')
            lector = LectorQrCodeReader()
            qr_code_data = lector.read_qr_code()
            while qr_code_data == lector.get_no_read_item():
                qr_code_data = lector.read_qr_code()

            self.client.publish(msg_scan_done, qr_code_data, qos=2)
            self.client.publish(self.mqtt_topic_wood_data, qr_code_data, qos=2, retain=True)

        if topic == msg_processor_to_plc['blue']['request_part_data']:
            logger.info(f"Topic: BLUE data request")
            fetch_data = http_client.wood_bundle_data(self.data_record_id)
            logger.info(f"Topic: {topic}")
            logger.info(f"ID: {self.data_record_id}")
            sleep(1)
            logger.info('sending data')
            self.client.publish(msg_plc_to_processor['blue']['request_part_data'])

        if topic == self.mqtt_topic_wood_data:
            logger.info(f'Topic: wood_id')
            try:
                self.set_data_record_id(int(msg.payload))
            except ValueError as e:
                logger.error(e)
        
