import yaml

import warnings
from multiprocessing.dummy import Pool as ThreadPool
from netmiko import Netmiko
from datetime import datetime,timedelta
import subprocess
startTime = datetime.now()
warnings.filterwarnings("ignore")

#importing the database files that will be used for the ssh sessions

filename = "dev_list.yml"
#loading the yml file that contains device details and storing it in a dictionary
with open (filename) as f:
    output = yaml.load(f)

#defining an empty list to be used for threading pools
dev_list = []

#looping over the dictionary to fetch key value pairs , and filling the data in the dev_list 
for key,value in output.items():
    dev = value
    dev_list.append(dev)
    

# defining a fuction to ping the device host , execute the commands from files accordingly with netmiko. The purpose of the function is for the thread process to enter its operation
def get_prompt (dev):
    ping_reply = subprocess.call(['ping', '-c', '3', '-w', '3', '-q', '-n', dev['host']], stdout =subprocess.PIPE)
    if ping_reply == 0:
        net_conn = Netmiko(**dev)
        print ("device %s is reachable"% dev['host'])
        # the commnad file used associated wit the ip address
        cfg_file = "%s.txt"%dev['host']
        output = net_conn.send_config_from_file(cfg_file)
        print (output)
        net_conn.save_config()
        net_conn.disconnect()
        # its always a good idea to write output to file to make sure that your commands have been executed successfully to the device
        print("\nWriting output to file for %s ..please wait while output is printed and saved to File.\n"% dev['host'])
        with open('cfg-%s.txt'%dev['host'], 'a') as f:
            f.writelines(output)
    else:
        status = "%s is not reachable..skipping"% dev['host']
        print (status)
        pass
#threading part , using a thread pool of 4 . Means 4 devices at a time. value depends on available ram on the client for sure.
num_threads_str =  4
num_threads = int(num_threads_str)

# defining the number of threads
threads = ThreadPool (num_threads)
# defining the thread process , basically the function and the associated list
results = threads.map ( get_prompt , dev_list )
#closing and joining threads accordingly 
threads.close()
threads.join()
# nice to record your script execution time. 
endTime = datetime.now()
elapsedTime = endTime - startTime
print(elapsedTime)

