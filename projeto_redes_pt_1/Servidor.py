from socket import *
from threading import Thread
import http.client

class Servidor:
    """ Servidor possui dois sockets tcp e udp ouvindo a mesma porta
        Sua funcao principal eh echoar a mensagem recebida de volta para o cliente

    
    """
    def __init__(self):
        # informacoes basicas para conexao
        self._hostServidor = "localhost"
        self._portaServidor = 20200
        self._ToleranciaAntesRecusaConexao = 1 # numero conexoes recusadas antes de fechar o socket para novas conexoes.
        self._conexao = (self._hostServidor, self._portaServidor)
        # criacao do socket tcp
        self._tcp = socket(AF_INET, SOCK_STREAM)
        self._tcp.bind(self._conexao)
        self._tcp.listen(self._ToleranciaAntesRecusaConexao)
        # criacao do socket udp
        self._udp = socket(AF_INET, SOCK_DGRAM)
        self._udp.bind(self._conexao)
        
        print("Servidor iniciado.")


    def esperarMensagemTCP(self):
        """ 
            Aguarda mensagens tcp e a retorna junto ao tipo de conexao usada (tcp no caso)

        """
        print("Aguardando conexoes TCP")
        while True:
            conexao_cliente, endereco_cliente = self._tcp.accept()
            msg_estado = "Conectado por " + str(endereco_cliente)
            print(msg_estado)

            requisicao_cliente = conexao_cliente.recv(1024) 
            # conexao_cliente.type retorna SockKind.STREAM nesse caso (TCP)
            mensagem_retorno = "Mensagem >>> " + requisicao_cliente.decode("UTF-8") + " | via: " + str(conexao_cliente.type)
            conexao_cliente.send(bytes(mensagem_retorno, "UTF-8"))
            conexao_cliente.close() 


    def esperarMensagemUDP(self):
        """ 
            Aguarda mensagens udp e a retorna junto ao tipo de conexao usada (udp no caso)
            
        """
        print("Aguardando conexoes UDP")
        while True:
            mensagem_cliente, endereco_cliente = self._udp.recvfrom(2048)
            print("Requisição UDP de " + str(endereco_cliente))
            # conexao_cliente.type retorna SockKind.DGRAM nesse caso (UDP)
            mensagem_modificada = "Mensagem >>> " + mensagem_cliente.decode("UTF-8") + " | via: " + str(self._udp.type)
            self._udp.sendto(bytes(mensagem_modificada, "UTF-8"), endereco_cliente)


if __name__ == '__main__':
    """
        Inicia duas threads uma para cada metodo da classe Servidor
    """
    objServidor = Servidor()
    try:
        Thread(target=objServidor.esperarMensagemTCP).start()
        Thread(target=objServidor.esperarMensagemUDP).start()

    except Exception as msg_erro:
        print(msg_erro)