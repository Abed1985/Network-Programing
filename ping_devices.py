# importing required libraries 
import csv
import sys
import subprocess
from multiprocessing.dummy import Pool as ThreadPool
import subprocess


# open the device list file using the CSV reader for operations.

file = csv.reader(open('devices_list.csv'),delimiter = ',')

# defining an empty device list for updating it from the csv doc.
dev_list= []

# looping over the device list csv to fill the empty created list
for line in file :
    dev = line[0]
    ip = line[1]
    dev = ['%s'%dev,'%s'%ip]
    dev_list.append(dev)

# opening a new csv file to write output of the ICMP , writting header only
with open('cpe-status.csv', 'a') as f:
    fieldnames = ['device', 'ip_address', 'status']
    writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
    writer.writeheader()
    
#defining the function ,opening the file , testing ICMP using a linux subprocess and writing the result in a row to file.

def get_prompt (dev):
    with open('cpe-status.csv', 'a') as f:
        fieldnames = ['device', 'ip_address', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
        ping_reply = subprocess.call(['ping', '-c', '3', '-w', '3', '-q', '-n', dev[1]], stdout =subprocess.PIPE)
        if ping_reply == 0:
            status = "%s is Reachable" %  dev[0]
            print (status)
            writer.writerow({'device': dev[0], 'ip_address': dev[1], 'status': status})
        else:
            status = "%s is not Reachable" %  dev[0]
            print (status)
            writer.writerow({'device': dev[0], 'ip_address': dev[1], 'status': status})




#threading pools process defined here , using a thread pool of 6 , can be edited to accomodate with your host capabilities

num_threads_str =  6
num_threads = int(num_threads_str)


threads = ThreadPool (num_threads)
results = threads.map ( get_prompt , dev_list )

threads.close()
threads.join()
