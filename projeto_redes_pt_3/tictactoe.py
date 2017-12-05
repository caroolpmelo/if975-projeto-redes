class velha():
    def __init__(self):
        self.tabuleiro = ['-'] + list(range(1, 10))
        self.jogadores = ['X', 'O']
        self.vencedor = None
        self.turno_atual = 0
        self.combinacoes = [
           (1, 2, 3),
           (4, 5, 6),
           (7, 8, 9),
           (1, 4, 7),
           (2, 5, 8),
           (3, 6, 9),
           (1, 5, 9),
           (3, 5, 7),
        ]

    @staticmethod
    def desenhar(lista):
        print ()
        print ('', lista[7], lista[8], lista[9], '\n', 
        lista[4], lista[5], lista[6], '\n',
        lista[1], lista[2], lista[3])
        print ()
        

    def turno(self):
        if self.turno_atual%2 == 0:
            return 'X'
        else:
            return 'O'

    def jogada(self, casa):
        try:
            if int(casa) in self.tabuleiro:
                self.tabuleiro[int(casa)] = self.turno()
                self.turno_atual += 1
                #Jogada valida
                #Tabuleiro atualizado
                return True
            else:
                #Numero invalido
                return False
        except ValueError:
            #Valor invalido
            return False



    def acabou(self):
        for a, b, c in self.combinacoes:
            if self.tabuleiro[a] == self.tabuleiro[b] == self.tabuleiro[c]:
                self.turno_atual += 1
                self.vencedor = self.turno()
                #Um dos jogadores venceu
                return True
            
        if self.turno_atual == 9:
            print("Empate\n")
            return True
        
        else:
            #Jogo ainda nao acabou
            return False

        
