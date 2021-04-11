#!/usr/local/bin/python3.9
import os
import uuid
import requests


def main():
    # loop through caps. this will be a flag. 
    for i, file in enumerate(os.listdir('captures')):
        UUID = uuid.uuid4() #try name too
        
        # unable to find driver error
        os.system("kismet -c /captures/{}:UUID={}".format(file, int(UUID))) 
    
    # get stats
    for i, file in enumerate(os.listdir()):
        if 'Kismet-' in file:
            os.system("kismetdb_statistics --in {}".format(file))
        

if __name__ == '__main__':
    main()