#from __future__ import print_function , unicode_literal
import jinja2
import time
import csv

cancel = False
device_list= []


with open ('dev_list.yml' , 'w') as f:
        f.writelines("---\n\n")


file = csv.reader(open('switches-list.csv'),delimiter = ',')
next(file)
for line in file :
        dev = line[1]
        dhcpsubnet = line[3]
        template_file = 'conf_template.j2'
        dev_list_dict = {"dhcpsubnet":dhcpsubnet}
        with open (template_file) as f:
            dev_temp = f.read()
        template = jinja2.Template(dev_temp)
        M = template.render(dev_list_dict)
        with open ('%s.txt'%dev , 'a') as f:
            f.writelines(M)
