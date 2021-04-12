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


```bash
	requests.post('http://username:password@localhost:2501/datasource/add_source.cmd', data=capture
```



# Update APSPOOF

ASPOOF: Essentially a list of valid MAC addresses for a given SSID used to mediate activity.
* If a beacon or probe response for that SSID is seen from a MAC address not found in that list, an alert will be raised. This can be used to detect spoofed or evil twin attacks and attacks like Karma, however it will not detect attacks which also spoof the MAC address --- what if they do...


Utilize .json dump from previous step 
* analyze uuids and add some / compare.... and more
```C
apspoof=Foo1:ssidregex="(?:foobar)",validmacs=00:11:22:33:44:55
apspoof=Foo2:ssid="Foobar",validmacs="00:11:22:33:44:55,AA:BB:CC:DD:EE:FF"
```
Note: The apspoof= configuration can specify exact string matches for the SSID, regular expressions using PCRE syntax, and single, multiple, or masked MAC addresses:


# Additional Alerts

Setup an alert using in ```kismet_alerts.conf``` using the following command
```C
alert=APSPOOF,5/min,1/sec
```
add more there are so many differnt [options](https://www.kismetwireless.net/docs/readme/alerts_and_wids/)
