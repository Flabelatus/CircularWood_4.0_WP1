# The code for subscribing to the mqtt broker and parsing all the
# messages and flags

import json

import paho.mqtt.client as mqtt
from time import sleep

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.production_run.Lector61x_V2D611D_MMSCE4 import Lector_QR_Reader
from workflow.production_run.ftp_handler import RAPID_FTP
from workflow.production_run.Call_Wood_Data_Variables_For_BLUE import Call_Wood_Data
from settings import WorkflowManagerConfigLoader

# mqttparams = WorkflowManagerConfigLoader().get_mqtt_network_configs()
mqttparams = WorkflowManagerConfigLoader().mqtt_network_configs
print(f"mqttparams = \n{mqttparams}")
#for the lector
mqttTopic_StartScan = mqttparams['topics']['production']['lector']['scanStart']
mqttTopic_ScanDone = mqttparams['topics']['production']['lector']['scanDone']

#the wood ID
mqttTopic_WoodID = mqttparams['topics']['production']['general']['wood_data']['woodID']
mqttTopic_WoodID_CW = "PLC_coms/Prod/WoodID/CW"
mqttTopic_WoodID_CB = "PLC_coms/Prod/WoodID/CB"
#for BLUE data transfer
mqttTopic_Data_request = mqttparams['topics']['production']['from_PC_to_plc']['blue']['request_part_data']
mqttTopic_Publish_Data = mqttparams['topics']['production']['from_plc_to_PC']['blue']['request_part_data']
mqttTopic_BLUE_Data_ACK_CW = "PLC_coms/Prod/CW_DATA_Scanned"
mqttTopic_BLUE_Data_ACK_CB = "PLC_coms/Prod/CB_DATA_Scanned"
mqttTopic_BLUE_Data_REQ_CW = "PLC_coms/Prod/BLUE_Gimmedata_CW"
mqttTopic_BLUE_Data_REQ_CB = "PLC_coms/Prod/BLUE_Gimmedata_CB"

#for RED RAPID
mqttTopic_CB = mqttparams['topics']['production']['from_PC_to_plc']['red']['fetch_rapid']['CB_RAPID_Needed']
mqttTopic_RAPID_Fetched_Fence = mqttparams['topics']['production']['from_plc_to_PC']['red']['fetch_rapid']['CB_RAPID_Fetched']

#broker information
mqttHost = mqttparams['broker_info']['hostname']

mqttPort = mqttparams['broker_info']['port']

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

woodID = 1
woodID_CW = 1
woodID_CB = 1

def on_connect(client, userdata, flags, rc, null):
    print("Connected with result code " + str(rc))

