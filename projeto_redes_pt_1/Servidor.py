from socket import *
from threading import Thread
import http.client
import sys
import os

class Servidor:
    """ Servidor possui dois sockets tcp e udp ouvindo a mesma porta
        Sua funcao principal eh echoar a mensagem recebida de volta para o cliente

    """
    def __init__(self):
        # informacoes basicas para conexao
        self._hostServidor = ""
        self._portaServidor = 20200
        self._conexao_tcp_udp = (self._hostServidor, self._portaServidor)
        
        self._portaServidorHttp = 8080
        self._conexao_http = (self._hostServidor, self._portaServidorHttp)


    def MensagemTCP(self):
        """ 
            Aguarda mensagens tcp e a retorna junto ao tipo de conexao usada (tcp no caso)

        """

        # criacao do socket tcp
        socket_tcp = socket(AF_INET, SOCK_STREAM)
        socket_tcp.bind(self._conexao_tcp_udp)
        socket_tcp.listen(5)

        print("Servidor TCP iniciado: Aguardando conexoes...")

        while True:
            try:
                conexao_cliente, endereco_cliente = socket_tcp.accept()
                msg_estado = "Conectado por " + str(endereco_cliente)
                print(msg_estado)

                requisicao_cliente = conexao_cliente.recv(1024) 
                # conexao_cliente.type retorna SockKind.STREAM nesse caso (TCP)
                mensagem_retorno = "Mensagem >>> " + requisicao_cliente.decode("UTF-8") + " | via: " + str(conexao_cliente.type)
                conexao_cliente.send(bytes(mensagem_retorno, "UTF-8"))
                conexao_cliente.close()
            
            except Exception as msg_erro:
                print(msg_erro)


    def MensagemUDP(self):
        """ 
            Aguarda mensagens udp e a retorna junto ao tipo de conexao usada (udp no caso)
            
        """
        socket_udp = socket(AF_INET, SOCK_DGRAM)
        socket_udp.bind(self._conexao_tcp_udp)
        
        print("Servidor UDP iniciado: Aguardando conexoes...")

        while True:
            try:
                mensagem_cliente, endereco_cliente = socket_udp.recvfrom(2048)
                print("Requisição UDP de " + str(endereco_cliente))
                # conexao_cliente.type retorna SockKind.DGRAM nesse caso (UDP)
                mensagem_modificada = "Mensagem >>> " + mensagem_cliente.decode("UTF-8") + " | via: " + str(socket_udp.type)
                socket_udp.sendto(bytes(mensagem_modificada, "UTF-8"), endereco_cliente)
            
            except Exception as msg_erro:
                print(msg_erro)


    def MensagemHTTP(self):
        """ 
            Aguarda mensagens HTTP e a retorna a pagina solicitada

        """

        # criacao do socket tcp
        socket_http = socket(AF_INET, SOCK_STREAM)
        socket_http.bind(self._conexao_http)
        socket_http.listen(5)
        diretorio_servidor = "Web"

        print("Servidor HTTP iniciado: Aguardando conexoes...")

        while True:
            try:
                conexao_cliente, endereco_cliente = socket_http.accept()
                msg_estado = "Conectado por " + str(endereco_cliente)
                print (msg_estado)
                requisicao_cliente = conexao_cliente.recv(1024).decode("UTF-8")
                
                # separar informações
                lista_de_string = requisicao_cliente.split(" ")

                
                #cabecalho_requisitado = lista_de_string[0]
                arquivo_requisitado = lista_de_string[1]
                

                # Recupera arquivo do servidor
                if arquivo_requisitado == "/": arquivo_requisitado = "/index.html"
                
                try:
                    arquivo = open(diretorio_servidor + arquivo_requisitado, "r")
                    resposta = arquivo.read()
                    arquivo.close()
                    
                    cabecalho = "HTTP/1.1 200 OK\r\n"

                    if arquivo_requisitado.endswith(".jpg") :
                        mime_type = "image/jpg"

                    elif(arquivo_requisitado.endswith(".css")):
                        mime_type = "text/css"

                    else:
                        mime_type = "text/html"

                    cabecalho += "Content=Type: " + str(mime_type) + "\r\n\r\n"
                
                except Exception as msg_erro:
                    print (msg_erro)
                    
                    cabecalho = "HTTP/1.1 404 Not Found\r\n\r\n"
                    resposta = """<html>
                          <body>
                            <center>
                             <h3>Error 404: File not found</h3>
                             <p>Servidor HTTP</p>
                            </center>
                          </body>
                        </html>"""

                mensagem_retorno = cabecalho + resposta
    
                conexao_cliente.send(bytes(mensagem_retorno, "UTF-8"))
                conexao_cliente.close()
            
            except Exception as msg_erro:
                print(msg_erro)
   
     
if __name__ == '__main__':
    """
        Inicia duas threads uma para cada metodo da classe Servidor
    """
    
    objServidor = Servidor()
    
    try:
        Thread(target=objServidor.MensagemTCP).start()
        Thread(target=objServidor.MensagemUDP).start()
        Thread(target=objServidor.MensagemHTTP).start()
   
    except Exception as msg:
        print(msg)
        