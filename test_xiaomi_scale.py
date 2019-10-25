#!/usr/bin/python3
from __future__ import print_function
import argparse
import binascii
import os
import sys
from bluepy import btle

MISCALE_MAC = 'XX:XX:XX:XX:XX:XX'

if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'


class ScanProcessor():

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr == MISCALE_MAC.lower() and isNewDev:
            print ('    Device: %s (%s), %d dBm %s. ' %
                   (
                       ANSI_WHITE + dev.addr + ANSI_OFF,
                       dev.addrType,
                       dev.rssi,
                       ('' if dev.connectable else '(not connectable)'))
                   , end='')
            for (sdid, desc, data) in dev.getScanData():
                print('')
                print ('data:')
                print (data)
                if data.startswith('1b18') and sdid == 22:
                    measunit = data[4:6]
                    measured = int((data[28:30] + data[26:28]), 16) * 0.01
                    unit = ''

                    if measunit == "03": unit = 'lbs'
                    if measunit == "02": unit = 'kg' ; measured = measured / 2
                    if unit:
                        print('measured:')
                        print (measured)
                        print('unit:')
                        print (unit)
                        print('')

                    else:
                        print("Scale is sleeping.")

            if not dev.scanData:
                print ('\t(no data)')
            print




def main():

    scanner = btle.Scanner().withDelegate(ScanProcessor())

    print (ANSI_RED + "Scanning for devices..." + ANSI_OFF)
    devices = scanner.scan(5)

if __name__ == "__main__":
    main()