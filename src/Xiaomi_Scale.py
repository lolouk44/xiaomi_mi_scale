#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import binascii
import time
import os
import sys
import subprocess
from bluepy import btle
from bluepy.btle import Scanner, BTLEDisconnectError, BTLEManagementError, DefaultDelegate
import paho.mqtt.publish as publish
from datetime import datetime
import json

import Xiaomi_Scale_Body_Metrics



# First Log msg
sys.stdout.write(' \n')
sys.stdout.write('-------------------------------------\n')
sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting Xiaomi mi Scale...\n")

# Configuraiton...
# Trying To Load Config From options.json (HA Add-On)
try:
    with open('/data/options.json') as json_file:
        sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Loading Config From Add-On Options...\n")
        data = json.load(json_file)
        try:
            MISCALE_MAC = data["MISCALE_MAC"]
        except:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - MAC Address not provided...\n")
            raise
        try:
            MQTT_USERNAME = data["MQTT_USERNAME"]
        except:
            MQTT_USERNAME = "username"
            pass
        try:
            MQTT_PASSWORD = data["MQTT_PASSWORD"]
        except:
            MQTT_PASSWORD = None
            pass
        try:
            MQTT_HOST = data["MQTT_HOST"]
        except:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - MQTT Host not provided...\n")
            raise
        try:
            MQTT_PORT = int(data["MQTT_PORT"])
        except:
            MQTT_PORT = 1883
            pass
        try:
            MQTT_PREFIX = data["MQTT_PREFIX"]
        except:
            MQTT_PREFIX = "miscale"
            pass
        try:
            TIME_INTERVAL = int(data["TIME_INTERVAL"])
        except:
            TIME_INTERVAL = 30
            pass
        try:
            MQTT_DISCOVERY = data["MQTT_DISCOVERY"]
        except:
            MQTT_DISCOVERY = True
            pass
        try:
            MQTT_DISCOVERY_PREFIX = data["MQTT_DISCOVERY_PREFIX"]
        except:
            MQTT_DISCOVERY_PREFIX = "homeassistant"
            pass
        try:
            HCI_DEV = data["HCI_DEV"][-1]
        except:
            HCI_DEV = "hci0"[-1]
            pass
        try:
            USER1_GT = int(data["USER1_GT"])
        except:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - USER1_GT not provided...\n")
            raise
        try:
            USER1_SEX = data["USER1_SEX"]
        except:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - USER1_SEX not provided...\n")
            raise
        try:
            USER1_NAME = data["USER1_NAME"]
        except:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - USER1_NAME not provided...\n")
            raise
        try:
            USER1_HEIGHT = int(data["USER1_HEIGHT"])
        except:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - USER1_HEIGHT not provided...\n")
            raise
        try:
            USER1_DOB = data["USER1_DOB"]
        except:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - USER1_DOB not provided...\n")
            raise
        try:
            USER2_LT = int(data["USER2_LT"])
        except:
            USER2_LT = USER1_GT
            pass
        try:
            USER2_SEX = data["USER2_SEX"]
        except:
            USER2_SEX = "female"
            pass
        try:
            USER2_NAME = data["USER2_NAME"]
        except:
            USER2_NAME = "Serena"
            pass
        try:
            USER2_HEIGHT = int(data["USER2_HEIGHT"])
        except:
            USER2_HEIGHT = 95
            pass
        try:
            USER2_DOB = data["USER2_DOB"]
        except:
            USER2_DOB = "1990-01-01"
            pass
        try:
            USER3_SEX = data["USER3_SEX"]
        except:
            USER3_SEX = "female"
            pass
        try:
            USER3_NAME = data["USER3_NAME"]
        except:
            USER3_NAME = "Missy"
            pass
        try:
            USER3_HEIGHT = int(data["USER3_HEIGHT"])
        except:
            USER3_HEIGHT = 150
            pass
        try:
            USER3_DOB = data["USER3_DOB"]
        except:
            USER3_DOB = "1990-01-01"
            pass
        sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Config Loaded...\n")

