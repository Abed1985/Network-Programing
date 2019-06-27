#This program parses the mac address table from devices and map the mac to the vendor using a mac-ip lookup that uses an API
#and stores the output in a CSV file. 
#supported devices are cisco , dell , HP/aruba
# the script uses NTC ansible for regex matching and Netmiko , and need to be considered as prerequistes. 
# usage : python3 mac-vendor-switches.py "ip-address or username" "username"
#example: python3 mac-vendor-switches.py "10.0.0.1" "abood"
import sys
import getpass
from netmiko import Netmiko
import requests
import time
import datetime
import csv


host = sys.argv[1]
username = sys.argv[2]
password = getpass.getpass()

device_type = input ("Enter the device type as mentioned ( cisco_ios, hp_procurve,dell_os6, huawei ): ")

try:
    my_device = {"host": host,"username": username, "password": password, "device_type": device_type}
    net_connect = Netmiko(**my_device)
except ValueError:
    print("\nOnly mentioned device models are allowed!\n")



if device_type == "cisco_ios":
    output = net_connect.send_command("show mac address-table", use_textfsm=True)
    print("\nWriting output to file..this will take a while..please wait while output is printed and saved to File.\n")
    with open('%s' % my_device['device_type'] + '%s' % my_device['host'] + '_mac-vendor-audit.csv', 'w') as f:
        fieldnames = ['Mac-Address', 'Port Number', 'Vendor mapped', 'Comments']
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
        writer.writeheader()
        output_flat = {}
        for d in output:
            output_flat.update(d)
            mac = d["destination_address"]
            Port = output_flat['destination_port']
            r = requests.get(url="https://api.macvendors.com/%s" % mac)
            time.sleep(1)
            Vendor = r.text
            if "errors" not in Vendor:
                print ('Mac-Address: %s' %mac, 'Port: %s' %Port, 'Venodr mapped: %s' %Vendor)
                writer.writerow({'Mac-Address': mac, 'Port Number': Port, 'Vendor mapped': Vendor, 'Comments': ''})
        print("\nDone! Check your output file\n")

elif device_type == "hp_procurve":
    output = net_connect.send_command("show mac-address", use_textfsm=True)
    print("\nWriting output to file..this will take a while..please wait while output is printed and saved to File.\n")
    with open('%s' % my_device['device_type'] + '%s' % my_device['host'] + '_mac-vendor-audit.csv', 'w') as f:
        fieldnames = ['Mac-Address', 'Port Number', 'Vendor mapped', 'Comments']
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
        writer.writeheader()
        output_flat = {}
        for d in output:
            output_flat.update(d)
            mac = d['mac']
            Port = output_flat['port']
            r = requests.get(url="https://api.macvendors.com/%s" % mac)
            time.sleep(1)
            Vendor = r.text
            if "errors" not in Vendor:
                print ('Mac-Address: %s' %mac, 'Port: %s' %Port, 'Venodr mapped: %s' %Vendor)
                writer.writerow({'Mac-Address': mac, 'Port Number': Port, 'Vendor mapped': Vendor, 'Comments': ''})
        print("Done! Check your output file")

elif device_type == "dell_os6":
    output = net_connect.send_command("show mac address-table", use_textfsm=True)
    print("\nWriting output to file..this will take a while..please wait while output is printed and saved to File.\n")
    with open('%s' % my_device['device_type'] + '%s' % my_device['host'] + '_mac-vendor-audit.csv', 'w') as f:
        fieldnames = ['Mac-Address', 'Port Number', 'Vendor mapped', 'Comments']
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
        writer.writeheader()
        output_flat = {}
        for d in output:
            output_flat.update(d)
            mac = d['mac']
            Port = output_flat['port']
            r = requests.get(url="https://api.macvendors.com/%s" % mac)
            time.sleep(1)
            Vendor = r.text
            if "errors" not in Vendor:
                print ('Mac-Address: %s' %mac, 'Port: %s' %Port, 'Venodr mapped: %s' %Vendor)
                writer.writerow({'Mac-Address': mac, 'Port Number': Port, 'Vendor mapped': Vendor, 'Comments': ''})
        print("\nDone! Check your output file\n")

elif device_type == "huawei":
    output = net_connect.send_command("display mac-address", use_textfsm=True)
    print("\nWriting output to file..this will take a while..please wait while output is printed and saved to File.\n")
    with open('%s' % my_device['device_type'] + '%s' % my_device['host'] + '_mac-vendor-audit.csv', 'w') as f:
        fieldnames = ['Mac-Address', 'Port Number', 'Vendor mapped', 'Comments']
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
        writer.writeheader()
        output_flat = {}
        for d in output:
            output_flat.update(d)
            mac = d['macaddress']
            r = requests.get(url="https://api.macvendors.com/%s" % mac)
            Vendor = r.text
            time.sleep(1)
            if "errors" not in Vendor:
                print ('Mac-Address: %s' %mac, 'Venodr mapped: %s' %Vendor)
                writer.writerow({'Mac-Address': mac, 'Vendor mapped': Vendor, 'Comments': ''})
        print("\nDone! Check your output file\n")
