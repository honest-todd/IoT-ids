import argparse
import subprocess
from pathlib import Path 
import os


class MethodTshark:
    def __init__(self, pcap=args.read, output=args.output):
        self.pcap = pcap
        self.output = output

    def filter(self):
        # channel is a 11
        i = 0
        if not self.output:
            while os.path.exists('capture-%s.pcap' % i):
                i += 1
            self.output = 'capture-%s.pcap' % i
        else:
            pass

        cmd = ['tshark', '-r', Path(self.pcap), '-R', 'bthci_evt.bd_addr', '-o', self.output]
        subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--read', '-r', type=open, help='read pecap file')
    parser.add_argument('--capture', '-Uc', nargs='*', help='live capture using ubertooth')
    parser.add_argument('--help', '-h', help='show this help message')
    parser.add_argument(
        '--out', '-o', action='store', type=argparse.FileType('w'), dest='output', help='')
    args = parser.parse_args()
    MethodTshark(args.read, args.output)


if __name__ == '__main__':
    main()

