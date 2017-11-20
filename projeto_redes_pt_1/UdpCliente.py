from socket import *

class UdpCliente:

    def __init__(self):
        self._hostServidor = "localhost"
        self._portaServidor = 20200
        self._conexao = (self._hostServidor, self._portaServidor)
        try:
            self._socket_cliente = socket(AF_INET, SOCK_DGRAM)
            self._socket_cliente.connect(self._conexao)
        except Exception as msg_erro:
            print(msg_erro)

    def enviar_mensagem(self, mensagem):
        self._socket_cliente.sendto(bytes(mensagem, "UTF-8"), self._conexao)
        mensagem_retornada, endereco_servidor = self._socket_cliente.recvfrom(2048)
        self._socket_cliente.close()
        return mensagem_retornada.decode("UTF-8")