
import ast
import socket
import sys
import os
from base64 import b64decode
import base64
import threading
import time
import logging
from help_utils import *

######################## logging setup #######################
logger      = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter   = logging.Formatter('%(levelname)s   %(message)s')

handler     = logging.FileHandler('server.log')
handler.setFormatter(formatter)
logger.addHandler(handler)
##############################################################



HOST_ADDR       = "127.0.0.1"
PORT            = 5000

clients_status  = {}
#{ client_name a.k.a (host_name,ip_address): ON/OFF}
clients_conns   = {}
msg_id          = 0




server          = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST_ADDR, PORT))
server.listen()



def write_response(msg):
    base64_dec_msg      = base64.decodebytes(msg)
    msg                 = base64_dec_msg.decode('utf-8')
    lst                 = ["Received", "Initialized", "Running", "Finished", "Error"]
    if any(msg.startswith(item) for item in lst):
        filepath        = os.path.join(os.getcwd(), "responses.txt")
        with open(filepath, "a") as f:
            f.write(msg + "\n")
        f.close()

                
def dispatch_data_dict(msg):
    msg     = ast.literal_eval(msg)
    out     = msg['output']
    err     = msg['err']
    id      = msg['id']
    if 'filename' in msg.keys():
        filename    = msg['filename']
    else:
        filename    = None
    return out, err, id, filename


def is_alive_msg(msg):
    if msg[:3] == "ack":
        return True
    return False

def check_data_type(msg,cl_name):
    dec_msg     = msg.decode('utf-8')
    if isBase64(msg) and not is_alive_msg(dec_msg):
        write_response(msg)
    elif is_alive_msg(dec_msg):
        pass
    else:
        msg     = msg.decode('utf-8')
        if(msg.startswith("{'output'")): # checking if data or alive msg
            out, err, id, filename      = dispatch_data_dict(msg)

            if(filename == None or err != ""):
                write_cl_data_file(out,err,id,cl_name)    #write data into file named after the client's name
            else: 
                download_file(out, err, id, filename)  
    

def write_cl_data_file(out,err,id,cl_name):
    hostname    = cl_name[0]
    filepath    = os.path.join(os.getcwd(), f"{hostname}.txt")
    with open(filepath, "a") as f:
        f.writelines(f"command number: {id}\n")
        if out != "":
            f.write(out + "\n\n\n\n\n")
        if err != "":
            f.writelines("err:" + err+ "\n\n\n\n\n")
            logger.error(f"in cmd id {id}: \t {err}")
    f.close()


def download_file(out, err, id, filename):
    filepath       = os.path.join(os.getcwd(), f"{filename}")
    with open(filepath, "w") as f:
        f.write(out)
    f.close()



def get_data(conn,cl_name):
    while(True):
        try:
            msg         = conn.recv(10000000)
            check_data_type(msg,cl_name)
        except socket.error:
            curr_time   = curr_date_and_time()
            logger.info(f"client {cl_name} disconnect - {curr_time}")
            client_disconnect(conn,cl_name)
            break



def send_msg(conn,cmd):
    global msg_id
    msg_id+=1
    msg     = {'payload':cmd.payload, 'type':cmd.type, 'args':cmd.args, 'id':msg_id}
    msg     = str(msg).encode('utf-8')
    try:
        conn.send(msg)
    except socket.error:
        client_disconnect(conn)
        conn.close()
    return



def client_disconnect(connection,cl_name=None):
    clients_status[cl_name] = "OFF"
    if connection == None: 
        connection          = clients_conns[cl_name]
    connection.close()
    return



def clients_handler():
        while(True):
            conn, addr          = server.accept()
            hostname            = socket.gethostname()
            ip_address          = socket.gethostbyname(hostname)
            client_name         = (hostname, ip_address)

            clients_conns[client_name]  = conn
            clients_status[client_name] = "ON"

            curr_time   = curr_date_and_time()
            logger.info(f"client {client_name} connect - {curr_time}")

            thread      = threading.Thread(target=get_data, args=(conn,client_name))
            thread.start()



            

