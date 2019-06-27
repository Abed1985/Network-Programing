#The Following code retreives log files  from syslog servers and search accross moved files for ease of getting back to historical logs for troubleshooting.
#The purpose of this code is to ease the searching process in the log files. Basically all customers network devices logs are stored in one single file that is archived over night.
#Since  it will take a quiet sometime to transfer the files via ssh to personal host machine , and then dearchive, then  search required device ip or host name.
# then look for the log of interest. The code will transfer up to 7 days of logs and take care of the search required, and save the desired output in a file.
# usage is python3 log-parse-bne.py "username" , which is the same username used to login to the server via scp/sftp
from datetime import datetime,timedelta
import pysftp
import gzip
import os
import re
import warnings
import glob
import sys
import getpass
import subprocess
warnings.filterwarnings("ignore")
startTime = datetime.now()
L2=[]
L3=[]
#recording time for illustration purposes of the total required time. 
now = datetime.today()
#passing the username  of the syslog server  shell connection

username = sys.argv[1]
password = getpass.getpass()
while True:
    log_R = input("Enter log retention value in days ( 1 ,3, or 7): ")
    print("Retrieving log files..")
    if log_R == "1":
        date = now.strftime("%Y%m%d")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        Path = os.getcwd()
        with pysftp.Connection('bne-syslog-03' ,
                            username = username,
                            password = password,
                            cnopts = cnopts) as sftp:
            sftp.isfile('/data/log/network/client/client_cpe.log')
            today = sftp.get('/data/log/network/client/client_cpe.log','%s/client_cpe.log' % Path)
        sftp.close()
        Str = input("Enter the 1st search string (customer hostname or IP): ")
        Str2 = input("Enter the 2nd search string (customer Issue..eg: DHCP,POE): ")
        filelist = os.listdir(Path)
        for n in filelist:
            if n.startswith("client"):
                with open(Path + "/" + n, "r") as k:
                    for line in k.readlines():
                        if re.search(Str, line, flags=re.IGNORECASE) and re.search(Str2, line, flags=re.IGNORECASE):
                            print(line)
                            L3.append(line)
        with open(Str + "--" + Str2 + "--" + "logs", 'a') as B:
            B.writelines(L3)
        break
    elif log_R == "3":
        date = now.strftime("%Y%m%d")
        yest = now - timedelta(days=1)
        byest= now - timedelta(days=2)
        date_yest = yest.strftime("%Y%m%d")
        date_byest = byest.strftime("%Y%m%d")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        Path = os.getcwd()
        with pysftp.Connection('bne-syslog-03' ,
                            username = username,
                            password = password,
                            cnopts = cnopts) as sftp:
            sftp.isfile('/data/log/network/client/client_cpe.log')
            today = sftp.get('/data/log/network/client/client_cpe.log','%s/client_cpe.log' % Path)
            yest_file = sftp.get('/data/log/network/client/client_cpe.log-%s.gz'%date_yest,'%s/client_cpe.log-%s.gz' % (Path, date_yest))
            byest_file = sftp.get('/data/log/network/client/client_cpe.log-%s.gz'%date_byest, '%s/client_cpe.log-%s.gz' % (Path, date_byest))
        sftp.close()
        Str = input("Enter the 1st search string (customer hostname or IP): ")
        Str2 = input("Enter the 2nd search string (customer Issue..eg: DHCP,POE): ")
        for file in glob.glob(Path + "/*.gz"):
            if os.path.isdir(file) == False:
                # uncompress the file
                subprocess.call(["gunzip", Path + "/" + os.path.basename(file)])

        Path = os.getcwd()
        filelist_2 = os.listdir(Path)
        for n in filelist_2:
            if n.startswith("client"):
                with open(Path + "/" + n, "r") as k:
                    for line in k.readlines():
                        if re.search(Str, line, flags=re.IGNORECASE) and re.search(Str2, line, flags=re.IGNORECASE):
                            print(line)
                            L3.append(line)
        with open(Str + "--" + Str2 + "--" + "logs", 'a') as B:
            B.writelines(L3)

        filelist_3 = os.listdir(Path)
        for v in filelist_3:
            if v.startswith("client"):
                subprocess.call(["rm", Path + "/" + os.path.basename(v)])
        break
    elif log_R == "7":
        date = now.strftime("%Y%m%d")
        day1 = now - timedelta(days=1)
        day2 = now - timedelta(days=2)
        day3 = now - timedelta(days=3)
        day4 = now - timedelta(days=4)
        day5 = now - timedelta(days=5)
        day6 = now - timedelta(days=6)
        day1_f = day1.strftime("%Y%m%d")
        day2_f = day2.strftime("%Y%m%d")
        day3_f = day3.strftime("%Y%m%d")
        day4_f = day4.strftime("%Y%m%d")
        day5_f = day5.strftime("%Y%m%d")
        day6_f = day6.strftime("%Y%m%d")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        Path = os.getcwd()
        with pysftp.Connection('bne-syslog-03' ,
                            username = username,
                            password = password,
                            cnopts = cnopts) as sftp:
            sftp.isfile('/data/log/network/client/client_cpe.log')
            today = sftp.get('/data/log/network/client/client_cpe.log','%s/client_cpe.log' % Path)
            day1_file = sftp.get('/data/log/network/client/client_cpe.log-%s.gz'%day1_f, '%s/client_cpe.log-%s.gz' % (Path,day1_f))
            day2_file = sftp.get('/data/log/network/client/client_cpe.log-%s.gz'%day2_f, '%s/client_cpe.log-%s.gz' % (Path,day2_f))
            day3_file = sftp.get('/data/log/network/client/client_cpe.log-%s.gz'%day3_f, '%s/client_cpe.log-%s.gz' % (Path,day3_f))
            day4_file = sftp.get('/data/log/network/client/client_cpe.log-%s.gz'%day4_f, '%s/client_cpe.log-%s.gz' % (Path,day4_f))
            day5_file = sftp.get('/data/log/network/client/client_cpe.log-%s.gz'%day5_f, '%s/client_cpe.log-%s.gz' % (Path,day5_f))
            day6_file = sftp.get('/data/log/network/client/client_cpe.log-%s.gz'%day6_f, '%s/client_cpe.log-%s.gz' % (Path,day6_f))
        sftp.close()
        Str = input("Enter the 1st search string (customer hostname or IP): ")
        Str2 = input("Enter the 2nd search string (customer Issue..eg: DHCP,POE): ")
        for file in glob.glob(Path + "/*.gz"):
            if os.path.isdir(file) == False:
                # uncompress the file
                subprocess.call(["gunzip", Path + "/" + os.path.basename(file)])

        filelist_2 = os.listdir(Path)
        for n in filelist_2:
            if n.startswith("client"):
                with open(Path + "/" + n, "r") as k:
                    for line in k.readlines():
                        if re.search(Str, line, flags=re.IGNORECASE) and re.search(Str2, line, flags=re.IGNORECASE):
                            print(line)
                            L3.append(line)
        with open(Str + "--" + Str2 + "--" + "logs", 'a') as B:
            B.writelines(L3)

        filelist_3 = os.listdir(Path)
        for v in filelist_3:
            if v.startswith("client"):
                subprocess.call(["rm", Path + "/" + os.path.basename(v)])
        break
    else:
        print("Only 1 , 3 , 7 days log retention allowed")
        continue

endTime = datetime.now()
elapsedTime = endTime - startTime
print(elapsedTime)
