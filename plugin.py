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

    if args.read is not None:
        tshark.filter()
    elif args.read is None:
        tshark.output_file()
        tshark.filter()
    elif args.interface is not None and args.capture is not None:
        tshark.capture()
    elif args.interface is not None and args.capture is None:
        tshark.capture()
    elif args.interface is None and args.capture is not None:
        print('ERROR: Must specify Interface')
        exit()


class MethodTshark:
    def __init__(self, pcap, output, capture, interface):
        self.pcap = os.path.join(os.getcwd(), os.path.abspath(pcap))
        self.output = output
        self.capture = capture
        self.interface = interface

    def output_file(self):
        # create default output file if one is not specified
        i = 0
        if not self.output:
            while os.path.exists('capture-%s.pcap' % i):
                i += 1
            self.output = 'capture-%s.pcap' % i
        else:
            pass
        return self.output
    
    def filter(self):
        # uses tshark via subprocess to apply the filter to the input and output a file
        # channel is a 11

        cmd = ['tshark', '-r', self.pcap, '-Y', 'bthci_evt.bd_addr', '-w', self.output]
        print(f'Processing \'{self.pcap}\' ...')
        subprocess.run(cmd)

    def capture(self):
        cmd1 = ['mkfifo', self.interface]
        cmd2 = ['tshark', '-i', self.interface, '-f', self.capture, '-2', '-w', self.output]
        subprocess.run(cmd1, stdout=subprocess.PIPE, check=True)
        subprocess.run(cmd2, stdout=subprocess.PIPE, check=True)


if __name__ == '__main__':
    main()

