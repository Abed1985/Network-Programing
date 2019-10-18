#from __future__ import print_function , unicode_literal
import jinja2
import time
import csv

cancel = False
device_list= []


with open ('dev_list.yml' , 'w') as f:
        f.writelines("---\n\n")


file = csv.reader(open('device_list.csv'),delimiter = ',')
next(file)
for line in file :
        dev_name = line[0]
        ip = line[0]
        username = line[1]
        password = line[2]
        template_file = 'dev_template2.j2'
        dev_list_dict = {"dev_name": dev_name,"ip":ip, "username":username,"password":password}
        with open (template_file) as f:
            dev_temp = f.read()
        template = jinja2.Template(dev_temp)
        M = template.render(dev_list_dict)
        with open ('dev_list.yml' , 'a') as f:
            f.writelines(M)
