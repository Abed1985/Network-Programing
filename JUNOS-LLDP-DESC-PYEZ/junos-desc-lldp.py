from jnpr.junos import Device
from multiprocessing.dummy import Pool as ThreadPool
from netmiko import Netmiko
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
import warnings
from lxml import etree
import xmltodict
import pprint
import json
import getpass
import xlsxwriter
from ncclldp2 import lldp, intdesc
import sys
import jinja2
import yaml
import os
import csv
import subprocess
from datetime import datetime,timedelta
startTime = datetime.now()
warnings.filterwarnings("ignore")
now = datetime.today()
#capturing rechability and auth failures hosts
Reach_Issue=open("non-reachables.txt", "a")
Auth_Issue=open("ssh-failures.txt", "a")

# importing the database files that will be used for the ssh sessions with rendering the yml file.
cancel = False
device_list= []

print ( "Creating the temporary host file.. ")
with open ('dev_list.yml' , 'w') as f:
        f.writelines("---\n\n")

file = csv.reader(open('device_list.csv'),delimiter = ',')
next(file)
username = sys.argv[1]
password = getpass.getpass()
for line in file :
        dev_name = line[0]
        ip = line[0]
        template_file = 'dev_template2.j2'
        dev_list_dict = {"dev_name": dev_name,"ip":ip, "username":username,"password":password}
        with open (template_file) as f:
            dev_temp = f.read()
        template = jinja2.Template(dev_temp)
        M = template.render(dev_list_dict)
        with open ('dev_list.yml' , 'a') as f:
            f.writelines(M)


filename = "dev_list.yml"
# loading the yml file that contains device details and storing it in a dictionary
with open(filename) as f:
    output = yaml.load(f)

# defining an empty list to be used for threading pools
dev_list = []

workbook = xlsxwriter.Workbook('LLDP_and_Desc.xlsx')
# looping over the dictionary to fetch key value pairs , and filling the data in the dev_list
for key, value in output.items():
    dev = value
    worksheet = workbook.add_worksheet('%s' % dev['host'])
    dev_list.append(dev)

workbook = xlsxwriter.Workbook('LLDP_and_Desc.xlsx')



# defining a fuction to ping the device host , execute the commands from files accordingly with netmiko. The purpose of the function is for the thread process to enter its operation
def get_prompt(dev):
    ping_reply = subprocess.call(['ping', '-c', '3', '-w', '3', '-q', '-n', dev['host']], stdout=subprocess.PIPE)
    if ping_reply == 0:
        try:
            print ( "Fething information from %s and storing into Excelsheet"%dev['host'])
            lldp_store = lldp("%s" % dev['host'], "%s" % dev['username'], "%s" % dev['password'])
            int_desc = intdesc("%s" % dev['host'], "%s" % dev['username'], "%s" % dev['password'])
            worksheet = workbook.add_worksheet('%s' % dev['host'])
            worksheet = workbook.get_worksheet_by_name('%s' % dev['host'])
            row = 0
            col = 0
            worksheet.write('A1', 'local port(LLDP)')
            worksheet.write('B1', 'remote device')
            worksheet.write('C1', 'local port(DESC)')
            worksheet.write('D1', 'port description')
            row = 1
            col = 0
            for key, value in lldp_store.items():
                for key, value in value.items():
                    for my_dict in value:
                        if type(my_dict) == dict:
                            port = my_dict['lldp-local-port-id']
                            remote = my_dict['lldp-remote-system-name']
                            worksheet.write(row, col, port)
                            worksheet.write(row, col + 1, remote)
                            row += 1
            row = 1
            col = 0
            for key, value in int_desc.items():
                for key, value in value.items():
                    if type(value) == list:
                        local_port = ([d["name"] for d in value])
                        desc = ([r["description"] for r in value])
                        for i in range(len(value)):
                            worksheet.write(row, col + 2, local_port[i])
                            worksheet.write(row, col + 3, desc[i])
                            row += 1
        except (SSHException, AuthenticationException):
            print ("device %s credentials issues..exporting to ssh-failures.txt" % dev['host'])
            Auth_Issue.write('%s\n' % dev['host'])
    else:
        status = "%s is not reachable..skipping..exporting to non-reachables.txt" % dev['host']
        print (status)
        Reach_Issue.write('%s\n' % dev['host'])
        pass


# threading part , using a thread pool of 4 . Means 4 devices at a time. value depends on available ram on the client for sure.
num_threads_str = 4
num_threads = int(num_threads_str)

# defining the number of threads
threads = ThreadPool(num_threads)
# defining the thread process , basically the function and the associated list
#results2 = threads.map(create_sheets, dev_list)
results = threads.map(get_prompt, dev_list)
# closing and joining threads accordingly
threads.close()
threads.join()
# nice to record your script execution time.
endTime = datetime.now()
elapsedTime = endTime - startTime
print(elapsedTime)
# worksheet.write(row, 0, 'port')
# worksheet.write(row, 1 , 'remote device')
workbook.close()

#deleting the host name file after the code finishes
Path = os.getcwd()
hostfile = os.listdir(Path)
for v in hostfile:
    if v.startswith("dev_list.yml"):
        subprocess.call(["rm", Path + "/" + os.path.basename(v)])

