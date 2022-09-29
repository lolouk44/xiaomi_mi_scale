#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import binascii
from bleak import BleakScanner
from collections import namedtuple
from datetime import datetime
import functools
import json
import paho.mqtt.publish as publish
import subprocess
import sys

import Xiaomi_Scale_Body_Metrics


# First Log msg
sys.stdout.write(' \n')
sys.stdout.write('-------------------------------------\n')
sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting Xiaomi mi Scale...\n")


# User Config
class USER:
    def __init__(self, name, gt, lt, sex, height, dob):
        self.NAME, self.GT, self.LT, self.SEX, self.HEIGHT, self.DOB


def customUserDecoder(userDict):
    return namedtuple('USER', userDict.keys())(*userDict.values())

def MQTT_discovery():
    """Published MQTT Discovery information if enabled in options.json"""
    for MQTTUser in (USERS):
        message = '{"name": "' + MQTTUser.NAME + ' Weight",'
        message+= '"state_topic": "' + MQTT_PREFIX + '/' + MQTTUser.NAME + '/weight",'
        message+= '"value_template": "{{ value_json.weight }}",'
        message+= '"json_attributes_topic": "' + MQTT_PREFIX + '/' + MQTTUser.NAME + '/weight",'
        message+= '"icon": "mdi:scale-bathroom",'
        message+= '"state_class": "measurement"}'
        publish.single(
                        MQTT_DISCOVERY_PREFIX + '/sensor/' + MQTT_PREFIX + '/' + MQTTUser.NAME + '/config',
                        message,
                        retain=True,
                        hostname=MQTT_HOST,
                        port=MQTT_PORT,
                        auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD},
                        tls=MQTT_TLS
                    )
    sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - MQTT Discovery Setup Completed...\n")

def check_weight(user, weight):
    return weight > user.GT and weight < user.LT

def GetAge(d1):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(datetime.today().strftime('%Y-%m-%d'),'%Y-%m-%d')
    return abs((d2 - d1).days)/365
    
def MQTT_publish(weight, unit, mitdatetime, hasImpedance, miimpedance):
    """Publishes weight data for the selected user"""
    if unit == "lbs": calcweight = round(weight * 0.4536, 2)
    if unit == "jin": calcweight = round(weight * 0.5, 2)
    if unit == "kg": calcweight = weight
    matcheduser = None
    for user in USERS:
        if(check_weight(user,weight)):
            matcheduser = user
            break
    if matcheduser is None:
        return
    height = matcheduser.HEIGHT
    age = GetAge(matcheduser.DOB)
    sex = matcheduser.SEX.lower()
    name = matcheduser.NAME

    lib = Xiaomi_Scale_Body_Metrics.bodyMetrics(calcweight, height, age, sex, 0)
    message = '{'
    message += '"weight":' + "{:.2f}".format(weight)
    message += ',"weight_unit":"' + str(unit) + '"'
    message += ',"bmi":' + "{:.2f}".format(lib.getBMI())
    message += ',"basal_metabolism":' + "{:.2f}".format(lib.getBMR())
    message += ',"visceral_fat":' + "{:.2f}".format(lib.getVisceralFat())

    if hasImpedance:
        lib = Xiaomi_Scale_Body_Metrics.bodyMetrics(calcweight, height, age, sex, int(miimpedance))
        bodyscale = ['Obese', 'Overweight', 'Thick-set', 'Lack-exerscise', 'Balanced', 'Balanced-muscular', 'Skinny', 'Balanced-skinny', 'Skinny-muscular']
        message += ',"lean_body_mass":' + "{:.2f}".format(lib.getLBMCoefficient())
        message += ',"body_fat":' + "{:.2f}".format(lib.getFatPercentage())
        message += ',"water":' + "{:.2f}".format(lib.getWaterPercentage())
        message += ',"bone_mass":' + "{:.2f}".format(lib.getBoneMass())
        message += ',"muscle_mass":' + "{:.2f}".format(lib.getMuscleMass())
        message += ',"protein":' + "{:.2f}".format(lib.getProteinPercentage())
        message += ',"body_type":"' + str(bodyscale[lib.getBodyType()]) + '"'
        message += ',"metabolic_age":' + "{:.0f}".format(lib.getMetabolicAge())
        message += ',"impedance":' + "{:.0f}".format(int(miimpedance))

    message += ',"timestamp":"' + mitdatetime + '"'
    message += '}'
    try:
        sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Publishing data to topic {MQTT_PREFIX + '/' + name + '/weight'}: {message}\n")
        publish.single(
            MQTT_PREFIX + '/' + name + '/weight',
            message,
            retain=MQTT_RETAIN,
            hostname=MQTT_HOST,
            port=MQTT_PORT,
            auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD},
            tls=MQTT_TLS
        )
        sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Data Published ...\n\n")
    except Exception as error:
        sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Could not publish to MQTT: {error}\n")
        raise



