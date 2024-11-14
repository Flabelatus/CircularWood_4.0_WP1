from time import sleep
import socket


class Printer:

    ip = "10.0.0.77"
    netmask = "255.255.255.0"
    port = 3000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self,IPadressInput,netmaskInput,StringValue,QRCodeValue,Velocity,Onduration):
        self.ip = IPadressInput
        self.netmask = netmaskInput

        self.setupSocket()
        self.connect()

        self.SetBarcodeAndStringValue(StringValue, QRCodeValue)
        self.print(Velocity, Onduration)
        self.disconnect()

    def setupSocket(self):
        self.s.connect((self.ip, self.port))
        print("socket connected")

    def connect(self):
        # disconnect
        self.s.send(b'CMD:D#')
        print(self.s.recv(1024), "disconnect")

        # connect
        self.s.send(b'CMD:C;admin;1234#')
        print(self.s.recv(1024), "connect")

        self.s.send(b'CMD:U;You are NOT in control !!#')
        print(self.s.recv(1024), "display message")

    def disconnect(self):
        # stop
        self.s.send(b'CMD:S#')
        print(self.s.recv(1024), "stop")
        # disconnect
        self.s.send(b'CMD:D#')
        print(self.s.recv(1024), "disconnect")

    def SetBarcodeAndStringValue(self, stringValue, QRcodeValue):
        # stop
        self.s.send(b'CMD:S#')
        print(self.s.recv(1024), "\nstop")
        sleep(0.5)

        # load file
        self.s.send(b'CMD:F,proto2#')
        print(self.s.recv(1024), "\nload file")

        # edit text size
        self.s.send(b'OBJ:Text;FON=Arial12#')
        print(self.s.recv(1024), "\nedit Test1 size")

        # edit text content
        contentString = "OBJ:Text;TEX=" + stringValue + "#"
        self.s.send(str.encode(contentString))
        print(self.s.recv(1024), "\nedit Test1 content")

        #edit barcode
        QRcodeContent = "OBJ:Barcode2;CON=" + QRcodeValue + "#"
        self.s.send(str.encode(QRcodeContent))
        print(self.s.recv(1024), "\nedit QRCODE content")

    def print(self, Velocity, OnDuration):
        # change velocity
        velocityString = "PAR;VEL=" + str(Velocity) + "#"
        self.s.send(str.encode(velocityString))
        print(self.s.recv(1024), "\nchange velocity")

        self.s.send(b'CMD:RUN#')
        print(self.s.recv(1024), "\nRUN")
        sleep(0.5)

        # start printing
        self.s.send(b'CMD:R;1#')
        print(self.s.recv(1024), "\nstart printing")
        sleep(0.5)

        self.s.send(b'CMD:RUN#')
        print(self.s.recv(1024), "\nRUN")
        sleep(OnDuration)

        print("printing for: " + str(OnDuration))
