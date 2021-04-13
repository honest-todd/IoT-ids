import argparse
import subprocess
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--read', '-r', type=open, help='read pcap file')
    parser.add_argument('--capture', '-Uc', nargs='*', help='live capture using ubertooth')
    parser.add_argument(
        '--out', '-o', action='store', type=argparse.FileType('w'), dest='output', help='')
    args = parser.parse_args()
    MethodTshark(args.read, args.output)


class MethodTshark:
    def __init__(self, pcap, output):
        self.pcap = os.path.abspath(pcap)
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

        cmd = ['tshark', '-r', self.pcap, '-R', 'bthci_evt.bd_addr', '-o', self.output]
        subprocess.run(cmd)


if __name__ == '__main__':
    main()
