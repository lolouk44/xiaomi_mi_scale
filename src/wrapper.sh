#!/bin/bash

export MISCALE_MAC=00:00:00:00:00:00 # Mac address of your scale
export MQTT_PREFIX=miScale
#export MQTT_HOST=<YOUR-IP>  # MQTT Server (defaults to 127.0.0.1)
#export MQTT_USERNAME=        # Username for MQTT server (comment out if not required)
#export MQTT_PASSWORD=        # Password for MQTT (comment out if not required)
#export MQTT_PORT=            # Defaults to 1883
#export MQTT_TIMEOUT=30       # Defaults to 60

# Auto-gender selection/config -- This is used to create the calculations such as BMI, Water/Bone Mass etc...
# Multi user possible as long as weitghs do not overlap!

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