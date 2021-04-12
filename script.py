#!/usr/local/bin/python3.9
import os, sys
import uuid
import requests
import argparse
import json
       
class kismet():
    '''
        exmaple usage:  python3 script.py -d captures -u jugegp16 -p peep1
    '''
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        content = self.parse_args()
        self.username = content.username
        self.password = content.password
        self.directory = content.directory
        
    def parse_args(self):
         '''
        '''
        self.parser.add_argument('-d', '--directory', type=str)
        self.parser.add_argument('-u', '--username',  type=str)
        self.parser.add_argument('-p', '--password',  type=str)
        return self.parser.parse_args()

    def api_call(self, url):
        try:
            resp = requests.get(url)
            if resp.status_code == 200: return resp.content
            return resp.status_code
        except:
            print('ERROR: make sure kismet is running locally')
        
    def check_login(self):
        resp = self.api_call("http://{}:{}@localhost:2501/session/check_login".format(self.username, self.password))
        if resp == 401: 
            print('ERROR: invalid login credentials')
            return -1
    
    def check_active_logs(self):
        resp = self.api_call("http://{}:{}@localhost:2501/logging/active.itjson".format(self.username, self.password))
        if resp == 404:
            print('ERROR: no active logs found')
        
        # convert to json
        resp = json.loads(resp)
        print(resp)

            
if __name__ == '__main__':
    kismet = kismet()
    if kismet.check_login() == -1: sys.exit
    kismet.check_active_logs()
    
    
    
# def main():
#     # loop through caps. this will be a flag. 
#     for i, file in enumerate(os.listdir('captures')):
#         UUID = uuid.uuid4() #try name too
        
#         # unable to find driver error
#         os.system("kismet -c /captures/{}:UUID={}".format(file, int(UUID))) 
    
#     # get stats
#     for i, file in enumerate(os.listdir()):
#         if 'Kismet-' in file:
#             os.system("kismetdb_statistics --in {}".format(file))
