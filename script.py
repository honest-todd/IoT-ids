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
        python3 script.py -t add-source -f captures/Bluetooth1.cap 
        
        python3 script.py -t analysis
    '''
    def __init__(self, source, task, alert):
        self.source = source
        self.task = task
        self.alert = alert

    def api_call(self, url):
        '''
        '''
        try:
            resp = requests.get("http://{}:{}@localhost:2501/{}".format(
                                    credentials['username'], 
                                    credentials['password'], 
                                    self.url
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
    
    def view_alert(self):
        '''
        '''
        resp = self.api_call("alerts/alerts_view.json")
        return resp

    def add_datasource(self):
        '''
            params
                source -- url of capture file
                name -- some name for datasource
                
            posts a capture to a session.
        '''
        try:
            for source in self.source:
                path = os.path.abspath(os.path.dirname(source))
                requests.post("http://{}:{}@localhost:2501/datasource/add_source.cmd".format(
                                        credentials['username'], 
                                        credentials['password']), 
                                        data={
                                            'source':'{}:type=pcapfile'.format(path),
                                            'name': '{}'.format(source),
                                            'realtime': 'false'
                                        })
                        
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')

    def add_alert(self):
        try:
            requests.post("http://{}:{}@localhost:2501/alerts/definitions/define_alert.cmd".format(
                                            credentials['username'], 
                                            credentials['password']), 
                                            data={
                                                'class':'{}'.format(self.alert)
                                                # ,
                                                # 'severity': '{}'.format(severity),
                                                # 'throttle': '{}'.format(throttle),
                                                # 'burst': '{}'.format(burst)
                                            })

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')


    def run_task(self):
        '''
            Runs a routine specified via command line. Either analysis of ids or add source.
        '''
        if self.check_login() == -1: 
            sys.exit()

        elif self.task == 'add-source':
            self.add_datasource()

        elif self.task == 'add-alert':
            self.add_alert()

        elif self.task == 'analysis':
            print('USER: {}'.format(credentials['username']))
            print('DATA SOURCES: {}'.format(self.get_datasources()))
            print('ACTIVE LOGS: {}'.format(self.get_active_logs()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', nargs='*', type=str)
    parser.add_argument('-a', '--alert', nargs='*', type=str)
    parser.add_argument('-t', '--task',  choices = ['analysis', 'add-source', 'add-alert'], required=True, type=str)
    contents = parser.parse_args()
    kis = kismet(contents.file, contents.task)
    kis.run_task()
    
if __name__ == '__main__':
    main()
