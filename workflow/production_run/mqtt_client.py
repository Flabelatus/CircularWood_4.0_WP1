# The code for subscribing to the mqtt broker and parsing all the 
# messages and flags

import paho.mqtt.client as mqtt
from time import sleep

import os
import sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



#TODO take care of these imports later
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from settings import WorkflowManagerConfig
from Lector61x_V2D611D_MMSCE4 import Lector_QR_Reader
import Call_Wood_Data_Variables_For_BLUE
from ftp_handler import RAPID_FTP
#TODO

#for the lector
mqttTopic_StartScan = "PLC_coms/Stool/Scan/StartScan"
mqttTopic_ScanDone = "PLC_coms/Stool/Scan/ScanDone"

#the wood ID
mqttTopic_WoodID = "PLC_coms/Stool/WoodID"

#for BLUE data transfer
mqttTopic_Data_request = "PLC_coms/Stool/GimmeData"
mqttTopic_Publish_Data = "PLC_coms/Stool/NewStoolData"

#for RED RAPID files
mqttTopic_CB = "PLC_coms/Stool/RAPID_Needed_CB"
mqttTopic_RAPID_Fetched_Fence = 'PLC_coms/RAPID_Fetched_Fence'

mqttHost = "10.0.0.9"
mqttPort = 1883

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

woodID = 1

def on_connect(client, userdata, flags, rc,null):
    print("Connected with result code " + str(rc))
def on_subscribe(client, userdata, mid, reason_code_list, properties=None):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_message(client, userdata, msg):
    global woodID

    topic = msg.topic
    print(f"Topic: {topic}")
    if topic == str(mqttTopic_StartScan):
        print(f"Topic: scanstart")
        lector = Lector_QR_Reader()
        QR_data = lector.read_QR_Code()
        while QR_data == lector.get_NoRead_item():
            QR_data = lector.read_QR_Code()
        mqttc.publish(mqttTopic_ScanDone,QR_data, qos=2)
        #mqttc.publish("PLC_coms/Stool/WoodID",QR_data,qos=2,retain=True)
        mqttc.publish(mqttTopic_WoodID, QR_data, qos=2, retain=True)

    if topic == str(mqttTopic_Data_request):
        print(f"Topic: BLUE data request")
        get_data = Call_Wood_Data_Variables_For_BLUE.Call_Wood_Data()
        print(f"Topic: {topic}")
        data = get_data.get_wood_data_from_id(woodID)
        print(f"ID {woodID} = {data}")
        sleep(1)
        print("sending data")
        mqttc.publish(topic=mqttTopic_Publish_Data, payload=data)

    if topic == str(mqttTopic_WoodID):
        print(f"Topic: woodID")
        try:
            woodID = int(msg.payload)
        except ValueError:
            print(ValueError)

    if topic == str(mqttTopic_CB):
        print(f"Topic: RED RAPID FTP")
        rapid_ftp = RAPID_FTP(ip='10.0.0.14',user='Default User',passwd='robotics')
        rapid_ftp.RAPID_FTP_main(WoodID=woodID,
                                 msg=msg,
                                 rapid_File_Path_1="Normal__abc.mod",
                                 rapid_File_Path_2="Reversed__abc.mod",
                                 Inbetween_RAPID_Marker='\nINBETWEEN\n',
                                 targetDirectory='RED_Milling')
        mqttc.publish(mqttTopic_RAPID_Fetched_Fence, 'N/A')


def mqttSubscribe(topic):
    mqttc.subscribe(topic, qos=2)
    print("subscribed to " + topic)

if __name__ == '__main__':

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe

    mqttc.connect(mqttHost, mqttPort)

    mqttSubscribe(mqttTopic_StartScan)
    mqttSubscribe(mqttTopic_Data_request)
    mqttSubscribe(mqttTopic_WoodID)
    mqttSubscribe(mqttTopic_CB)

    mqttc.loop_forever()