# Failed to open options.json, Loading Config From Environment (Not HA Add-On)
except FileNotFoundError:
    pass
    sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Loading Config From OS Environment...\n")
    MISCALE_MAC = os.getenv('MISCALE_MAC', '')
    MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'username')
    MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', None)
    MQTT_HOST = os.getenv('MQTT_HOST', '127.0.0.1')
    MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
    MQTT_PREFIX = os.getenv('MQTT_PREFIX', 'miscale')
    TIME_INTERVAL = int(os.getenv('TIME_INTERVAL', 30))
    MQTT_DISCOVERY = os.getenv('MQTT_DISCOVERY',True)
    MQTT_DISCOVERY_PREFIX = os.getenv('MQTT_DISCOVERY_PREFIX','homeassistant')
    HCI_DEV = os.getenv('HCI_DEV', 'hci0')[-1]

    # User Variables...
    USER1_GT = int(os.getenv('USER1_GT', '70')) # If the weight is greater than this number, we'll assume that we're weighing User #1
    USER1_SEX = os.getenv('USER1_SEX', 'male')
    USER1_NAME = os.getenv('USER1_NAME', 'David') # Name of the user
    USER1_HEIGHT = int(os.getenv('USER1_HEIGHT', '175')) # Height (in cm) of the user
    USER1_DOB = os.getenv('USER1_DOB', '1988-09-30') # DOB (in yyyy-mm-dd format)

    USER2_LT = int(os.getenv('USER2_LT', '55')) # If the weight is less than this number, we'll assume that we're weighing User #2
    USER2_SEX = os.getenv('USER2_SEX', 'female')
    USER2_NAME = os.getenv('USER2_NAME', 'Joanne') # Name of the user
    USER2_HEIGHT = int(os.getenv('USER2_HEIGHT', '155')) # Height (in cm) of the user
    USER2_DOB = os.getenv('USER2_DOB', '1988-10-20') # DOB (in yyyy-mm-dd format)

    USER3_SEX = os.getenv('USER3_SEX', 'male')
    USER3_NAME = os.getenv('USER3_NAME', 'Unknown User') # Name of the user
    USER3_HEIGHT = int(os.getenv('USER3_HEIGHT', '175')) # Height (in cm) of the user
    USER3_DOB = os.getenv('USER3_DOB', '1988-01-01') # DOB (in yyyy-mm-dd format)
    sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Config Loaded...\n")

OLD_MEASURE = ''

def discovery():
    for MQTTUser in (USER1_NAME,USER2_NAME,USER3_NAME):
        message = '{"name": "' + MQTTUser + ' Weight",'
        message+= '"state_topic": "miscale/' + MQTTUser + '/weight","value_template": "{{ value_json.weight }}","unit_of_measurement": "kg",'
        message+= '"json_attributes_topic": "miscale/' + MQTTUser + '/weight","icon": "mdi:scale-bathroom"}'
        publish.single(
                        MQTT_DISCOVERY_PREFIX + '/sensor/' + MQTT_PREFIX + '/' + MQTTUser + '/config',
                        message,
                        retain=True,
                        hostname=MQTT_HOST,
                        port=MQTT_PORT,
                        auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD}
                    )
    sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Discovery Completed...\n")


