# pyHax
A collection of tools written in python.

## Requirements 
- [Scapy](https://pypi.org/project/scapy/) `pip install scapy`
- A Linux system

<hr>

### MAC Changer 
**Usage**: `mac_changer.py [-h] [-m MAC] [-r] interface`

Example-
> `python3 mac_changer.py wlan0 -m 00:11:22:33:44:55`

Reset the MAC-
> `python3 mac_changer.py wlan0 -r`

### Network Scanner
**Usage**: `network_scanner.py [-h] ip` 

> `python3 network_scanner.py 10.2.0.1/24` will scan the all IPs in the gateway and return MAC addresses for the responses.

<hr>

### ARP Spoofer
*Requires port forwarding to be enabled on your machine* 

` echo 1 > /proc/sys/net/ipv4/ip_forward` *does the job*

**Usage**: ` arp_spoof.py [-h] [-t TARGET] [-s SPOOF] `

> `python3 arp_spoof.py -t 10.0.2.4 -s 10.0.2.1`

<hr>

### Packet Sniffer
*Requires ARP spoofing*

**Usage**: `packet_sniffer.py [-h] [-i INTERFACE]`

> `python3 packet_sniffer.py -i wlan0`

<hr>

### Net Cut
> Disables internet for the ARP spoofed victim machine

*Redirect all the packets recieved on your machine to a queue using the linux command -*

 `iptables -I FORWARD -j NFQUEUE --queue-num 0`


Accessing this queue in the Python script-

 `pip install netfilterqueue`

 > `netfilterqueue` might have some issues while installing on Python 3.8 check this [link](https://github.com/kti/python-netfilterqueue/issues/53).

 Make sure port forwarding is enabled and ARP spoof another machine

 Usage: `python3 net_cut.py'

*Flush the iptables after running the script*

`iptables --flush`

<hr>

### DNS Spoofer

*Edit the domain name to spoof(`rrname`) and the ip(`rdata`)*

**Usage**: `python3 dns_spoof.py`

<hr>



