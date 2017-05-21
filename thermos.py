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
    now = datetime.datetime.now()
    with ThreadPoolExecutor(max_workers = len(thermostats)) as executor:
        futures = [executor.submit(get_therm, t) for t in thermostats]
        therms = [f.result() for f in futures]
        therms.insert(0, str(now))
        print("\t".join(therms))
    sys.stdout.flush()

def get_therm(therm):
    temp_c = read_w1_slave(therm + '/w1_slave')
    return str(temp_c)
    
def main():
    thermostats = glob.glob('/sys/bus/w1/devices/28-*')
    statnames = [os.path.basename(t) for t in thermostats]
    header = "time\t" + "\t".join(statnames)
    print(header)
    while True:
        print_therms(thermostats)
        time.sleep(2)

main()
