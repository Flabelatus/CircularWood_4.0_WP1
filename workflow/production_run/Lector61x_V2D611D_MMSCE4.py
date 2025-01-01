import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket

from generated_dataclasses import Lector, Ports
from workflow.production_run import logger, ProductionCore

logger.getChild('lector')


class LectorQrCodeReader(ProductionCore):
    def __init__(self):
        super().__init__()
        """
        Initializes the QR reader by creating a socket and connecting to the specified IP address and port.
        """
        self.device_title = 'Lector61x_V2D611D_MMSCE4'
        self.device_configs = self.params.lector
        self.device_network_configs = Lector(**self.params.tcp.lector)
        self.ports = Ports(**self.device_network_configs.ports)
        self.ip = self.device_network_configs.ip
        self.port = self.ports.command_port
        self.response_port = self.ports.response_port
        self.no_read_item = ""
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.connect()

    def connect(self):
        """
        Establishes a connection to the QR reader device.
        Sets a 5-second timeout for the connection attempt.
        """
        try:
            self.socket_client.settimeout(5.0)
            self.socket_client.connect((self.ip, self.port))
            self.no_read_item = "NoRead"
            logger.debug(f"Connected to device:\nip: {self.ip}, port: {self.port}, response_port: {self.response_port}")
        except OSError as e:
            logger.error(f"Error in `def connect(self): ...` while trying to connect to the socket: {e}")

    def send_command(self, command):
        """
        Sends a command to the QR reader device and waits for a response.
        Formats the command with specific delimiters and sends it over the socket.
        Sets a timeout of 8 seconds for the response.
        Parses the response and checks if it matches the sent command.
        Returns `True` if the command was executed successfully, `False` otherwise.
        """
        payload = '\x02{}\x03'.format(command)
        logger.debug('sending {0}'.format(payload))

        self.socket_client.send(payload.encode())
        self.socket_client.settimeout(8.0)
        
        response = self.socket_client.recv(self.response_port)
        logger.debug('sent {0} and received back {1}'.format(payload, response.decode()))

        if response.decode().strip().replace('\x02', '').replace('\x03', '') == '{0}'.format(command):
            logger.debug('command executed and confirmed')
            return True
        else:
            return False

    def start_reading(self):
        """
        Sends a command to the QR reader to start reading QR codes.
        """
        self.send_command(21)

    def stop_reading(self):
        """
        Sends a command to the QR reader to stop reading QR codes.
        """
        self.send_command(22)

    def get_no_read_item(self):
        """
        Returns a string indicating that no QR code was read.
        """
        return self.no_read_item
    
    def read_qr_code(self):
        """
        Starts the QR code reading process.
        Continuously receives data from the QR reader until a QR code is detected or a timeout occurs.
        If a QR code is detected, it stops the reading process and returns the code.
        If a timeout occurs, it returns the "NoRead" item.
        """
        self.start_reading()
        reading = True
        while reading:
            try:
                self.socket_client.settimeout(8.0)
                response = self.socket_client.recv(self.response_port)
                logger.debug(response)
                response = response.decode().strip().replace('\x02', '').replace('\x03', '')
                logger.debug('found code:{}'.format(response))
                self.stop_reading()
                break;
            except TimeoutError as e:
                logger.error(f'nothing received for 5s: {e}')
                response = self.get_no_read_item()
        return response
