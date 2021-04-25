#!/usr/local/bin/python3.9
import os
import argparse
import plugin
from plugin import MethodTshark
import kismet_proc
import subprocess


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--automated', '-a',action='store_true' , help='perform a run with default values')
    parser.add_argument('--run', help='perform a normal run')
    parser.add_argument('--read', '-r', help='read pcap file')

    args = parser.parse_args()

    output = MethodTshark(args.read, None, None, None).output_file()

    if args.automated is True:
        MethodTshark(args.read, output, None, None).filter()
        kismet_proc.kismet(output, 'add-source')
    elif args.run is not None:
        plugin.main()
        kismet_proc.main()


if __name__ == '__main__':
    main()
