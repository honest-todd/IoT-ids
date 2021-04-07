

We will proccess data sources via the **command line** 

compile various commands with control flow into a script in some language...

# Load Data into Kismet

Kismet recieves data (which can be packets, devices, or other information) from “data sources”
 - we will use pcap files as our primary viable data source... Ubertooth... more?


#### ex.
```bash
$ kismet -c /catpures/foo.pcap:uuid=1,realtime=false,pps=1000,name=capture_1
```
 

## Flags we will specify for each .pcap source definition 


* **uuid** -  Kismet usually generates a UUID based on attributes of the **source**
    * ex. interface MAC address if the datasource is linked to a physical interface
    * ex. device’s position in the USB bus, or some other consistent identifier. 
    * We will likely override this and manually set them due to bluetooth????

    

* **realtime** - reduce the packet processing rate to the original capture rate. In other words, packets will be processed with real-time delays equal to how they were received.
    * realtime=false
   
* **pps** - packets-per-second rate. Throttles processing of the packet to a more sustainable speed. 
    * Note: cannot be combined with the `realtime` option.
    * We will develop a threshold based on system processing capabilities (something simple for now)

* **name** -  name of the data source 


# output a JSON record


```bash
$ kismetdb_statistics --in capture_1.kismet --json 
```
outputs a .kismet file containg everything Kismet knows about the given source.

this is an exmaple from linux wifi 
```json
{
  "data_packets": 8,
  "datasources": [
    {
      "definition": "rtl433-0:name=carnuc-rtl433",
      "hardware": "Generic RTL2832U OEM",
      "interface": "rtl433-0",
      "name": "carnuc-rtl433",
      "packets": 8,
      "type": "rtl433",
      "uuid": "5E600813-0000-0000-0000-00005DBB0805"
    },
    {
      "definition": "wlx000e8e5c8866:name=carnuc-mediatek",
      "hardware": "mt76x2u",
      "hop_channels": [                                                                                                            
        "1",                                                                                                                       
        "1HT40+",                                                                                                                  
        "2",                                                                                                                       
        "3",                                                                                                                            
	  ],
      "hop_rate": 5,
      "interface": "wlx000e8e5c8866",
      "name": "carnuc-mediatek",
      "packets": 424,
      "type": "linuxwifi",
      "uuid": "5FE308BD-0000-0000-0000-000E8E5C8866"
    }
  ],
  "device_max_time": 1554240046,
  "device_min_time": 1554239405,
  "devices": 133,
  "diag_distance_km": 11.00620557382399,
  "file": "/home/dragorn/wavehack/carnuc-20190402-17-10-03-1.kismet",
  "kismetdb_version": 5,
  "max_lat": 40.000000000,
  "max_lon": -70.000000000,
  "min_lat": 45.000000000,
  "min_lon": -75.000000000,
  "packets": 447
}
```
## Flags

* **skip-clean** - kismetdb_strip_packets runs a SQL Vacuum command to optimize the database and clean up any journal files. 
    * Skipping this process will save time on larger captures.



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
