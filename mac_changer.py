#!/usr/bin/env python3

import subprocess
import argparse
import re
from colorama import Fore, Style

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("interface", help="Interface to change MAC ")
	parser.add_argument("-m", "--MAC", dest="mac", help="New MAC address")
	parser.add_argument("-r", "--Reset", help="Reset MAC ", action="store_true")
	args = parser.parse_args()
	if not args.mac and not args.Reset:
		parser.error("\n[-] -m or -r argument required, see --help for more info")
	return args


def change_mac(interface, mac):
	try:
		print(f"\n[+] Changing MAC address for {interface} to {mac}")
		subprocess.call(["ifconfig", interface, "down"])
		subprocess.call(["ifconfig", interface, "hw", "ether", mac])
		subprocess.call(["ifconfig", interface, "up"])
		verify_change(interface, mac)

	except Exception as e:
		print(f'\n{Fore.RED}[-] Error: No such interface - {interface}. Make sure the interface exists.')
	
	
def verify_change(interface, mac):
	print(f'[+] Current MAC: {mac}')
	ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
	ifconfig_mac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)
	if ifconfig_mac:
		ifconfig_mac = ifconfig_mac[0]
	else:
		print(f'{Fore.RED}[-] MAC not found for {interface}')
		return

	if mac == ifconfig_mac:
		print(f"{Fore.GREEN}[+] Changed MAC address for {interface} to {mac} successfully")
	else: 
		print(f"{Fore.RED}[-] Failed to Change MAC address for {interface}")


def reset_mac(interface):
	output = subprocess.check_output(["ethtool", "-P",  interface]).decode('utf-8')
	default_mac = output.split(' ')[2].strip('\n')
	change_mac(interface, default_mac)



if __name__ == '__main__':
	args = parse_arguments()
	reset_mac(args.interface) if args.Reset else change_mac(args.interface, args.mac)
	print(Style.RESET_ALL)



