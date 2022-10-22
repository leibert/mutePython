# mutePython
Mute the microphone of a Windows PC using mqtt. Useful if you want to add an external button to mute/unmute your microphone during conference calls. 

The script will publish the initial microphone mute state to your mqtt topic on startup, as well as any time it is changed locally on the computer. It will monitor the mqtt topic, updating the mute status of the computer when changed.

In my case, I have a switch connected to an ESP8266 running ESPHome (https://esphome.io/) to remotely update the mqtt topic, and in turn mute the microphone. I also have a stack light, also connected to an ESP8266 runing ESPHome, monitoring and responding to the mqtt topic.

ESPHOME MQTT: https://esphome.io/components/mqtt.html#on-message-trigger

Video of it in action:

https://user-images.githubusercontent.com/8097715/197355207-d9b6d1ae-79b9-49af-9e4b-dee789723447.mp4

