from ctypes import cast, POINTER, windll
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import paho.mqtt.client as mqtt 

import time
from dotenv import load_dotenv
import os
import socket 

# load_dotenv(dotenv_path=".env")

#setup microphone as device
device = AudioUtilities.GetMicrophone()
interface = device.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
muteStatus = 0

#setup mqtt
# mqttBroker = os.environ.get('mqttBroker')
# client = mqtt.Client("laptop_microphone_mute")
# client.username_pw_set(os.environ.get('mqttUser'), password=os.environ.get('mqttPassword'))
mqttBroker = "mqtt.mccarthyinternet.net"
client = mqtt.Client("laptop_mutePython_"+socket.gethostname())
client.username_pw_set("mqtt", password="VZh%&u2eQc9VN@9S".encode('utf-8'))
print("connecting as laptop_mutePython_"+socket.gethostname())

#connect to mqtt broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #subcribe to topic to see if there is a mqtt message sent
    client.subscribe("computerLock/#")

#recieve mqtt message, this may be a device sending a mute command
def on_message(client, userdata, msg):
    global muteStatus

    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    topic = msg.topic
    print(topic)
    #if mute update, parse and act
    if topic == "computerLock":
        if msg.payload.decode() == "ON":
            windll.user32.LockWorkStation()

         
# Main function
if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqttBroker, 1883)
    client.loop()

    while True:
        time.sleep(.1)
 