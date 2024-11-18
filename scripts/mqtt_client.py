# The code for subscribing to the mqtt broker and parsing all the
# messages and flags

import paho.mqtt.client as mqtt
from time import sleep

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.production_run.Lector61x_V2D611D_MMSCE4 import Lector_QR_Reader
from workflow.production_run.ftp_handler import RAPID_FTP
from workflow.production_run.Call_Wood_Data_Variables_For_BLUE import Call_Wood_Data
from settings import WorkflowManagerConfig

mqttparams = WorkflowManagerConfig().get_mqtt_network_configs()


#for the lector
mqttTopic_StartScan = mqttparams['topic']['production']['lector']['scanStart']
mqttTopic_ScanDone = mqttparams['topic']['production']['lector']['scanDone']

#the wood ID
mqttTopic_WoodID = mqttparams['topic']['production']['general']['wood_data']['woodID']

#for BLUE data transfer
mqttTopic_Data_request = mqttparams['topic']['production']['from_PC_to_plc']['blue']['request_part_data']
mqttTopic_Publish_Data = mqttparams['topic']['production']['from_plc_to_PC']['blue']['request_part_data']

#for RED RAPID
mqttTopic_CB = mqttparams['topic']['production']['from_PC_to_plc']['red']['fetch_rapid']['CB_RAPID_Needed']
mqttTopic_RAPID_Fetched_Fence = mqttparams['topic']['production']['from_plc_to_PC']['red']['fetch_rapid']['CB_RAPID_Fetched']

#broker information
mqttHost = mqttparams['broker']['hostname']
mqttPort = mqttparams['broker']['port']

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

woodID = 1

def on_connect(client, userdata, flags, rc, null):
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
        try:
            lector = Lector_QR_Reader()
            QR_data = lector.read_QR_Code()
            while QR_data == lector.get_NoRead_item():
                QR_data = lector.read_QR_Code()
            mqttc.publish(mqttTopic_ScanDone,QR_data, qos=2)
            #mqttc.publish("PLC_coms/Stool/WoodID",QR_data,qos=2,retain=True)
            mqttc.publish(mqttTopic_WoodID, QR_data, qos=2, retain=True)
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

    if topic == str(mqttTopic_WoodID):
        print(f"Topic: woodID")
        try:
            woodID = int(msg.payload)
        except ValueError:
            print(ValueError)

    if topic == str(mqttTopic_CB):
        print(f"Topic: RED RAPID FTP")
        try:
            ftp_params = WorkflowManagerConfig().get_ftp_params()

            ip = ftp_params["RED"]['ip']
            user = ftp_params["RED"]['username']
            passwd = ftp_params["RED"]['password']

            rapid_ftp = RAPID_FTP(ip=ip, user=user, passwd=passwd)
            #TODO
            # put the old RED code back
            rapid_ftp.upload_file(inputPath="example_RAPID/Example.mod", targetDirectory="MILLING_UPLOAD",
                                  targetPath="Example.mod")
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

    mqttc.loop_forever()

def mqttSTOP():
    mqttc.disconnect()

if __name__ == '__main__':
    mqttMAIN()
    