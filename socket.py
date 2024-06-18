# Name: 1-socket.py
# Author: emily h. (nemo) 
# Date: 30.04.24
# Description: A program that connects via socket to a remote connection, receives CMD commands and returns output, and on the other side connects with netcat.

import socket 
host = ""
port = ""

import socket
hostname = ""
portnum = ""

def netcat ():
	 s=socket.socket()

#create socket and connect the clinet
with socket.socket () as client:
    client.connect((host, port))


#recive commands
commands = client.recv ()

#send answer
answer = input ("")
client.sendall (answer)
