import csv
import subprocess
import easysnmp

#Importing the csv file that contains the device names and IP addresses. ex. device_list.csv
file = csv.reader(open('SSG-2-MOD.csv'),delimiter = ',')
#below commands used to skip first row of the csv which is the heading
next(file)
#looping over the device file
for line in file :
    dev_name = line[1]
    ip = line[2]
    print ("Testing Reachability  .. %s ..IP address ..%s" %(dev_name,ip))
    #calling a subprocess to ping ip addresses , if devices are reachable to to try snmp function
    ping_reply = subprocess.call(['ping', '-c', '3', '-w', '3', '-q', '-n', ip], stdout =subprocess.PIPE)
    if ping_reply == 0:
       status = "%s is Reachable" %ip
       print (status)
       #following command in easysnmp uses the ip from the csv , along with a community string , with version 2 . This part is editable to suit the needs of community string, snmp version.
       session = easysnmp.Session(hostname = '%s'%ip,community= 'NmSm0n1tor',version=2)
       try:
          #trying to get the sysdescription oid  
          description = session.get('.1.3.6.1.2.1.1.1.0')
          #convert the value for a string and look for "SNMP Variable" in the output as it indicates a sucessful walk 
          description_mod = str(description)
          if "SNMPVariable" in description_mod:
             State = "SNMP Ok"
             print(State)
          else:
              State = "SNMP Error"
              print(State)
       #catching out basic snmp errors to indicate an SNMP or community problem          
       except easysnmp.EasySNMPTimeoutError:
           State = "SNMP or Community Problem"
           print(State)
    else:
        status = "%s is not Reachable"%ip
        print (status)
        pass
