#importing required libraries

import jinja2

cancel = False
device_list= []

#asking the user to enter the devices ips and credentials and creating a device list from user input

while (True):
    name = input ("Enter the device name : ")
    ip_address = [str(i) for i in input("enter the device ip address ( e.g: 1.1.1.1): ").split(" ")]
    username = [str(i) for i in input("enter the username to used to log in to the device: ").split(" ")]
    password = [str(i) for i in input("enter the device password used to log in to the device: ").split(" ")]
    device_type = [str(i) for i in input("enter the device type( cisco_is , dell_os6 , hp_procurve): ").split(" ")]

    device_list.append({
        "name": name,
        "ip_address": ip_address,
        "username":  username,
        "password": password,
        "device_type": device_type
    })

    cont = input("Add another device? (Y/N)")
    if cont == "N":
        break;
    
#rednering the jinja2 template to create the device db

with open ('device_rendered_list.yml' , 'w') as f:
    f.writelines("---\n\n")


for d in device_list:
    name = d['name']
    name_str = ''.join(str(e) for e in name)
    ip_address = d['ip_address']
    ip_address_str = ''.join(str(e) for e in ip_address)
    username = d['username']
    username_str = ''.join(str(e) for e in username)
    password = d['password']
    password_str = ''.join(str(e) for e in password)
    device_type = d['device_type']
    device_type_str = ''.join(str(e) for e in device_type)
    dev_list_dict = {"name": name_str , "ip_address":ip_address_str, "username":username_str,"password":password_str,"device_type":device_type_str}
    template_file = 'dev_template.j2'
    with open (template_file) as f:
        dev_temp = f.read()
    template = jinja2.Template(dev_temp)
    M = template.render(dev_list_dict)
    with open ('device_rendered_list.yml' , 'a') as f:
        f.writelines(M)


