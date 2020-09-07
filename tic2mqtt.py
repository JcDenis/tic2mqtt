#!/usr/bin/env python

# TIC Teleinfo to mqtt
# Read, parse and send TIC data from French electric meter.
# https://github.com/JcDenis/tic2mqtt

# Libs
import argparse, sys, serial, json
import paho.mqtt.client as mqtt
from teleinfo import Parser
from teleinfo.hw_vendors import UTInfo2

# Functions
def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-c", "--client", help="Client name aka topic name, enedis")
    parser.add_argument("-b", "--host", help="Broker IP, localhost")
    parser.add_argument("-p", "--port", type=int, help="Broker port, 1883")
    parser.add_argument("-u", "--user", help="Broker user login")
    parser.add_argument("-w", "--password", help="Broker user password")
    parser.add_argument("-t", "--topic", help="Main topic, teleinfo")
    parser.add_argument("-i", "--interface", help="USB port, /dev/ttyUSB0")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options

def on_connect(client, obj, rc):
    if options.verbose: print("Connected to broker")

def on_disconnect(client, obj, rc):
    if options.verbose: print("Diconnected from broker")

def sanitize_frame(f):
    for k, v in f.items():
        v = v.replace("..","")
        if v.isdigit(): v = str(int(v))
        f[k] = v

# Options
options = getOptions(sys.argv[1:])

if options.verbose: print(options)

opt_client = "enedis"
if options.client: opt_client = options.client
opt_host = "localhost"
if options.host: opt_host = options.host
opt_port = 1883
if options.port: opt_port = options.port
opt_user = False
if options.user: opt_user = options.user
opt_password = False
if options.password: opt_password = options.password
opt_topic = "teleinfo"
if options.topic: opt_topic = options.topic
opt_interface = "/dev/ttyUSB0"
if options.interface: opt_interface = options.interface

# Teleinfo
tic = Parser(UTInfo2(port=opt_interface))

# MQTT
client = mqtt.Client(opt_client)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
if opt_user and opt_password:
    client.username_pw_set(opt_user, opt_password)
client.connect(opt_host, opt_port, 60)
client.loop_start()

# Loop
lio = ""
try:
    while True:
        frm = tic.get_frame()
	   sanitize_frame(frm)
        li = json.dumps(frm)
        if lio != li:
            client.publish(opt_topic + '/' + opt_client, li, 1)
            lio = li
            if options.verbose: print(li)

        elif options.verbose:
	       print("Repeated value")

except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()