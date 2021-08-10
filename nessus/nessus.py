# encoding = utf-8

import os
import sys
import time
import datetime
import requests

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    nessus_url = definition.parameters.get('nessus_url', None)
    access_key = definition.parameter.get('access_key', None)
    secret_key = definition.parameter.get('secret_key', None)
    
    nessus = "%s/scans/" % nessus_url 
    helper.log_info("URL: " + nessus)
    try:
        response = helper.send_http_request(
            url=nessus,
            method='GET',
            headers={
                'Content-type': 'application/json', 
                'X-ApiKeys': 'accessKey='+access_key+'; secretKey='+secret_key,
                },
            verify=False
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(
            "An HTTP Error occured while trying to access the Nessus API " + str(err))
                
    pass

def collect_events(helper, ew):
    
    nessus_url = helper.get_arg('nessus_url')
    access_key = helper.get_arg('access_key')
    secret_key = helper.get_arg('secret_key')
    
    
    helper.log_info("getEntries: " + time.strftime("%d-%m-%Y %H:%M:%S"))
    nessus = "%s/scans/" % nessus_url
    data = []
    
    
    response = helper.send_http_request(
            url=nessus,
            method='GET',
            headers={
                'Content-type': 'application/json', 
                'X-ApiKeys': 'accessKey='+access_key+'; secretKey='+secret_key,
                },
            verify=False
        )
    
    response.raise_for_status()
    a = response.json()
    for i in a['scans']:
        if i['enabled'] == True:
            id = i['id']
            scan_pull = nessus_url+'/scans/'+str(id)
            r = helper.send_http_request(
                    url=scan_pull,
                    method='GET',
                    headers={
                        'Content-type': 'application/json', 
                        'X-ApiKeys': 'accessKey='+access_key+'; secretKey='+secret_key,
                        },
                    verify=False
                )
            j = r.json()
            for i in j['hosts']:
                hosts=[]
                h_id = i['host_id']
                hosts.append(h_id)
                for h in hosts:
                    host_pull = scan_pull+'/hosts/'+str(h)
                    x = helper.send_http_request(
                            url=host_pull,
                            method='GET',
                            headers={
                            'Content-type': 'application/json', 
                            'X-ApiKeys': 'accessKey='+access_key+'; secretKey='+secret_key,
                            },
                            verify=False
                        )
                    y = x.json()
                    data.append(y)
                    
                    
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    
    import json
    for d in data:
        event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=json.dumps(d))
        ew.write_event(event)