# Configuraiton...
# Trying To Load Config From options.json (HA Add-On)
try:
    with open('/data/options.json') as json_file:
        sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Loading Config From Options.json...\n")
        data = json.load(json_file)["options"]
        try:
            MISCALE_MAC = data["MISCALE_MAC"]
        except:
            sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - MAC Address not provided...\n")
            raise
        try:
            MISCALE_VERSION = data["MISCALE_VERSION"]
            if(type(MISCALE_VERSION) != int):
                sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [Warning] Converting MISCALE_VERSION to integer...\n")
                MISCALE_VERSION = int(MISCALE_VERSION)
        except:
            MISCALE_VERSION = 2
            pass
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
            MQTT_RETAIN = data["MQTT_RETAIN"]
        except:
            MQTT_RETAIN = True
            pass
        try:
            MQTT_PORT = data["MQTT_PORT"]
            if(type(MQTT_PORT) != int):
                sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [Warning] Converting MQTT_PORT to integer...\n")
                MQTT_PORT = int(MQTT_PORT)
        except:
            MQTT_PORT = 1883
            pass
        try:
            MQTT_TLS_CACERTS = data["MQTT_TLS_CACERTS"]
        except:
            MQTT_TLS_CACERTS = None
            pass
        try:
            MQTT_TLS_INSECURE = data["MQTT_TLS_INSECURE"]
        except:
            MQTT_TLS_INSECURE = None
            pass
        try:
            MQTT_PREFIX = data["MQTT_PREFIX"]
        except:
            MQTT_PREFIX = "miscale"
            pass
        try:
            TIME_INTERVAL = data["TIME_INTERVAL"]
            if(type(TIME_INTERVAL) != int):
                sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [Warning] Converting TIME_INTERVAL to integer...\n")
                TIME_INTERVAL = int(TIME_INTERVAL)
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
            BLUEPY_PASSIVE_SCAN = data["BLUEPY_PASSIVE_SCAN"]
        except:
            BLUEPY_PASSIVE_SCAN = False
            pass

        if MQTT_TLS_CACERTS in [None, '', 'Path to CA Cert File']:
            MQTT_TLS = None
        else:
            MQTT_TLS = {'ca_certs':MQTT_TLS_CACERTS, 'insecure':MQTT_TLS_INSECURE}

        USERS = []
        for user in data["USERS"]:    
            try:
                user = json.dumps(user)
                user = json.loads(user, object_hook=customUserDecoder)
                if user.GT > user.LT:
                    raise ValueError("GT can not be larger than LT - user {user.Name}")  
                USERS.append(user)
            except:
                sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {sys.exc_info()[1]}\n")
                raise
        OLD_MEASURE = None
        sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Config Loaded...\n")

# Failed to open options.json
except FileNotFoundError as error:
    sys.stderr.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - options.json file missing... {error}\n")
    raise

async def main(MISCALE_MAC):
    stop_event = asyncio.Event()

    # TODO: add something that calls stop_event.set()

    def callback(device, advertising_data):
        global OLD_MEASURE
        if device.address.lower() == MISCALE_MAC:
            #print(f"miscale found, with advertising_data: {advertising_data}")
            try:
                device_name = advertising_data.local_name
            except:
                device_name = None
                pass
            data = binascii.b2a_hex(advertising_data.service_data['0000181b-0000-1000-8000-00805f9b34fb']).decode('ascii')
            if device_name == "MIBCS":
                ### Xiaomi V2 Scale ###
                    data = "1b18" + data # although not technically needed, keeping this 'ID' may be required in the future to identify V1 Vs V2 scales
                    data2 = bytes.fromhex(data[4:])
                    ctrlByte1 = data2[1]
                    isStabilized = ctrlByte1 & (1<<5)
                    hasImpedance = ctrlByte1 & (1<<1)
                    measunit = data[4:6]
                    measured = int((data[28:30] + data[26:28]), 16) * 0.01
                    unit = ''
                    if measunit == "03": unit = 'lbs'
                    if measunit == "02": unit = 'kg' ; measured = measured / 2
                    miimpedance = str(int((data[24:26] + data[22:24]), 16))
                    if unit and isStabilized:
                        if OLD_MEASURE != round(measured, 2) + int(miimpedance):
                            OLD_MEASURE = round(measured, 2) + int(miimpedance)
                            MQTT_publish(round(measured, 2), unit, str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')), hasImpedance, miimpedance)
            else:
            ### Xiaomi V1 Scale ###
                    data = "1d18" + data # although not technically needed, keeping this 'ID' may be required in the future to identify V1 Vs V2 scales
                    measunit = data[4:6]
                    measured = int((data[8:10] + data[6:8]), 16) * 0.01
                    unit = ''
                    if measunit.startswith(('03', 'a3')): unit = 'lbs'
                    if measunit.startswith(('12', 'b2')): unit = 'jin'
                    if measunit.startswith(('22', 'a2')): unit = 'kg' ; measured = measured / 2
                    if unit:
                        if OLD_MEASURE != round(measured, 2):
                            OLD_MEASURE = round(measured, 2)
                            MQTT_publish(round(measured, 2), unit, str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')), "", "")
        pass

    async with BleakScanner(callback) as scanner:
        ...
        # Important! Wait for an event to trigger stop, otherwise scanner
        # will stop immediately.
        await stop_event.wait()

        
if __name__ == "__main__":
    sys.stdout.write('-------------------------------------\n')
    sys.stdout.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Initialization Completed, Waiting for Scale...\n")
    try:
        asyncio.run(main(MISCALE_MAC.lower()))
    except:
        pass