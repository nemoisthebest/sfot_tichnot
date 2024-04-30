# Name: 1-socket.py
# Author: emily h. (nemo) 
# Date: 30.04.24
# Description: this program connects remotely, receives CMD commands and returns output


import socket 
host = ""
port = ""

#create socket and connect the clinet
with socket.socket () as client:
	client.connect((host, port))

import client
hostname = ""
portnum = ""

def netcat ():
	s =socket.socket ()
  s.connect (hostname, int(portnum))

#recive commands
commands = client.recv ()

#send answer
answer = input ""
client.sendall (answer)