class ScanProcessor():
    def GetAge(self, d1):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(datetime.today().strftime('%Y-%m-%d'),'%Y-%m-%d')
        return abs((d2 - d1).days)/365

    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        global OLD_MEASURE
        if dev.addr == MISCALE_MAC.lower() and isNewDev:
            for (sdid, desc, data) in dev.getScanData():
                ### Xiaomi V1 Scale ###
                if data.startswith('1d18') and sdid == 22:
                    measunit = data[4:6]
                    sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Measuring Unit: {measunit}\n")
                    measured = int((data[8:10] + data[6:8]), 16) * 0.01
                    sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Measured Raw Weight: {measured}\n")
                    unit = ''
                    if measunit.startswith(('03', 'a3')): unit = 'lbs'
                    if measunit.startswith(('12', 'b2')): unit = 'jin'
                    if measunit.startswith(('22', 'a2')): unit = 'kg' ; measured = measured / 2
                    if unit:
                        if OLD_MEASURE != round(measured, 2):
                            self._publish(round(measured, 2), unit, str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')), "", "")
                            OLD_MEASURE = round(measured, 2)

                ### Xiaomi V2 Scale ###
                if data.startswith('1b18') and sdid == 22:
                    data2 = bytes.fromhex(data[4:])
                    ctrlByte1 = data2[1]
                    isStabilized = ctrlByte1 & (1<<5)
                    hasImpedance = ctrlByte1 & (1<<1)

                    measunit = data[4:6]
                    measured = int((data[28:30] + data[26:28]), 16) * 0.01
                    unit = ''
                    if measunit == "03": unit = 'lbs'
                    if measunit == "02": unit = 'kg' ; measured = measured / 2
                    #mitdatetime = datetime.strptime(str(int((data[10:12] + data[8:10]), 16)) + " " + str(int((data[12:14]), 16)) +" "+ str(int((data[14:16]), 16)) +" "+ str(int((data[16:18]), 16)) +" "+ str(int((data[18:20]), 16)) +" "+ str(int((data[20:22]), 16)), "%Y %m %d %H %M %S")
                    miimpedance = str(int((data[24:26] + data[22:24]), 16))
                    if unit and isStabilized:
                        if OLD_MEASURE != round(measured, 2) + int(miimpedance):
                            self._publish(round(measured, 2), unit, str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')), hasImpedance, miimpedance)
                            OLD_MEASURE = round(measured, 2) + int(miimpedance)


    def _publish(self, weight, unit, mitdatetime, hasImpedance, miimpedance):
        if unit == "lbs": calcweight = round(weight * 0.4536, 2)
        if unit == "jin": calcweight = round(weight * 0.5, 2)
        if unit == "kg": calcweight = weight
        if int(calcweight) > USER1_GT:
            user = USER1_NAME
            height = USER1_HEIGHT
            age = self.GetAge(USER1_DOB)
            sex = USER1_SEX
        elif int(calcweight) < USER2_LT:
            user = USER2_NAME
            height = USER2_HEIGHT
            age = self.GetAge(USER2_DOB)
            sex = USER2_SEX
        else:
            user = USER3_NAME
            height = USER3_HEIGHT
            age = self.GetAge(USER3_DOB)
            sex = USER3_SEX

        lib = Xiaomi_Scale_Body_Metrics.bodyMetrics(calcweight, height, age, sex, 0)
        message = '{'
        message += '"weight":"' + "{:.2f}".format(weight) + '"'
        message += ',"weight_unit":"' + str(unit) + '"'
        message += ',"bmi":"' + "{:.2f}".format(lib.getBMI()) + '"'
        message += ',"basal_metabolism":"' + "{:.2f}".format(lib.getBMR()) + '"'
        message += ',"visceral_fat":"' + "{:.2f}".format(lib.getVisceralFat()) + '"'

        if hasImpedance:
            lib = Xiaomi_Scale_Body_Metrics.bodyMetrics(calcweight, height, age, sex, int(miimpedance))
            bodyscale = ['Obese', 'Overweight', 'Thick-set', 'Lack-exerscise', 'Balanced', 'Balanced-muscular', 'Skinny', 'Balanced-skinny', 'Skinny-muscular']
            message += ',"lean_body_mass":"' + "{:.2f}".format(lib.getLBMCoefficient()) + '"'
            message += ',"body_fat":"' + "{:.2f}".format(lib.getFatPercentage()) + '"'
            message += ',"water":"' + "{:.2f}".format(lib.getWaterPercentage()) + '"'
            message += ',"bone_mass":"' + "{:.2f}".format(lib.getBoneMass()) + '"'
            message += ',"muscle_mass":"' + "{:.2f}".format(lib.getMuscleMass()) + '"'
            message += ',"protein":"' + "{:.2f}".format(lib.getProteinPercentage()) + '"'
            message += ',"body_type":"' + str(bodyscale[lib.getBodyType()]) + '"'
            message += ',"metabolic_age":"' + "{:.0f}".format(lib.getMetabolicAge()) + '"'

        message += ',"timestamp":"' + mitdatetime + '"'
        message += '}'
        try:
            sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Publishing data to topic {MQTT_PREFIX + '/' + user + '/weight'}: {message}\n")
            publish.single(
                MQTT_PREFIX + '/' + user + '/weight',
                message,
                # qos=1, #Removed qos=1 as incorrect connection details will result in the client waiting for ack from broker
                retain=True,
                hostname=MQTT_HOST,
                port=MQTT_PORT,
                auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD}
            )
            sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Data Published ...\n")
        except Exception as error:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Could not publish to MQTT: {error}\n")
            raise

def main():
    if MQTT_DISCOVERY.lower() in ['true', '1', 'y', 'yes']:
        discovery()
    BluetoothFailCounter = 0
    while True:
        try:
            scanner = btle.Scanner(HCI_DEV).withDelegate(ScanProcessor())
            scanner.scan(5) # Adding passive=True to try and fix issues on RPi devices
        except BTLEDisconnectError as error:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - btle disconnected: {error}\n")
            pass
        except BTLEManagementError as error:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Bluetooth connection error: {error}\n")
            if BluetoothFailCounter >= 4:
                sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 5+ Bluetooth connection errors. Resetting Bluetooth...\n")
                cmd = 'hciconfig hci' + HCI_DEV + ' down'
                ps = subprocess.Popen(cmd, shell=True)
                time.sleep(1)
                cmd = 'hciconfig hci' + HCI_DEV + ' up'
                ps = subprocess.Popen(cmd, shell=True)
                time.sleep(30)
                BluetoothFailCounter = 0
            else:
                BluetoothFailCounter+=1
            pass
        except Exception as error:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error while running the script: {error}\n")
            pass
        else:
            BluetoothFailCounter = 0
        time.sleep(TIME_INTERVAL)

if __name__ == "__main__":
    main()
