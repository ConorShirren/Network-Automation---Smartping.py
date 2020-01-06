import os
import subprocess
import platform
import ipaddress
import re

class Smartping():

    def __init__(self,ips=[],ping_count=1, subnet=""):
        self.ips=ips
        self.ping_count = ping_count
        self.subnet = subnet
        self.platform = platform.system().lower()
        self.ping_result = ""
        self.flattened_ips=[]  #IPs will be added here
    
    def load_ips(self,filename):
        with open(filename) as file:  #load IPs from a spesific file
            ip_text_file = file.read()
            self.ips = ip_text_file.split("\n")

    def flatten_ips(self):
        for ip in self.ips:
            if "/" in ip:  #convert network address to IPs
                self.load_ips_from_subnet(ip)
            else:
                self.flattened_ips.append(ip)

    def ping(self):
        self.flatten_ips()
        if self.platform == "windows":
            self.windows_ping()
        else:
            self.linux_ping()

    def linux_ping(self):
        for ip in self.flattened_ips:
            command = "ping -c {} {}".format(str(self.ping_count), ip)  #EX: ping -c 1 10.10.10.1  (send 1 ping)
            response = os.system(command)
            if response == 0:
                self.ping_result += ip + " is up!\n"
            else:
                self.ping_result += ip + " is down!\n"
        #print(self.ping_result)

    def windows_ping(self):
        for ip in self.flattened_ips:
            command = "ping -a -n {} {}".format(str(self.ping_count), ip)   #EX: ping -n 1 10.10.10.1  (send 1 ping)
            response = subprocess.run(command, capture_output=True)
            output = response.stdout.decode()
            FQDN = re.search("Pinging (.*\.gm\.com)", output)
            print(FQDN.group())
            #print(output)
            if "Destination host unreachable" in output:
                self.ping_result += ip + " (" + FQDN.group(1) +")           Status: DOWN [Destination host unreachable] \n"
            elif "Request timed out" in output:
                self.ping_result += ip + " (" + FQDN.group(1) +")           Status: DOWN [Request timed out]\n"
            else:
                self.ping_result += ip + " (" + FQDN.group(1) +")           Status: UP\n"
        #print(self.ping_result)



    def load_ips_from_subnet(self,subnet):
        for addr in ipaddress.ip_network(subnet):  #find all the IPs in network, add it to list
            self.flattened_ips.append(str(addr))

    def save_output(self,filename="pingresult.txt"):  #write the ping result to a file
        file = open(filename, "w")
        file.write(self.ping_result)
        file.close()


############################################
#Run the script by editing below
############################################

#Step 1, call the class object and create a smartping object
a = Smartping()
#Step 2, load IPs.
print("\nPlease specify IP address location (.txt file) : \n")
add_file = input()
print("\n")
a.load_ips(add_file)   #load IPs from file
a.ping()
a.save_output("Results.txt")
#
print("\n\n\n * * * * * All Pings Returned. Check Output File for results * * * * * \n\n\n")
#
#
# End or Script
