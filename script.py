#!/usr/local/bin/python3.9
import os, sys
import uuid
import requests
import argparse
import json
from requests.exceptions import HTTPError
       
class kismet():
    '''
        
    '''
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        content = self.parse_args()
        self.username = content.username
        self.password = content.password
        self.directory = content.directory
        
    def parse_args(self):
        '''
            python3 script.py -d captures -u jugegp16 -p peep1
        '''
        self.parser.add_argument('-d', '--directory', type=str)
        self.parser.add_argument('-u', '--username',  type=str)
        self.parser.add_argument('-p', '--password',  type=str)
        return self.parser.parse_args()

    def api_call(self, url):
        '''
        '''
        try:
            resp = requests.get("http://{}:{}@localhost:2501/{}".format(self.username, self.password, url))
            if resp.status_code == 200: return resp.text
            return resp.status_code
        except:
            print('ERROR: make sure kismet is running locally')
        
    def check_login(self):
        '''
        '''
        resp = self.api_call("session/check_login")
        if resp == 401: 
            print('ERROR: invalid login credentials')
            return -1
    
    def get_active_logs(self):
        '''
        
        '''
        resp = self.api_call("logging/active.itjson")
        if resp == 404:
            print('ERROR: no active logs found')
        
        # convert to json
        resp = json.loads(resp)
        print(resp)
    
    
    def get_datasources(self):
        '''
        '''
        resp = self.api_call("datasource/all_sources.json")
        if resp == 404:
            print('ERROR: no datasources defined')
        
        # convert to json
        resp = json.loads(resp)
        print(resp)
    
    def add_datasource(self, source ='/captures/Bluetooth1.cap', name ='Bluetooth1.cap'):
        '''
            params
                source -- url of capture file
                name -- some name for datasource
                
            posts a capture to a session.
        '''
        try:
            requests.post("http://{}:{}@localhost:2501/datasource/add_source.cmd".format(self.username, self.password), 
                          data={'source':'{}:type=pcapfile'.format(source),
                                'name': '{}'.format(name),
                                'realtime': 'false'
                                })
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        
    
if __name__ == '__main__':
    kismet = kismet()
    if kismet.check_login() == -1: sys.exit()
    kismet.get_active_logs()
    kismet.add_datasource()
    kismet.get_datasources()
