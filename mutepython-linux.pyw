import paho.mqtt.client as mqtt 
import time
# from dotenv import load_dotenv
import os, subprocess
import socket


mqttBroker = "mqtt.mccarthyinternet.net"
client = mqtt.Client("laptop_mutePython_"+socket.gethostname())
client.username_pw_set("mqtt", password="VZh%&u2eQc9VN@9S".encode('utf-8'))
print("will connet as laptop_mutePython_"+socket.gethostname())

#connect to mqtt broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #subcribe to topic to see if the mute status is changed remotely
    client.subscribe("laptopMuteStatus/#")
    client.subscribe("computerLock/#")


#todo port mute status to linux


#recieve mqtt message, this may be a device sending a mute command
def on_message(client, userdata, msg):
    global muteStatus

    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    topic = msg.topic
    print(topic)
    #if mute update, parse and act
    if topic == "computerLock":
        if msg.payload.decode() == "ON":
           os.popen('xdg-screensaver lock')

    elif topic == "laptopMuteStatus/muteStatus":
        if msg.payload.decode() == "ON":
    #         #set mute on computer
            os.popen("pacmd list-sources | grep -oP 'index: \d+' | awk '{ print $2 }' | xargs -I{} pactl set-source-mute {} True ")


    #         #keep track of mutestatus locally
            muteStatus=1
        else:
            os.popen("pacmd list-sources | grep -oP 'index: \d+' | awk '{ print $2 }' | xargs -I{} pactl set-source-mute {} False ")
            muteStatus=0
        #try to debounce
        time.sleep(0.1)
            


# #check if mute status has changed locally
def checkLocalMuteStatus():
    if localMuteStatus() != muteStatus:
        print("local mute status changed")
        updateMuteStatus()
    

def localMuteStatus():
    pacmdMuteStatus = 1

    #get local mute status
    pacmdResult=os.popen("pacmd list-sources | grep -oP 'muted: (?:yes|no)'").read()
    for line in pacmdResult.split("\n"):
        if line == "muted: no":
            pacmdMuteStatus=0

    return pacmdMuteStatus

# #push local mute status to mqtt
def updateMuteStatus():
    global muteStatus
#     #get mute status from computer
    tempIsMuted=localMuteStatus()
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
 