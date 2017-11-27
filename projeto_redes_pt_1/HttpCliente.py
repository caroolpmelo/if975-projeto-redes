from socket import *
from urllib.parse import urlparse

class HttpCliente:
    
    def __init__(self):
        self._hostServidor = "localhost"
        self._portaServidor = 8080   # porta igual a do tcp para testes
        self._conexao = (self._hostServidor, self._portaServidor)
        try:
            self._socket_cliente = socket(AF_INET, SOCK_STREAM)
            self._socket_cliente.connect(self._conexao)
        except Exception as msg_erro:
            print(msg_erro)
    
    def receber_pagina(self, url):
        url_info = urlparse(url)
        mensagem_http = str.format("GET {0} HTTP/1.1\r\nHost: {1}\r\n\r\n", url_info.path, url_info.netloc)
        
        self._socket_cliente.send(bytes(mensagem_http, "UTF-8"))
        retorno_servidor = self._socket_cliente.recv(1024)
        self._socket_cliente.close()
        return retorno_servidor.decode("UTF-8")