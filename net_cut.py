#! /usr/bin/env python3

import netfilterqueue

def process_packet(packet):
	print(packet)
	packet.drop()

queue = netfilterqueue.NetfilterQueue()
# queue number is set to the queue number set in the iptables rule 
# iptables -I FORWARD -j NFQUEUE --queue-num 0 
queue.bind(0, process_packet)
queue.run() 