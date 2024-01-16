#!/usr/bin/env python

import subprocess
import optparse
import re

#retornar valores mediante funcion
def get_arguments():
    # parser object
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='interface to change its mac aderess')
    parser.add_option('-m', '--mac', dest='new_mac', help='new mac adress')
    # instruir para que analice la linea de comandos
    (options, arg) = parser.parse_args()  # options devuelve los valores de las opciones
    # arg lista de argumentos pocicionales
    if not options.interface:
        #handle error
        parser.error('[-] Plese specify an interface, use --help for more info')
    elif not options.new_mac:
        #handle error
        parser.error('[-] Plese specify an new mac, use --help for more info')
    return options



#separa en funcion de intentions
def mac_changer(interface, new_mac):
    print('[+] Changing MAC adress for ' + interface + ' to ' + new_mac)
    subprocess.run(['ifconfig', interface, 'down'])
    subprocess.run(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.run(['ifconfig', interface, 'up'])

def get_current_mac(interface):
    ifconfigResult = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    # regex para filtrar
    macAdressSerchResult = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfigResult)
    if macAdressSerchResult:
        return macAdressSerchResult.group(0)
    else:
        print('[-] Could not read the mac adress')


# subprocess.call('ifconfig '+ interface +' down', shell=True)
# subprocess.call('ifconfig '+ interface +' hw ether ' + new_mac, shell=True)
# subprocess.call('ifconfig '+ interface +' up', shell=True)


# interface = options.interface
# new_mac = options.new_mac

# funcion que devuelve los parametros
options = get_arguments()

#funcion devleve el mac actual
original_mac = get_current_mac(options.interface)
print('the Actual mac = '+str(original_mac))

#funcion que recive valores
mac_changer(options.interface, options.new_mac)

#el mac actual es lo mismo que la que se quiere cambiar
current_mac = get_current_mac(options.interface)
print('the current mac = '+str(current_mac))

print(options.new_mac)
print(original_mac)
if original_mac != options.new_mac:
    print('[+] MAC adress was succesfully changed to ' + current_mac)
else:
    print('[-] MAC adress did not get changed')






