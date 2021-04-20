# Capturing Bluetooth Traffic using Wireshark
Wireshark can be accesed using the terminal command:

```bash
$ wireshark
```
This will open the wireshark GUI

Bluetooth traffic can either be captured life or the path of a pcap file can be used.
To find the mac addressed for the Bluetooth traffic being analysed type the following in the address bar:

### bthci_evt.bd_addr

Finally, you can export the resulting packets as a pcap by going to File and selecting:

### Export Specified Packets...

# Processing the Data

We will process data sources via the **command line** 

compile various commands with control flow into a script in some language...

# Load Data into Kismet

Kismet recieves data (which can be packets, devices, or other information) from “data sources”
 - we will use pcap files as our primary viable data source... Ubertooth... more?

```Python
Python3 kismet_proc.py -t add-source -f file.cap
```

# config APSPOOF

ASPOOF: Essentially a list of valid MAC addresses for a given SSID used to mediate activity.
* If a beacon or probe response for that SSID is seen from a MAC address not found in that list, an alert will be raised. This can be used to detect spoofed or evil twin attacks and attacks like Karma, however it will not detect attacks which also spoof the MAC address --- what if they do...

```Python
Python3 kismet_proc.py -t add-alert -a SPOOF
```
