# This would be the secondary Flask app to add the endpoints in order to orchestrate 
# all the workflows and processes of the production in the factory.
# In the end run this app and the primary app.py file as separate services containerized
import logging

# I make the app = Flask(__name__)

# MQTT CLient importing your script... and run it

# Deliver RAPID to Blue
# /run

from scripts.mqtt_client import mqttMAIN,mqttSTOP
from flask import Flask
app = Flask(__name__)

mqttConnectionFLag = False

@app.route('/')
def index():
    return "use /start to start the mqtt client and use /stop to stop the mqtt client"

@app.route('/start')
def mqtt_start():
    global mqttConnectionFLag
    if mqttConnectionFLag != True:
        print("mqtt started")
        mqttConnectionFLag = True
        #TODO IN DIFFERENT THREAD!
        mqttMAIN()
    else:
        print("mqtt already started")
        return "MQTT ALREADY STARTED"
    return "MQTT STARTED"

@app.route('/stop')
def mqtt_stop():
    logger = logging.getLogger("mqtt_client")
    logger.debug('mqtt_stop')
    global mqttConnectionFLag
    print("mqtt stopped")
    try:
        mqttConnectionFLag = False
        mqttSTOP()
    except TypeError as e:
        pass
    return "MQTT STOPPED"


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
