#!/usr/bin/env python3

import scapy.all as scapy
import argparse

def scan(ip):
	#create arp request 
	arp_request = scapy.ARP(pdst=ip)
	# broadacast packet
	broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
	# joining the packets
	arp_request_broadcast = broadcast/arp_request
	#sending the packet and recieving response
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
	
	clients =  []
	for answer in answered_list:
		client_dict = {'ip' : answer[1].psrc, 'mac':answer[1].hwsrc }
		clients.append(client_dict)
	return clients


def print_result(clients):
	print('\nIP\t\t|\t MAC Address\n------------------------------------------')
	for client in clients:
		print(client['ip'] + '\t|\t' + client['mac'])
	print()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('ip', help="IP or IP range to scan.")
	args = parser.parse_args()
	result = scan(args.ip)
	print_result(result)



