#!/usr/local/bin/python3.9
import os, sys
import requests
import argparse
import json
from requests.exceptions import HTTPError
from config import credentials
       

class kismet():
    '''
        Python3 kismet_proc.py -a APSPOOF
        Python3 kismet_proc.py -s captures/Bluetooth1.pcap
    '''
    def __init__(self, source, alert):
        self.source = source
        self.alert = alert
        
        self.session = requests.Session()
        self.session.auth = (credentials['username'], credentials['password'])
        if self.api_call('auth/apikey/list.json').text == '[]':
            # create admin API token.
            status = self.session.post("http://@localhost:2501/auth/apikey/generate.cmd", 
                                    json={
                                        'name': credentials['username'],
                                        'role': 'admin',
                                        'duration': 0
                                    })
            print(status.json)
            
        self.session.session_key = self.api_call('auth/apikey/list.json').json()[0]
        
    def api_call(self, path):
        '''
            params
                path -- path of request, excluding the root path
        '''
        resp = None
        try:
            resp = self.session.get("http://@localhost:2501/{}".format(path))
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except ERROR as e:
            print('ERROR')
        
        return resp

    def run_task(self):
        '''
        
        '''
        if self.alert:
            status = self.session.post("http://@localhost:2501/alerts/definitions/define_alert.cmd", 
                                json={
                                    'name': 'APSPOOF',
                                    'class': str(self.alert),
                                    'role': 'admin',
                                    'severity':10,
                                    'description': 'desc',
                                    'throttle': '5/min',
                                    'burst': '1/sec'
                                }).text
            print(status)
            
        if self.source:
            for src in self.source:
                path = os.path.join(os.getcwd(), os.path.abspath(src))
                source = "{}:type=pcapfile,name=test,realtime=false".format(path)
                status = self.session.post("http://@localhost:2501/datasource/add_source.cmd", 
                                        json={
                                            "definition":source
                                        }).status_code
                print(status)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', nargs='*', type=str)
    parser.add_argument('-a', '--alert', nargs='*', type=str)
    contents = parser.parse_args()
    kis = kismet(contents.source, contents.alert)
    kis.run_task()
    
if __name__ == '__main__':
    main()
