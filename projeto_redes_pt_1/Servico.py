import os
from TcpCliente import TcpCliente
from UdpCliente import UdpCliente
from HttpCliente import HttpCliente

"""
    Para rodar a aplicacao a classe Servidor.py precisa estar rodando
    Funcao da aplicacao:
      O usuario escolhe o metodo de transmissao que vai ser usado - (tcp, udp, http)
      Inicia a classe cliente do protocolo escolhido
      Envia a mensagem para o servidor
      Recebe e imprime a resposta
"""

def main():

    while True:
      os.system('cls' if os.name == 'nt' else 'clear')
      protocolo = lerProtocolo()
      print("\nSERVICO ECHO: Protocolo " + protocolo)
      iniciaCliente(protocolo)

      escolha = input("\nDeseja enviar outra mensagem? (S/N)\n")
      if escolha.lower() == "n":
          break


def lerProtocolo():
    """
        recebe a entrada do usuario de qual protocolo sera usado
        retorna uma string com protocolo escolhido
    """

    estado = ""

    while True:
        escolha = input("Qual protocolo usar?\n1. TCP\n2. UDP\n3. HTTP\n\n" + estado +"> ")

        if escolha == "1":
            protocolo = "tcp"
            break

        elif escolha == "2":
            protocolo = "udp"
            break

        elif escolha == "3":
            protocolo = "http"
            break

        else:
            estado = "protocolo nao suportado escolha novamente\n\n"
            os.system('cls' if os.name == 'nt' else 'clear')

    return protocolo  


def iniciaCliente(protocolo):
    """
        A depender do protocolo escolhido, inicia o cliente correspondente
    """

    if protocolo == "tcp":
        
        cliente = TcpCliente()
        mensagem = input("Digite uma mensagem >>> ")
        retorno = cliente.enviar_mensagem(mensagem)
        print(retorno)

    elif protocolo == "udp":
        cliente = UdpCliente()
        mensagem = input("Digite uma mensagem >>> ")
        retorno = cliente.enviar_mensagem(mensagem)
        print(retorno)

    elif protocolo == "http":

        cliente = HttpCliente()
        url = input("digite a url do servidor: Ex: http://localhost:20200/index.html\n")        
        retorno = cliente.receber_pagina(url)
        print(retorno)

    else:
        print("protocolo não suportado") 


if __name__ == '__main__':
    main()