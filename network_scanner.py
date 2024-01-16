#!/usr/bin/env python

import scapy.all as scapy
import optparse


##listar dispositivos
#scapy.arping(ip, iface=iface)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    options, arguments = parser.parse_args()
    return options
def scan(ip):
    #use ARP to ask who has target IP
    arp_request = scapy.ARP(pdst=ip)
    #set destination MAC to brodcast MAC
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')#instance of internet
    arp_request_broadcast = broadcast/arp_request
    #enviar el paquete y recibir la respuesta
    answered_list = scapy.srp(arp_request_broadcast, timeout=1)[0]
    #extract list(array)

    client_list = []
    for element in answered_list:
        client_dict = {'ip': element[1].psrc, 'mac': element[1].hwsrc}
        client_list.append(client_dict)

    return client_list

def print_result(results_list):
    print('IP \t\t\tMAC Adress\n--------------------------------------------')
    for client in results_list:
        print(client['ip']+ '\t\t' + client['mac'])

options = get_arguments()
scar_results = scan(options.target)
print_result(scar_results)