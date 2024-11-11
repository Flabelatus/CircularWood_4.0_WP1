import socket, time

class Lector_QR_Reader:
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.clientsocket.settimeout(5.0)
        self.clientsocket.connect(('10.0.0.45', 2112))
        self.NoReadItem = "NoRead"

    def sendcommand(self, command):
        payload = '\x02{}\x03'.format(command)
        print('sending {}'.format(payload))
        self.clientsocket.send(payload.encode())
        self.clientsocket.settimeout(8.0)
        response = self.clientsocket.recv(1024)
        print('sent {} and received back {}'.format(payload, response.decode()))
        if response.decode().strip().replace('\x02', '').replace('\x03', '') == '{}'.format(command):
            print('command executed and confirmed')
            return True
        else:
            return False

    def start_reading(self):
        self.sendcommand(21)

    def stop_reading(self):
        self.sendcommand(22)

    def get_NoRead_item(self):
        return self.NoReadItem
    def read_QR_Code(self):

        self.start_reading()
        reading = True
        while True:
            try:
                self.clientsocket.settimeout(8.0)
                response = self.clientsocket.recv(1024)
                print(response)
                response = response.decode().strip().replace('\x02', '').replace('\x03', '')
                print('found code:{}'.format(response))
                self.stop_reading()
                break;
            except TimeoutError:
                print('nothing received for 5s')
                response = self.get_NoRead_item()
        return response
