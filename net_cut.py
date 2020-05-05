#! /usr/bin/env python3

""" run this before executing this script
 iptables -I FORWARD -j NFQUEUE --queue-num 0 

flush the iptables after quitting this script
	iptables --flush
"""

import netfilterqueue

def process_packet(packet):
	packet.drop()

queue = netfilterqueue.NetfilterQueue()
# queue number is set to the queue number set in the iptables rule (0)
queue.bind(0, process_packet)
queue.run() 