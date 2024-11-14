import socket, time

class Lector_QR_Reader:
    def __init__(self):
        """
        Initializes the QR reader by creating a socket and connecting to the specified IP address and port.
        """
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        """
        Establishes a connection to the QR reader device.
        Sets a 5-second timeout for the connection attempt.
        """
        self.clientsocket.settimeout(5.0)
        self.clientsocket.connect(('10.0.0.45', 2112))
        self.NoReadItem = "NoRead"

    def sendcommand(self, command):
        """
        Sends a command to the QR reader device and waits for a response.
        Formats the command with specific delimiters and sends it over the socket.
        Sets a timeout of 8 seconds for the response.
        Parses the response and checks if it matches the sent command.
        Returns `True` if the command was executed successfully, `False` otherwise.
        """
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
        """
        Sends a command to the QR reader to start reading QR codes.
        """
        self.sendcommand(21)

    def stop_reading(self):
        """
        Sends a command to the QR reader to stop reading QR codes.
        """
        self.sendcommand(22)

    def get_NoRead_item(self):
        """
        Returns a string indicating that no QR code was read.
        """
        return self.NoReadItem
    def read_QR_Code(self):
        """
        Starts the QR code reading process.
        Continuously receives data from the QR reader until a QR code is detected or a timeout occurs.
        If a QR code is detected, it stops the reading process and returns the code.
        If a timeout occurs, it returns the "NoRead" item.
        """
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
