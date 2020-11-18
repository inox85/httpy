#!/usr/bin/env python

from paho.mqtt.client import Client

client = Client(client_id = "Subscriber_test")

def on_connect(client, userdata, flags, rc):
    print("Connesso con successo")

def on_message(client, userdata, message):
    print(message.payload.decode())
    

client.on_connect = on_connect
client.on_message = on_message

client.connect("inoxhome.duckdns.org")
client.subscribe("outTopic")
client.loop_forever()
