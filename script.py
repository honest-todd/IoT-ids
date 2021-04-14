#!/usr/local/bin/python3.9
import os, sys
import uuid
import requests
import argparse
import json
from requests.exceptions import HTTPError
from config import credentials
       
class kismet():
    '''
        usage: python3 script.py -d captures -t add-source
    '''
    def __init__(self, dir, task):
        self.dir = os.path.abspath(os.path.dirname(dir))
        self.task = task

    def api_call(self, url):
        '''
        '''
        try:
            resp = requests.get("http://{}:{}@localhost:2501/{}".format(
                                    credentials['username'], 
                                    credentials['password'], 
                                    url
                                ))
            
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
        return resp
    
    
    def get_datasources(self):
        '''
        '''
        resp = self.api_call("datasource/all_sources.json")
        if resp == 404:
            print('ERROR: no datasources defined')
        
        # convert to json
        resp = json.loads(resp)
        return resp
    
    def add_datasource(self, source ='/captures/Bluetooth1.cap', name ='Bluetooth1.cap'):
        '''
            params
                source -- url of capture file
                name -- some name for datasource
                
            posts a capture to a session.
        '''
        try:
            requests.post("http://{}:{}@localhost:2501/datasource/add_source.cmd".format(
                                    credentials['username'], 
                                    credentials['password']), 
                                    data={'source':'{}:type=pcapfile'.format(source),
                                    'name': '{}'.format(name),
                                    'realtime': 'false'
                                })
                        
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
    
    def run_task(self):
        '''
            Runs a routine specified via command line. Either analysis of ids or add source.
        '''
        if self.check_login() == -1: 
            sys.exit()
        
        if self.task == 'add-source':
            self.add_datasource()
        elif self.task == 'analysis':
            # write to file
            print('USER: {}'.format(credentials['username']))
            print('DATA SOURCES: {}'.format(self.get_datasources()))
            print('ACTIVE LOGS: {}'.format(self.get_active_logs()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', required=True, type=str)
    parser.add_argument('-t', '--task',  choices = ['analysis', 'add-source'], required=True, type=str)
    contents = parser.parse_args()
    kis = kismet(contents.dir, contents.task)
    kis.run_task()
    
if __name__ == '__main__':
    main()
