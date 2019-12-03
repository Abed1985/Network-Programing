from jnpr.junos import Device
from lxml import etree
import xmltodict
import pprint
import json
import xlsxwriter
 
def lldp(dev,username,password):
    lldp_dict = {}
    with Device(host = dev,username = username,password= password,port = 22,normalize =True) as dev:
        output = dev.rpc.get_lldp_neighbors_information()
        lldp = etree.tostring(output,encoding = 'unicode')
        doc = xmltodict.parse(etree.tostring(output))
        my_dict = json.dumps(doc)
        lldp_store = json.loads(my_dict)
        return lldp_store           
 

def intdesc(dev,username,password):
    try:
        with Device(host = dev,username = username,password= password,port = 22,normalize =True) as dev:
            output2 = dev.rpc.get_interface_information(descriptions=True)
            intdesc = etree.tostring(output2,encoding = 'unicode')
            doc2 = xmltodict.parse(etree.tostring(output2))
            my_dict2 = json.dumps(doc2)
            intdesc_store = json.loads(my_dict2)
            return intdesc_store
    except (KeyError, TypeError):
        pass
