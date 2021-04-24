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
        Python3 kismet_proc.py -t add-alert -a APSPOOF
        Python3 kismet_proc.py -t add-source -s captures/Bluetooth1.cap
    '''
    def __init__(self, source, task, alert):
        self.source = source
        self.task = task
        self.alert = alert

    def get_active_logs(self):
        '''
        '''
        resp = self.api_call("logging/active.itjson", s)
        if resp == 404:
            print('ERROR: no active logs found')
        
        return json.loads(resp)
    
    
    def get_datasources(self):
        '''
        '''
        resp = self.api_call("datasource/all_sources.json", s)
        if resp == 404:
            print('ERROR: no datasources defined')
        
        # convert to json
        resp = json.loads(resp)
        return resp
    
    def api_call(self, path, s):
        '''
            params
                path -- path of request, excluding the root path
                s -- current session 
            
        '''
        resp = None
        try:
            resp = s.get("http://{}:{}@localhost:2501/{}".format(
                                        credentials['username'], 
                                        credentials['password'], 
                                        path
                                    ))
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')

        except ERROR as e:
            print('ERROR')
        
        return resp
        
    def start_up(self, s):
        # no session cookie
        # print(self.api_call('auth/apikey/list.json', s).status_code)
        if self.api_call('auth/apikey/list.json', s).text:
            
            # create admin API token. this will be the master one for the system. no exp
            s.post("http://{}:{}@localhost:2501/auth/apikey/generate.cmd".format(
                                credentials['username'], credentials['password']), 
                                json={
                                    'name': credentials['username'],
                                    'role': 'admin',
                                    'duration': 0
                                })
        sessionCookie = self.api_call('auth/apikey/list.json', s).json()

        resp = self.api_call("session/check_session", s)
        if resp == 401: 
            print('ERROR: invalid login credentials')
            return -1
        # s.get('https://httpbin.org/cookies/set/sessioncookie/{}'.format(sessionCookie)) # set session cookie as our API token
        # sessionCookie = s.get('https://httpbin.org/cookies')
        print(sessionCookie)
        return sessionCookie

    def run_task(self):
        '''
        '''
        session = requests.Session()
        sessionCookie = self.start_up(session)
        # cj = requests.cookies.cookiejar_from_dict(sessionCookie[0])
        if self.task == 'add-alert':
            session.post("http://{}:{}:{}@localhost:2501/alerts/definitions/define_alert.cmd".format(
                                credentials['username'], credentials['password'], sessionCookie[0]), 
                                json={
                                    'name': credentials['username'],
                                    'class': self.alert,
                                    'role': 'admin',
                                    'severity':10,
                                    'description': 'desc',
                                    'throttle': '5/min',
                                    'burst': '1/sec'
                                })
            
        if self.task == 'add-source':
            for src in self.source:
                path = os.path.join(os.getcwd(), os.path.abspath(src))
                src = '/' + src
                source = "{}:type=pcapfile,name=test,realtime=false".format(src)
                print(source)
                status = session.post("http://{}:{}:{}@localhost:2501/datasource/add_source.cmd".format(
                                        credentials['username'], credentials['password'], sessionCookie[0]['kismet.httpd.auth.token']), 
                                        json={
                                            "definition":source
                                        }).text
                print(status)
                

        if self.task == 'analysis':
            print('USER: {}'.format(credentials['username']))
            print('DATA SOURCES: {}'.format(self.get_datasources()))
            print('ACTIVE LOGS: {}'.format(self.get_active_logs()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--datasource', nargs='*', type=str)
    parser.add_argument('-a', '--alert', nargs='*', type=str)
    parser.add_argument('-t', '--task',  choices = ['analysis', 'add-source', 'add-alert'], type=str)
    contents = parser.parse_args()
    kis = kismet(contents.datasource, contents.task, contents.alert)
    kis.run_task()
    
if __name__ == '__main__':
    main()
