#!/usr/bin/python3

import paho.mqtt.client as mqtt
import time
import sport
from datetime import datetime
import os

sport_api = sport.SportAPI

def on_connect(client,userdata,flags, rc):
    #Hier sollten alle Topics aufgelistet werden, auf welche gehört werden soll
    #Der integer-Wert im Tuple ist egal, da er nicht von der Methode verwendet wird
    client.subscribe([("req/sport/next",0),("req/sport/now",0)])

#Diese Funktion wird aufgerufen, wenn es für ein Topic kein spezielles Callback gibt
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def specific_callback(client, userdata, msg):
    print("Specific Topic: "+msg.topic+" "+str(msg.payload))

    if msg.topic == "req/sport/next":
        client.publish("sport/next", sport_api.get_next_match())
        print("sent sport/next")
    
    if msg.topic == "req/sport/now":
        client.publish("sport/now", sport_api.get_current_matches())
        print("sent sport/now")

def function2Test():
    return True

if __name__ == "__main__": # pragma: no cover
    #aufbau der MQTT-Verbindung
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    #Definition einer Callback-Funktion für ein spezielles Topic
    client.message_callback_add("req/sport/next", specific_callback)
    client.message_callback_add("req/sport/now", specific_callback)

    docker_container = os.environ.get('DOCKER_CONTAINER', False)
    if docker_container:
        mqtt_address = "broker"
    else:
        mqtt_address = "localhost"
    client.connect(mqtt_address,1883,60)
    client.loop_start()

    #Hier kann der eigene Code stehen. Loop oder Threads
    while True:
        time.sleep(100)
        #client.publish("test/Pfad/1", "asdf")
        #time.sleep(5)
        #client.publish("test/Pfad/2", "jklm")

    #Sollte am Ende stehen, da damit die MQTT-Verbindung beendet wird
    client.loop_stop()
    client.disconnect()