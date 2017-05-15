#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import datetime
import glob

def read_w1_slave(slave):
    with open(slave, 'r') as f:
        lines = f.readlines()
        if lines[0].strip()[-3:] == 'YES':
            temp_output = lines[1].find('t=')
            if temp_output != -1:
                temp_string = lines[1].strip()[temp_output+2:]
                temp_c = float(temp_string)/1000.0
                return temp_c
    return 'CRC-ERROR'


def print_therms(thermostats):
    print(datetime.datetime.now())
    for therm in thermostats:
        statname = os.path.basename(therm)
        temp_c = read_w1_slave(therm + '/w1_slave')
        print("{0}\t{1}".format(statname, temp_c))


def main():
    thermostats = glob.glob('/sys/bus/w1/devices/28-*')
    while True:
        print_therms(thermostats)
        time.sleep(2)

main()
