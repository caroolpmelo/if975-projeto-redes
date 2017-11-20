from socket import *

class TcpCliente:

    def __init__(self):
        self._hostServidor = "localhost"
        self._portaServidor = 20200
        self._conexao = (self._hostServidor, self._portaServidor)
        try:
            self._socket_cliente = socket(AF_INET, SOCK_STREAM)
            self._socket_cliente.connect(self._conexao)
        except Exception as msg_erro:
            print(msg_erro)
    
    def enviar_mensagem(self, mensagem):
        self._socket_cliente.send(bytes(mensagem, "UTF-8"))
        retorno_servidor = self._socket_cliente.recv(1024)
        self._socket_cliente.close()
        return retorno_servidor.decode("UTF-8")