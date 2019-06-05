#############################################################################################
# Code to read weight measurements fom Xiaomi Scale V2
# (Framework is prsent to also read from Xiaomi Scale V1, though I do not own one to test so code has not been maintained)
# Must be executed with Python 3 else body measurements are incorrect.
# Must be executed as root, therefore best to schedule via crontab every 5 min (so as not to drain the battery):
# */5 * * * * python3 /path-to-script/Xiaomi_Scale.py
# Multi user possible as long as weitghs do not overlap, see lines 117-131
#
# Thanks to @syssi (https://gist.github.com/syssi/4108a54877406dc231d95514e538bde9) and @prototux (https://github.com/wiecosystem/Bluetooth) for their initial code
#
# Make sure you edit MQTT credentials below and user logic/data on lines 117-131
#
#############################################################################################



#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import binascii
import time
import os
import sys
from bluepy import btle
import paho.mqtt.client as mqtt
from datetime import datetime

import Xiaomi_Scale_Body_Metrics

MISCALE_MAC = 'REDACTED'
MQTT_USERNAME = 'REDACTED'
MQTT_PASSWORD = 'REDACTED'
MQTT_HOST = 'REDACTED'
MQTT_PORT = 1883
MQTT_TIMEOUT = 60


class ScanProcessor():

	def GetAge(self, d1):
		d1 = datetime.strptime(d1, "%Y-%m-%d")
		d2 = datetime.strptime(datetime.today().strftime('%Y-%m-%d'),'%Y-%m-%d')
		return abs((d2 - d1).days)/365

	def __init__(self):
		self.mqtt_client = None
		self.connected = False
		self._start_client()

	def handleDiscovery(self, dev, isNewDev, isNewData):
		if dev.addr == MISCALE_MAC.lower() and isNewDev:
			# print ('	Device: %s (%s), %d dBm %s. ' %
				   # (
					   # ANSI_WHITE + dev.addr + ANSI_OFF,
					   # dev.addrType,
					   # dev.rssi,
					   # ('' if dev.connectable else '(not connectable)'))
				   # , end='')
			for (sdid, desc, data) in dev.getScanData():
				### Xiaomi V1 Scale ###
				if data.startswith('1d18') and sdid == 22:
					measunit = data[4:6]
					measured = int((data[8:10] + data[6:8]), 16) * 0.01
					unit = ''

					if measunit.startswith(('03', 'b3')): unit = 'lbs'
					if measunit.startswith(('12', 'b2')): unit = 'jin'
					if measunit.startswith(('22', 'a2')): unit = 'kg' ; measured = measured / 2

					if unit:
						print('')
						self._publish(round(measured, 2), unit, "", "")
					else:
						print("Scale is sleeping.")

				### Xiaomi V2 Scale ###
				if data.startswith('1b18') and sdid == 22:
					measunit = data[4:6]
					measured = int((data[28:30] + data[26:28]), 16) * 0.01
					unit = ''

					if measunit == "03": unit = 'lbs'
					if measunit == "02": unit = 'kg' ; measured = measured / 2
					mitdatetime = datetime.strptime(str(int((data[10:12] + data[8:10]), 16)) + " " + str(int((data[12:14]), 16)) +" "+ str(int((data[14:16]), 16)) +" "+ str(int((data[16:18]), 16)) +" "+ str(int((data[18:20]), 16)) +" "+ str(int((data[20:22]), 16)), "%Y %m %d %H %M %S")
					miimpedance = str(int((data[24:26] + data[22:24]), 16))



					if unit:
						print('')
						self._publish(round(measured, 2), unit, str(mitdatetime), miimpedance)
					else:
						print("Scale is sleeping.")


			if not dev.scanData:
				print ('\t(no data)')
			print

	def _start_client(self):
		self.mqtt_client = mqtt.Client()
		self.mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

		def _on_connect(client, _, flags, return_code):
			self.connected = True
			#print("MQTT connection returned result: %s" % mqtt.connack_string(return_code))

		self.mqtt_client.on_connect = _on_connect

		self.mqtt_client.connect(MQTT_HOST, MQTT_PORT, MQTT_TIMEOUT)
		self.mqtt_client.loop_start()

	def _publish(self, weight, unit, mitdatetime, miimpedance):
		if not self.connected:
			raise Exception('not connected to MQTT server')
		if int(weight) > 72:
			user="lolo"
			height=175
			age=self.GetAge("1900-01-01")
			sex="male"
		elif int(weight) < 50:
			user="kiaan"
			height=103
			age=self.GetAge("1900-01-01")
			sex="male"
		else:
			user = "div"
			height=170
			age=self.GetAge("1900-01-01")
			sex="female"
		lib = Xiaomi_Scale_Body_Metrics.bodyMetrics(weight, height, age, sex, 0)
		message = '{'
		message += '"Weight":"' + "{:.2f}".format(weight) + '"'
		message += ',"BMI":"' + "{:.2f}".format(lib.getBMI()) + '"'
		message += ',"Basal Metabolism":"' + "{:.2f}".format(lib.getBMR()) + '"'
		message += ',"Visceral Fat":"' + "{:.2f}".format(lib.getVisceralFat()) + '"'

		if miimpedance:
			lib = Xiaomi_Scale_Body_Metrics.bodyMetrics(weight, height, age, sex, int(miimpedance))
			message += ',"Lean Body Mass":"' + "{:.2f}".format(lib.getLBMCoefficient()) + '"'
			message += ',"Body Fat":"' + "{:.2f}".format(lib.getFatPercentage()) + '"'
			message += ',"Water":"' + "{:.2f}".format(lib.getWaterPercentage()) + '"'
			message += ',"Bone Mass":"' + "{:.2f}".format(lib.getBoneMass()) + '"'
			message += ',"Muscle Mass":"' + "{:.2f}".format(lib.getMuscleMass()) + '"'
			message += ',"Protein":"' + "{:.2f}".format(lib.getProteinPercentage()) + '"'
			self.mqtt_client.publish(user, weight, qos=1, retain=True)

		message += ',"TimeStamp":"' + mitdatetime + '"'
		message += '}'
		self.mqtt_client.publish(user+'/weight', message, qos=1, retain=True)
		print('\tSent data to topic %s: %s' % (user+'/weight', message))

def main():

	# while(True):
	scanner = btle.Scanner().withDelegate(ScanProcessor())

	devices = scanner.scan(5)

if __name__ == "__main__":
	main()
