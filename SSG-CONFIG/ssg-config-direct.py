# importing needed libraries 
import csv
import paramiko
import re
import subprocess

#reading the device file that contains the device ips and credentials
file = csv.reader(open('device_list.csv'),delimiter = ',')
#skipping the headerline 
next(file)
#looping over the csv values and storing each in a variable to be called by the rest of the script
for line in file :
    dev_name = line[0]
    ip = line[1]
    username = line[2]
    password = line[3]

    # Logging into device using the paramiko library with a try ,except block
    try:
        #defining a variable for the paramiko ssh client
        session = paramiko.SSHClient()
        #this allows auto-accepting unknown host keys
        #do not use in production! the default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #print a screen message of attempting to connect to a device
        print ("Connection to  .. %s ..IP address ..%s and executing commands" %(dev_name,ip))
        # testing icmp reachability for the device first before any attempt to complete the script and pass that device if icmp fails. For this purpose we used a linux subprocess.
        ping_reply = subprocess.call(['ping', '-c', '3', '-w', '3', '-q', '-n', ip], stdout =subprocess.PIPE)
        #A successfull icmp will return a value of "0"
        if ping_reply == 0:
            #print a screen message saying that this ip is reachable 
            status = "%s is Reachable" %ip
            print (status)
            #connect to the device using the username,password mentioned in the csv per device.
       	    session.connect(ip, username=username, password=password)
            #starts an interactive shell session on the router
            connection = session.invoke_shell()
            #send an enter to start the session on a clear ssh screen and inserting a safe time delay before sending commands down the shell
            connection.send("\n")
            time.sleep(2)
            connection.send('set route 192.168.40.0/24 interface tunnel.1\n')
            time.sleep(2)
            connection.send('set route 192.168.50.0/24 interface tunnel.1\n')
            time.sleep(2)
            connection.send('set snmp community "public" Read-Only version v2c\n')
            time.sleep(2)
            connection.send('set snmp host "public" 192.168.40.0 255.255.255.0 src-interface l0.1\n')
            time.sleep(2)
            connection.send('set snmp host "public" 192.168.50.0 255.255.255.0 src-interface l0.1\n')
            time.sleep(2)
            connection.send('set snmp port listen 161\n')
            time.sleep(2)
            connection.send('exit\n')
            time.sleep(2)
            connection.send('y\n')
            time.sleep(2)
            # 65535 byes maximum receive of the data and store it in a variable
            output = connection.recv(65535)
            #opening a text file with name as the ip address to write the output. The purpose of this file is to inspect later how the commands been executed on the CLI
            with open('%s.txt' % ip,'wb') as f:
                f.write(output)
            # also reading command output on the screen
            print (output)

            # Closing the connection
            session.close()
        else:
            #basically if the ip is not reachable, the loop will pass to the next one before any of the above commands follow
            status = "%s is not Reachable"%ip
            print (status)
            pass
        #catching an authentication error incase the csv has wrong credentials , but if any device had this issue the script will jump to the except block, this can be enhanced to capture per device.
    except paramiko.AuthenticationException:
        print ("* Invalid username or password. \n* Please check the username/password file or the device configuration!")
        print ("* Closing program...\n")
