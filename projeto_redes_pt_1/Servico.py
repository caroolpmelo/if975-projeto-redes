from TcpCliente import TcpCliente
from UdpCliente import UdpCliente
from HttpCliente import HttpCliente


"""
    Para rodar a aplicacao a classe Servidor.py precisa estar rodoando
    Funcao da aplicacao: 
      Ler de um arquivo de texto do metodo de transmissao que vai ser usado - (tcp, udp, http)
      Inicia a classe cliente do protocolo escolhido
      Envia a mensagem para o servidor 
      Recebe e imprime a resposta
"""

def main():

    protocolo = lerProtocolo()
    iniciaCliente(protocolo)

def lerProtocolo():
    """
        Abre o arquivo e le a primeira linha, tratando a string e retornando-a
    """
    caminho_arquivo = "metodo_envio.txt"
    arquivo = open(caminho_arquivo, "r")
    protocolo_envio = arquivo.readline().strip().lower()
    print("protocolo escolhido: " + protocolo_envio)
    return  protocolo_envio

def iniciaCliente(protocolo):
    """
        A depender do protocolo escolhido, inicia o cliente correspondente
    """
    if protocolo == "tcp":
        
        cliente = TcpCliente()
        mensagem = input("Digite aqui >>> ")
        retorno = cliente.enviar_mensagem(mensagem)
        print(retorno)

    elif protocolo == "udp":
        cliente = UdpCliente()
        mensagem = input("Digite aqui >>> ")
        retorno = cliente.enviar_mensagem(mensagem)
        print(retorno)

    elif protocolo == "http":
        """
            AQUI ESTA O PROBLEMA DO HTTP 
        """
        cliente = HttpCliente()
        url = input("digite a url: (Ex: http://localhost:20200/index.html)\n")        
        retorno = cliente.receber_pagina(url)
        print(retorno)

    else:
        print("protocolo não suportado") 


if __name__ == '__main__':
    main()