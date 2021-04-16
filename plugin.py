#!/usr/local/bin/python3.9
import argparse
import subprocess
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--read', '-r', help='read pcap file')
    parser.add_argument('--interface', '-i', default='/tmp/pipe', help='set capture interface')
    parser.add_argument('--capture', '-c', nargs='*', default='bthci_evt.bd_addr',
                        help='live capture using ubertooth')
    parser.add_argument('--output', '-o', help='specify outfile')
    args = parser.parse_args()
    tshark = MethodTshark(args.read, args.output, args.capture, args.interface)

    if args.read is True:
        tshark.filter()
    elif args.interface is True and args.capture is True:
        tshark.capture()
    elif args.interface is True and args.capture is False:
        tshark.capture()
    elif args.interface is False and args.capture is True:
        print('ERROR: Must specify Interface')
        exit()


class MethodTshark:
    def __init__(self, pcap, output, capture, interface):
        self.pcap = os.path.join(os.getcwd(), os.path.abspath(pcap))
        self.output = output
        self.capture = capture
        self.interface = interface

    def filter(self):
        # channel is a 11
        i = 0
        if not self.output:
            while os.path.exists('capture-%s.pcap' % i):
                i += 1
            self.output = 'capture-%s.pcap' % i
        else:
            pass

        cmd = ['tshark', '-r', self.pcap, '-Y', 'bthci_evt.bd_addr', '-w', self.output]
        subprocess.run(cmd)

    def capture(self):
        cmd1 = ['mkfifo', self.interface]
        cmd2 = ['tshark', '-i', self.interface, '-f', self.capture, '-2', '-w', self.output]
        subprocess.run(cmd1, stdout=subprocess.PIPE, check=True)
        subprocess.run(cmd2, stdout=subprocess.PIPE, check=True)


if __name__ == '__main__':
    main()

