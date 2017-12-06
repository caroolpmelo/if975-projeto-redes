# servidor.py 
import socket                                         
import time

# cria um objeto socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# pega nome do host local
host = socket.gethostname()                           

port = 9999                                           

# liga host à porta
serversocket.bind((host, port))                                  

print('Servidor aguardando conexão...')

# até 25 requests na fila
serversocket.listen(25)                                           

while True:
    # estabelece conexão
    clientsocket,addr = serversocket.accept()      

    print("O servidor conectou-se a %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    clientsocket.send(currentTime.encode('ascii'))
    clientsocket.close()