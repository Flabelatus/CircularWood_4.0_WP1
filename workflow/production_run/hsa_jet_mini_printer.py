import socket

from time import sleep

from generated_dataclasses import LabelPrinter, Ports
from workflow.production_run import logger, ProductionCore

logger.getChild("label_printer")


class InkJetLabelPrinter(ProductionCore):

    def __init__(self):
        super().__init__()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device_configs = self.params.label_printer
        self.device_network_configs = LabelPrinter(**self.params.tcp.label_printer)
        self.ports = Ports(**self.device_network_configs.ports)
        self.ip = self.device_network_configs.ip
        self.port = self.ports.command_port
        self.admin_usr = 'admin'
        self.admin_pwd = '1234'
        
        self.commands = {
            'disconnect': 'CMD:D#',
            'connect': f'CMD:C;{self.admin_usr};{self.admin_pwd}#',
            'stop': 'CMD:S#',
            'run': 'CMD:RUN#',
            'load_file': 'CMD:F,{0}#',
            'edit_text_size': 'OBJ:Text;FON={0}#',
            'edit_text_content': 'OBJ:Text;TEX={0}#',
            'edit_qr_code': 'OBJ:Barcode2;CON={0}#',
            'edit_velocity': 'PAR;VEL={0}#',
            'start_print': 'CMD:R;1#',
        }
        
        self.setup_tcp_socket()

    def setup_tcp_socket(self):
        try:
            self._socket.connect((self.ip, self.port))
            logger.debug("socket connected")
        except:
            logger.error("Error in `def setup_tcp_socket(self): ...`")
 
    def connect(self):
        try:
            # disconnect
            self._socket.send(self.commands.get('disconnect').encode('utf-8'))
            logger.debug(f"{self._socket.recv(1024)} disconnect")
            # connect
            self._socket.send(self.commands.get('connect').encode('utf-8'))
            logger.debug(f"{self._socket.recv(1024)} connect")
            # Print message
            self._socket.send(b'CMD:U;You are NOT in control !!#')
            logger.debug(f"{self._socket.recv(1024)} display message")
        except OSError as e:
            logger.error(f"Error in `def connect(self): ...` while trying to connect to the socket: {e}")

    def disconnect(self):
        # stop
        self._socket.send(self.commands.get('stop').encode('utf-8'))
        logger.debug(f"{self._socket.recv(1024)} stop")
        # disconnect
        self._socket.send(self.commands.get('disconnect').encode('utf-8'))
        logger.debug(f"{self._socket.recv(1024)} disconnect")

    def set_barcode_and_string_value(self, value: str, qr_code_value):
        # stop
        self._socket.send(self.commands.get('stop').encode('utf-8'))
        logger.debug(f"{self._socket.recv(1024)}\nstop")        
        sleep(0.5)
        # load file
        filename = 'proto2'
        self._socket.send(self.commands['load_file'].format(filename).encode('utf-8'))
        logger.debug(f"{self._socket.recv(1024)}\nload file")        
        # edit text size
        new_font_settings = 'Arial12'
        self._socket.send(self.commands['edit_text_size'].format(new_font_settings).encode('utf-8'))
        logger.debug(f"{self._socket.recv(1024)}\nedit Test1 size")
        # edit text content
        self._socket.send(self.commands['edit_text_content'].format(value).encode('utf-8'))
        logger.debug(f"{self.s.recv(1024)}\nedit Test1 content")
        # edit qr_code
        self._socket.send(self.commands['edit_qr_code'].format(str(qr_code_value)).encode('utf-8'))
        logger.debug(f"{self.s.recv(1024)}\nedit QRCODE content")

    def _print_label(self, velocity, on_duration):
        # change velocity
        self._socket.send(self.commands['edit_velocity'].format(str(velocity)).encode('utf-8'))
        logger.debug(f"{self.s.recv(1024)}\nchange velocity")
        # run
        self._socket.send(self.commands['run'].encode('utf-8'))
        logger.debug(f"{self.s.recv(1024)}\nRUN")
        sleep(0.5)
        # start printing
        self._socket.send(self.commands['start_print'].encode('utf-8'))
        logger.debug(f"{self.s.recv(1024)}\nstart printing")
        sleep(0.5)
        # run
        self._socket.send(self.commands['run'].encode('utf-8'))
        logger.debug(f"{self.s.recv(1024)}\nRUN")
        sleep(on_duration)
        logger.debug(f"printing for: {str(on_duration)}")

    def print_out(self, text_to_print: str = "NULL", qr_code_value: str = "0000000", velocity: float = 3.5, on_duration: int = 60):
        self.connect()
        self.set_barcode_and_string_value(text_to_print, qr_code_value)
        self._print_label(velocity, on_duration)
        self.disconnect()
