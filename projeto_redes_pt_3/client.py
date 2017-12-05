#CLIENT
import socket
from tictactoe import *

class Client:

    def __init__(self):
        self.ip = input("Digite o IP do servidor\n")
        self.porta = input("Digite uma porta\n")
        self.endereco = (self.ip, int(self.porta))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(60)
        
    def fazer_jogada(self):
        data = input("Faca a sua jogada: ")
        self.sock.sendto(data.encode(), (self.endereco))
 
    def receber(self):
        data, addr = self.sock.recvfrom(1024)
        return (data)

    def construir_tabuleiro(self, tabstr):
        '''
        Converte um tabuleiro em formato de string
        para uma lista e o imprime na tela
        '''
        
        if len(tabstr) == 28:
            lista = tabstr.split(",")
            velha.desenhar(lista)
        else:
            print (tabstr)

    def iniciar(self):

        nome = input("Nome do usuario: ")
        self.sock.sendto(nome.encode(), self.endereco)
        print ("Conexao com o servidor em andamento...")

        jogadores = self.receber()
        print (jogadores.decode())

        data = self.receber()
        self.construir_tabuleiro(data.decode())

        while True:

            ordem = self.receber()
            
            if ordem:
                if ordem.decode() == '000':
                    print ("Empate!")
                    break

                elif ordem.decode() == '101':
                    print ("Jogador X venceu!")
                    break

                elif ordem.decode() == '201':
                    print ("Jogador O venceu!")
                    break
                
                elif ordem.decode() == '999':
                    print ("Conexao perdida com um dos jogadores")
                    break

            self.construir_tabuleiro(ordem.decode())

            if str(ordem.decode()) == "Turno do oponente":
                #Esperar
                tab = self.receber()
                self.construir_tabuleiro(tab.decode())

            if str(ordem.decode()) == "Seu turno":
                #Jogar
                self.fazer_jogada()
                tab = self.receber()
                self.construir_tabuleiro(tab.decode())
                

if __name__ == '__main__':
    try:
        cliente = Client()
        cliente.iniciar()
    
    except socket.timeout:
        print ("Time out - socket encerrado")


    
        
    

