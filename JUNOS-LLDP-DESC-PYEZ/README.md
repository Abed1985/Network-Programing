ode utilizes Juniper PyeZ to pring the output of interface description and LLDP output information
# in an excel workbook , sheet per host 
# usage : python3 junos-desc-lldp.py "root" , where "root" is the username to connect to devices ssh/netconf and will prompt 
# the user for a password
# the code will produce an excel sheet LLDP_and_Desc.xlsx with the required information / sample attached.
# sample output 
python3 junos-desc-lldp.py "root"
Creating the temporary host file.. 
Password: 
Fething information from 192.168.2.15 and storing into Excelsheet
Fething information from 192.168.2.11 and storing into Excelsheet
Fething information from 192.168.2.12 and storing into Excelsheet
Fething information from 192.168.2.14 and storing into Excelsheet
Fething information from 192.168.2.16 and storing into Excelsheet
Fething information from 192.168.2.17 and storing into Excelsheet
Fething information from 192.168.2.18 and storing into Excelsheet
0:00:14.565734
