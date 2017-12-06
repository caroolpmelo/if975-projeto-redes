# cliente.py  
import socket

# cria um objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# pega nome do host local
host = socket.gethostname()                           

port = 9999

# conexão no host pela porta
s.connect((host, port))                               

# recebe no máximo 1024 bytes
tm = s.recv(1024)                                     

s.close()

print("O tempo que o servidor demorou foi %s" % tm.decode('ascii'))