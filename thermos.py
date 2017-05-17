#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import glob
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

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
    with ThreadPoolExecutor(max_workers = len(thermostats)) as executor:
        futures = []
        for therm in thermostats:
            futures.append(executor.submit(get_therm, therm))

        for future in futures:
            print(future.result())
            
    sys.stdout.flush()

def get_therm(therm):
    statname = os.path.basename(therm)
    temp_c = read_w1_slave(therm + '/w1_slave')
    return "{0}\t{1}".format(statname, temp_c)
    
def main():
    thermostats = glob.glob('/sys/bus/w1/devices/28-*')
    while True:
        print_therms(thermostats)
        time.sleep(2)

print('Start!')
main()
