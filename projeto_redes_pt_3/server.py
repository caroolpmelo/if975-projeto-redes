#SERVER
import socket
import time
from tictactoe import *

class Servidor:
    def __init__(self):
        #Criacao do socket
        self.jogo = velha()
        self.enderecos = []
        self.miscdata = []
        self.turnos = {'X': '', 'O':''}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 1337))
        #Tempo de timeout para perdas de conexao
        self.sock.settimeout(60)


    def enviar_ambos(self, data):
        '''
        Envia dados para ambos os jogadores
        Se possivel
        '''
        
        self.sock.sendto((data.encode()), (self.enderecos[0]))
        try:
            self.sock.sendto((data.encode()), (self.enderecos[1]))
        except IndexError:
            pass


    def enviar(self, data, addr):
        '''
        Enviar para endereco especifico
        '''
        
        self.sock.sendto((data.encode()), addr)


    def enviar_tabuleiro(self):
        '''
        Converte o tabuleiro para uma string
        e envia para ambos
        '''
        
        data = (', '.join((str(x) for x in self.jogo.tabuleiro)))
        self.enviar_ambos(data)


    def esperar_conn(self):
        '''
        Esperar por uma tentativa
        de conexao e guardar o endereco
        '''
    
        data, addr = self.sock.recvfrom(1024)
        (self.enderecos).append(addr)
        return data

        
    def iniciar(self):
        
        print ("Iniciando Servidor")
        print ("Esperando conexoes\n")

        while len(self.enderecos) != 2 :
            #Esperando duas conexoes
            nome = self.esperar_conn()
            self.miscdata.append(nome.decode())
        msg = "Jogadores conectados: " + str(self.miscdata)
        print (msg)
        self.enviar_ambos(msg)


        self.turnos['X'] = self.enderecos[0]
        self.turnos['O'] = self.enderecos[1]
       

        self.enviar_tabuleiro()

        #Loop do jogo
        while not self.jogo.acabou():
            try:
                if self.jogo.turno_atual % 2 == 0:
                    #Turno do X
                    self.enviar('Seu turno', self.turnos['X'])
                    self.enviar('Turno do oponente', self.turnos['O'])

                    jogada, addr = self.sock.recvfrom(1024)
                    self.jogo.jogada(jogada.decode())
                    self.enviar_tabuleiro()
                    
                else:
                    #Turno do O
                    self.enviar('Seu turno', self.turnos['O'])
                    self.enviar('Turno do oponente', self.turnos['X'])
                    
                    jogada, addr = self.sock.recvfrom(1024)
                    self.jogo.jogada(jogada.decode())
                    self.enviar_tabuleiro()

            except ConnectionResetError:
                #Um dos jogadores foi desconectado
                self.enviar_ambos('999')
                print ("Erro de conexao")
                          
        vencedor = self.jogo.vencedor

        if vencedor == 'X':
            #X venceu
            self.enviar_ambos('101')
        elif vencedor == 'O':
            #O venceu
            self.enviar_ambos('201')
        else:
            #Empate
            self.enviar_ambos('000')


if __name__ == '__main__':
    try:
        a = Servidor()
        a.iniciar()

    except socket.timeout:
        print ("Time out - socket encerrado")
