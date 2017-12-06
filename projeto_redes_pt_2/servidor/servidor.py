#!/usr/bin/env python

# servidor.py
from socket import *
import time

# cria um objeto socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# pega nome do host local
host = gethostname()

port = 9999

# liga host à porta
serverSocket.bind((host, port))

print('Servidor aguardando conexão...')

# até 25 requests na fila
serverSocket.listen(25)

# estabelece conexão
clientsocket,addr = serverSocket.accept()

print("O servidor conectou-se a %s" % str(addr))
#currentTime = time.ctime(time.time()) + "\r\n"
#clientsocket.send(currentTime.encode('ascii'))
#clientsocket.close()

def listenCliente():
	while True:
		requestCliente = clientsocket.recv(1024).decode('ascii')
	clientsocket.close()
