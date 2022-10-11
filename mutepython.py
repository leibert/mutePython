from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import paho.mqtt.client as mqtt 

import time
from dotenv import load_dotenv
import os 

load_dotenv()

#setup microphone as device
device = AudioUtilities.GetMicrophone()
interface = device.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
muteStatus = 0

#setup mqtt
mqttBroker = os.environ.get('mqttBroker')
client = mqtt.Client("laptop_microphone_mute")
client.username_pw_set(os.environ.get('mqttUser'), password=os.environ.get('mqttPassword'))

#connect to mqtt broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #subcribe to topic to see if the mute status is changed remotely
    client.subscribe("laptopMuteStatus/#")


def on_message(client, userdata, msg):
    global muteStatus

    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    topic = msg.topic
    print(topic)
    #if mute update, parse and act
    if topic == "laptopMuteStatus/muteStatus":
        if msg.payload.decode() == "ON":
            volume.SetMute(1, None)
            muteStatus=1
        else:
            volume.SetMute(0, None)
            muteStatus=0
            


#check if mute status has changed locally
def checkLocalMuteStatus():
    if volume.GetMute() != muteStatus:
        print("local mute status changed")
        updateMuteStatus()
    

#push local mute status to mqtt
def updateMuteStatus():
    global muteStatus
    tempIsMuted=volume.GetMute()
    if tempIsMuted == 1:
        muteStatus = 1
        client.publish("laptopMuteStatus/muteStatus", "ON")
    else:
        muteStatus = 0
        client.publish("laptopMuteStatus/muteStatus", "OFF")
    
    







# volume.GetMute()
# #volume.GetMasterVolumeLevel()
# #volume.GetVolumeRange()
# #volume.SetMasterVolumeLevel(-20.0, None)
# volume.GetMute()
# volume.SetMute(1, None)
# volume.GetMute()
# volume.SetMute(0, None)



# Main function
if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqttBroker, 1883)
    client.loop_start()

    #publish inital mute status
    updateMuteStatus()

    while True:
        checkLocalMuteStatus()
        time.sleep(.1)
 