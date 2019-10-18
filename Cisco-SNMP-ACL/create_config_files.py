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
        dev = line[0]
        location = line[3]
        subnet = line[4]
        template_file = 'conf_template2.j2'
        dev_list_dict = {"location":location,"subnet":subnet}
        with open (template_file) as f:
            dev_temp = f.read()
        template = jinja2.Template(dev_temp)
        M = template.render(dev_list_dict)
        with open ('%s.txt'%dev , 'a') as f:
            f.writelines(M)