def on_subscribe(client, userdata, mid, reason_code_list, properties=None):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_message(client, userdata, msg):
    global woodID
    global woodID_CW
    global woodID_CB

    topic = msg.topic
    print(f"Topic: {topic}")

    if topic == mqttTopic_BLUE_Data_REQ_CW:
        try:
            lector = Lector_QR_Reader()
            QR_data = lector.read_QR_Code()
            while QR_data == lector.get_NoRead_item():
                QR_data = lector.read_QR_Code()

            mqttc.publish(mqttTopic_WoodID_CB, QR_data, qos=2, retain=True)

            #TODO add database call to get width from woodID, remove this line below later
            width = 225

            publishdata = dict()
            publishdata["P_AMOUNT"] = "1"
            publishdata["P1L"] = str(width)
            publishdata["P1L_len"] = len(str(width))
            json_str = json.dumps(publishdata)
            mqttc.publish(mqttTopic_BLUE_Data_ACK_CW,json_str, qos=2)
        except TimeoutError:
            print("ERROR: cant connect to lector")

    if topic == mqttTopic_BLUE_Data_REQ_CB:
        try:
            lector = Lector_QR_Reader()
            QR_data = lector.read_QR_Code()
            while QR_data == lector.get_NoRead_item():
                QR_data = lector.read_QR_Code()

            mqttc.publish(mqttTopic_WoodID_CB, QR_data, qos=2, retain=True)

            #TODO add database call to get width from woodID, remove this line below later
            width = 325

            publishdata = dict()
            publishdata["P_AMOUNT"] = "1"
            publishdata["P1L"] = str(width)
            publishdata["P1L_len"] = len(str(width))
            json_str = json.dumps(publishdata)
            mqttc.publish(mqttTopic_BLUE_Data_ACK_CB,json_str, qos=2)
        except TimeoutError:
            print("ERROR: cant connect to lector")

    if topic == str(mqttTopic_Data_request):
        try:
            print(f"Topic: BLUE data request")
            get_data = Call_Wood_Data()
            print(f"Topic: {topic}")
            data = get_data.get_wood_data_from_id(woodID)
            print(f"ID {woodID} = {data}")
            sleep(1)
            print("sending data")
            mqttc.publish(topic=mqttTopic_Publish_Data, payload=data)
        except:
            print("ERROR with calling wood data for BLUE ")

    if topic == str(mqttTopic_WoodID_CW):
        print(f"Topic: woodID_CW")
        try:
            woodID_CW = int(msg.payload)
        except ValueError:
            print(ValueError)
    if topic == str(mqttTopic_WoodID_CB):
        print(f"Topic: woodID_CB")
        try:
            woodID_CB = int(msg.payload)
        except ValueError:
            print(ValueError)

    if topic == str(mqttTopic_CB):
        print(f"Topic: RED RAPID FTP")
        try:
            ftp_params = WorkflowManagerConfigLoader().ftp_network_configs

            ip = ftp_params["red_robot"]['ip']
            user = ftp_params["red_robot"]['credentials']['username']
            passwd = ftp_params["red_robot"]['credentials']['password']

            rapid_ftp = RAPID_FTP(ip=ip, user=user, passwd=passwd)
            #TODO
            # put the old RED code back
            rapid_ftp.upload_file(inputPath="example_RAPID/Example.mod", targetDirectory="MILLING_UPLOAD",
                                  targetPath="Example_ABC_abc.mod")
            mqttc.publish(mqttTopic_RAPID_Fetched_Fence, 'N/A')
            #TODO
            # uncomment later when correct database call implementation in ftp class is done
            #
            #
            # rapid_ftp = RAPID_FTP(ip='10.0.0.14',user='Default User',passwd='robotics')
            # rapid_ftp.RAPID_FTP_main(WoodID=woodID,
            #                          msg=msg,
            #                          rapid_File_Path_1="Normal__abc.mod",
            #                          rapid_File_Path_2="Reversed__abc.mod",
            #                          Inbetween_RAPID_Marker='\nINBETWEEN\n',
            #                          targetDirectory='RED_Milling')
            # mqttc.publish(mqttTopic_RAPID_Fetched_Fence, 'N/A')
        except:
            print("error in ftp")

def on_disconnect(client, userdata, rc):
    global connected_flag
    connected_flag=False #set flag
    print("disconnected OK")

def mqttSubscribe(topic):
    mqttc.subscribe(topic, qos=2)
    print("subscribed to " + topic)
def mqttMAIN():

    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_disconnect = on_disconnect

    mqttc.connect(mqttHost, mqttPort)

    mqttSubscribe(mqttTopic_StartScan)
    mqttSubscribe(mqttTopic_Data_request)
    mqttSubscribe(mqttTopic_WoodID)
    mqttSubscribe(mqttTopic_CB)

    mqttSubscribe("PLC_coms/Prod/BLUE_Gimmedata_CB")
    mqttSubscribe("PLC_coms/Prod/BLUE_Gimmedata_CW")

    mqttc.loop_forever()

def mqttSTOP():
    mqttc.disconnect()

if __name__ == '__main__':
    mqttMAIN()
    