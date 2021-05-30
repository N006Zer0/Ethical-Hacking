### -- Ashish Chaturvedi -- ###

import subprocess
import  optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to chnage MAC Address.")
    parser.add_option("-m", "--mac", dest="new_mac_addr", help="New MAC Address.")
    (options, arguments)= parser.parse_args()
    if not options.interface:
        parser.error("[-] Please enter the interface name for more information use, --help or -h")

    elif not options.new_mac_addr:
        parser.error("[-] Please enter the MAC Addres for more information use, --help or -h")

    return options

def change_mac(interface, new_mac_addr):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac_addr])
    subprocess.call(["ifconfig", interface, "up"])
    # print("[+] Now our " + interface + " MAC Address change to " + new_mac_addr)

def mac_change_validation(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    

    match_mac_change = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result.decode("utf-8"))
    if match_mac_change:
        return match_mac_change.group(0)
    else:
        print("[-] could not read mac address.")

options = get_arguments()

validate_mac = mac_change_validation(options.interface)
print("Privious MAC Address = " + str(validate_mac))

change_mac(options.interface, options.new_mac_addr)

new_mac_after_change = mac_change_validation(options.interface)
if new_mac_after_change == options.new_mac_addr:
    print("[+] MAC Addrss successfully changed to " + str(options.new_mac_addr))
else:
    print("[-] Faild to changed MAC Address.")
