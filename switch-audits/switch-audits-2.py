# importing the required libraries
# The purpose of this code is to create a list of ports that constitute 
# a potenial port of a connected switch or an access point. 
# Basically Any port with 3 or more learned MAC addresses on

import yaml
import os
import csv
import subprocess
import warnings
from multiprocessing.dummy import Pool as ThreadPool
from netmiko import Netmiko
from datetime import datetime,timedelta
import subprocess
startTime = datetime.now()
warnings.filterwarnings("ignore")
import create_devicedb
from collections import Counter

# opening the rendered device database
# create a device list by looping over the loaded yaml
filename = "device_rendered_list.yml"

with open (filename) as f:
    output1 = yaml.load(f)

dev_list = []

for key,value in output1.items():
    dev = value
    name = key
    dev_list.append(dev)

# opening a new csv file 
file_exists = os.path.isfile('Potential_switch_ports.csv')

# creating a function to login to devices depending on device type using netmiko and issue 
# the show mac address table command, using NTC to format data
def get_prompt (dev):
    H = [key for (key,value) in output1.items() if value['host'] == dev['host']][0]
    print ("Fetching information from %s..." %H )
    net_conn = Netmiko(**dev)
    if dev['device_type'] == 'cisco_ios':
       output = net_conn.send_command("show mac address-table", use_textfsm=True)
       # counting the number of ports in the mac address table
       C2 = Counter(x['destination_port'] for x in output)
       C3 = dict(C2)
       # returning key values for >3 ports
       C3_switch = [key  for (key, value) in C3.items() if value >= 3]
       print ("Writing information  from %s  to file.." %H)
       # writing the output to a csv file
       with open('Potential_switch_ports.csv', 'a') as f:
               fieldnames = ['Device Name', 'Port Number']
               writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
               writer.writeheader()
               for i in range(len(C3_switch)):
                   writer.writerow({'Device Name': H, 'Port Number': C3_switch[i]})

    elif dev['device_type'] == 'hp_procurve':
         output = net_conn.send_command("show mac-address", use_textfsm=True)
         C2 = Counter(x['port'] for x in output)
         C3 = dict(C2)
         C3_switch = [key  for (key, value) in C3.items() if value >= 3]
         print ("Writing information  from %s  to file.." %H)
         with open('Potential_switch_ports.csv', 'a') as f:
                 fieldnames = ['Device Name', 'Port Number']
                 writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
                 writer.writeheader()
                 for i in range(len(C3_switch)):
                     writer.writerow({'Device Name': H, 'Port Number': C3_switch[i]})

    elif dev['device_type'] == 'dell_os6':
         output = net_conn.send_command("show mac address-table", use_textfsm=True)
         C2 = Counter(x['port'] for x in output)
         C3 = dict(C2)
         C3_switch = [key  for (key, value) in C3.items() if value >= 3]
         print ("Writing information  from %s  to file.." %H)
         with open('Potential_switch_ports.csv', 'a') as f:
                 fieldnames = ['Device Name', 'Port Number']
                 writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
                 writer.writeheader()
                 for i in range(len(C3_switch)):
                     writer.writerow({'Device Name': H, 'Port Number': C3_switch[i]})

# deleting the device list after this code finishes execution . 

Path = os.getcwd()
filelist = os.listdir(Path)
for v in filelist:
    if v == "device_rendered_list.yml":
       subprocess.call(["rm", Path + "/" + os.path.basename(v)])



#this part where threading pools is used , using a threading pool of 4. 
#This can be changed according to your host capabilities.

num_threads_str =  4
num_threads = int(num_threads_str)


threads = ThreadPool (num_threads)
results = threads.map ( get_prompt , dev_list )

threads.close()
threads.join()

endTime = datetime.now()
elapsedTime = endTime - startTime
print(elapsedTime)

