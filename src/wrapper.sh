#!/bin/bash

sleep 60                      # Give the system time after a reboot to connect to WiFi before continuing
export MISCALE_MAC=00:00:00:00:00:00 # Mac address of your scale
export HCI_DEV=hci0                  # Bluetooth hci device to use
export MQTT_HOST=127.0.0.1           # MQTT Server (defaults to 127.0.0.1)
export MQTT_PREFIX=miscale           # MQTT Topic Prefix. Defaults to miscale
export MQTT_USERNAME=                # Username for MQTT server (comment out if not required)
export MQTT_PASSWORD=                # Password for MQTT (comment out if not required)
export MQTT_PORT=1883                # Defaults to 1883
export TIME_INTERVAL=30              # Time in sec between each query to the scale, to allow other applications to use the Bluetooth module. Defaults to 30
export MQTT_DISCOVERY=true           # Home Assistant Discovery (true/false), defaults to true
export MQTT_DISCOVERY_PREFIX=        # Home Assistant Discovery Prefix, defaults to homeassistant

export USER1_GT=70            # If the weight is greater than this number, we'll assume that we're weighing User #1
export USER1_SEX=male
export USER1_NAME=Jo          # Name of the user
export USER1_HEIGHT=175       # Height (in cm) of the user
export USER1_DOB=1990-01-01   # DOB (in yyyy-mm-dd format)

export USER2_LT=35            # If the weight is less than this number, we'll assume that we're weighing User #2
export USER2_SEX=female
export USER2_NAME=Sarah       # Name of the user
export USER2_HEIGHT=95        # Height (in cm) of the user
export USER2_DOB=1990-01-01   # DOB (in yyyy-mm-dd format)

export USER3_SEX=female
export USER3_NAME=Missy       # Name of the user
export USER3_HEIGHT=150       # Height (in cm) of the user
export USER3_DOB=1990-01-01   # DOB (in yyyy-mm-dd format)

MY_PWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 $MY_PWD/Xiaomi_Scale.py