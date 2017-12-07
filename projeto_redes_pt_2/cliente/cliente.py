#!/usr/bin/env python

# cliente.py
from socket import *
import time, os, json

# # recebe no máximo 1024 bytes
# tm = s.recv(1024)

# s.close()

# print("O tempo que o servidor demorou foi %s" % tm.decode('ascii'))

def fazerConexao():
    try:
    	# cria um objeto socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # pega nome do host local
        clientHost = gethostname()
        clientPort = 9999
        # conexão no host pela porta
        clientSocket.connect((clientHost, clientPort))
        return clientSocket
    except:
        input("Conexão falhou. O servidor está rodando corretamente?")

def CabecalhoUI(nomeMenu, usuarioLogado = ""):
    print(nomeMenu.upper())
    if usuarioLogado != "":
        print("Usuário %s" %usuarioLogado)
    else:
        print("Usuário desconectou")
    print("Conectado")

def pegaString(textoComando):
    while True:
        stringUsuario = input("\n" + textoComando + "\n")

        if (stringUsuario != ""): break

    return stringUsuario

def pegaStringOp(textoComando):
    while True:
        escolhaUsuario = input(textoComando + "\n")
        if escolhaUsuario == "S" or escolhaUsuario == "N": break

    return escolhaUsuario

def LerInteiro(textoComando, valorMinimo, valorMaximo):
    while True:
        try:
            entradaUsuario = int(input(textoComando + "\n"))

            while (valorMinimo > entradaUsuario) or (entradaUsuario > valorMaximo):
                print("\n\nNúmero digitado deve estar entre %d e %d. ◄ ◄ ◄\n" %(valorMinimo, valorMaximo))
                entradaUsuario = int(input(textoComando + "\n"))

            break

        except ValueError:
            print("\n\nErro com entrada!\n")

    return entradaUsuario

##################################################
clientSocket = fazerConexao()

def ChamarServidor(solicitacao, clientSocket):
    clientSocket.send(solicitacao.encode("utf-8"))

def menuOp(clientSocket):
    CabecalhoUI("Menu Inicial")

    print("\n\n► Olá! Para começar, escolha uma opção:\n\n" +
          "1) Acessar Conta\n" +
          "2) Criar uma Conta\n" +
          "3) Sobre o CIn Drive")

    opcaoEscolhida = LerInteiro("\nDigite o número respectivo à sua escolha:", 1, 3)

    if opcaoEscolhida == 1:
        ChamarServidor("AcessarConta()", clientSocket)
        AcessarConta(clientSocket)

    elif opcaoEscolhida == 2:
        ChamarServidor("CriarConta()", clientSocket)
        CriarConta(clientSocket)

    else:
        Sobre(clientSocket)

def MenuPrincipal(nomeCliente, clientSocket):
    CabecalhoUI("Menu Principal", nomeCliente)

    print("\n\nAutenticação realizada com sucesso!\n\n" +
          "O que você deseja? \n\n" +
          "1) Meu armazenamento\n" +
          "2) Arquivos compartilhados com meu usuário")

    opcaoEscolhida = LerInteiro("\nDigite sua opção", 1, 2)

    if opcaoEscolhida == 1:
        ChamarServidor("meusArquivos()", clientSocket)
        meusArquivos(nomeCliente, clientSocket)

    else:
        ChamarServidor("compartilhadosComUsuario()", clientSocket)
        compartilhadosComUsuario(nomeCliente, clientSocket)

def Sobre(clientSocket):
    CabecalhoUI("Sobre")

    print("Projeto da cadeira Redes de Computadores - CIn UFPE. O objetivo é implementar um sistema que " +
          "sirva como um armazenador de arquivos, com download e upload, e autenticação de usuário.\n\n" +
          "Aluna:\n\n" +
          "  Carolina Maria de Paiva Melo\n\n")
    input("Aperte Enter para voltar!")
    menuOp(clientSocket)

def DownloadArquivo(nomeCliente, nomeArquivoEscolhido, clientSocket):
    CabecalhoUI("Download de Arquivo", nomeCliente)

    print("\n\nDeseja baixar o arquivo '%s'?" %nomeArquivoEscolhido)

    escolhaUsuario = pegaStringOp("\nS/N")

    if escolhaUsuario == "S":
        clientSocket.send(escolhaUsuario.encode("utf-8")) # ENVIA "S" OU "N"

        arquivoRequisitado = open("./Storage/Downloads/" + nomeArquivoEscolhido, "wb")

        bytesRecebidos = clientSocket.recv(1024)
        while bytesRecebidos:
            arquivoRequisitado.write(bytesRecebidos)
            bytesRecebidos = clientSocket.recv(1024)
        arquivoRequisitado.close()

        input("\nDownload completo! Vá a pasta Downloads.\n" +
              "Tecle Enter para voltar.")
    else: print("Cancelou download")

def CriarConta(clientSocket):
    CabecalhoUI("Criar Conta")
    #clientSocket = fazerConexao()

    print("\n\n► Para criar uma conta, informe seus dados abaixo.")

    while True:
        nomeUsuario = pegaString("Digite um nome de usuário:")

        while True:
            senhaUsuario = pegaString("Crie uma senha:")
            confirmacaoSenha = pegaString("Digite a mesma senha para confirmá-la:")

            if senhaUsuario != confirmacaoSenha:
                print("\nAs senhas digitadas são distintas. Tente cadastrá-la novamente.")

            else: break

        dictDadosAutenticacao = {nomeUsuario: senhaUsuario}

        # ENVIA DICIONARIO PARA SERVIDOR:
        dictDAJson = json.dumps(dictDadosAutenticacao)
        clientSocket.send(dictDAJson.encode("utf-8"))
        # ENVIADO - OK.

        # RECEBE INFORMAÇAO SE O USUARIO JA EXISTE:
        statusExistencia = clientSocket.recv(1024).decode("utf-8")
        # OK.

        if statusExistencia == "EXISTENTE":
            print("\nO nome de usuario já existe. Tente cadastrá-lo novamente.")

        elif statusExistencia == "INEXISTENTE": break

    # APENAS DEPOIS DE TER SAIDO DO LOOP, RECEBE INFORMAÇÃO SE O CADASTRO FOI FEITO OU NAO:
    statusCadastro = clientSocket.recv(1024).decode("utf-8")
    if statusCadastro == "SUCESSO":
        input("\n\nConta cadastrada com sucesso! Tecle 'enter' para acessar a tela de login.")

        ChamarServidor("AcessarConta()", clientSocket)
        AcessarConta(clientSocket)

    elif statusCadastro == "ERRO":
        print("\n\nErro de cadastro. Reinicialize o programa.")
    # OK.

def AcessarConta(clientSocket):
    CabecalhoUI("Acessar Conta")
    #clientSocket = fazerConexao()

    print("\n\nDados da conta: ")

    while True:
        nomeUsuario = pegaString("Usuário:")
        senhaUsuario = pegaString("Senha:")

        dictDadosAutenticacao = {nomeUsuario: senhaUsuario}

        # ENVIA DICIONARIO PARA SERVIDOR:
        dictDAJson = json.dumps(dictDadosAutenticacao)
        clientSocket.send(dictDAJson.encode("utf-8"))
        # ENVIADO - OK.

        # RECEBE INFORMAÇAO SE DADOS DO LOGIN ESTÃO CORRETOS OU NÃO:
        statusLogin = clientSocket.recv(1024).decode("utf-8")
        # OK.

        if statusLogin == "FALHA":
            print("\n\nUsuário ou senha incorretos. Digite novamente.\n")

        elif statusLogin == "LOGADO": break

    MenuPrincipal(nomeUsuario, clientSocket)

def EnumerarLista(lista, textoIntroducao, textoComando):
    print("\n\n► " + textoIntroducao + "\n")

    for x in range(len(lista)):
        print(str(x + 1) + ") " + lista[x])

    numeroEscolhido = LerInteiro("\n" + textoComando, 1, len(lista))
    numeroPosicaoLista = (numeroEscolhido - 1)
    nomeConteudoEscolhido = lista[numeroPosicaoLista]


    return nomeConteudoEscolhido, numeroPosicaoLista

def ExploradorDiretorio(diretorio):
    listaConteudoDir = (os.listdir("./" + diretorio))

    print("\n► Explorando o conteúdo do diretório local '%s'.\n" %diretorio.upper())

    for x in range(len(listaConteudoDir)):
        print(str(x + 1) + ") " + listaConteudoDir[x])

    return listaConteudoDir

def UploadArquivo(nomeCliente, nomeDiretorio, nomePastaDestino, clientSocket):
    CabecalhoUI("Upload de Arquivo", nomeCliente)

    listaConteudoDir = ExploradorDiretorio("Storage") # Explora o root, inicialmente.
    historicoAcessoPasta = ""

    while True:
        escolhaUsuario = LerInteiro("\nSelecione a pasta ou o arquivo pelo seu respectivo número:", 1, len(listaConteudoDir))
        nomeConteudoEscolhido = listaConteudoDir[escolhaUsuario - 1]

        if os.path.isdir("./Storage/" + historicoAcessoPasta + nomeConteudoEscolhido) == True:
            listaConteudoDir = ExploradorDiretorio("Storage/" + historicoAcessoPasta + nomeConteudoEscolhido)
            historicoAcessoPasta += (nomeConteudoEscolhido + "/")

        else:
            input("\nDeseja fazer o upload do arquivo '%s' para a pasta '%s'?" %(nomeConteudoEscolhido, nomePastaDestino))
            break

    nomeDirCompleto = nomeDiretorio + "/" + nomePastaDestino
    clientSocket.send(nomeDirCompleto.encode("utf-8"))
    time.sleep(1)
    clientSocket.send(nomeConteudoEscolhido.encode("utf-8"))

    arquivoEnvio = open("./Storage/" + historicoAcessoPasta + nomeConteudoEscolhido, "rb")

    arquivoPronto = arquivoEnvio.read(1024)
    while arquivoPronto:
        clientSocket.send(arquivoPronto)
        arquivoPronto = arquivoEnvio.read(1024)

    arquivoEnvio.close()
    #clientSocket.close()

    input("\nUpload do arquivo '%s' feito com sucesso! Pressione 'enter' para retornar ao Menu Principal." %nomeConteudoEscolhido)

    #MenuPrincipal(nomeCliente)

def CompartilharConteudo(nomeUsuario, nomeDiretorioRespectivo, nomeConteudoEscolhido, clientSocket):
    CabecalhoUI("Compartilhar Conteúdo", nomeUsuario)

    nomeDiretorioRespectivo += "/"

    # RECEBE LISTA DE USUÁRIOS CADASTRADOS E REMOVE DESTA LISTA O NOME DO USUÁRIO LOGADO
    listaUsuariosCadastrados_JS = clientSocket.recv(1024).decode("utf-8")
    listaUsuariosCadastrados = json.loads(listaUsuariosCadastrados_JS)
    listaUsuariosCadastrados.remove(nomeUsuario)
    # OK.

    nomeUsuarioACompartilhar, numeroPosicaoLista = EnumerarLista(listaUsuariosCadastrados,
                                           "Com qual usuário você gostaria de compartilhar o conteúdo '%s'?" %nomeConteudoEscolhido,
                                           "Selecione o nome do usuário pelo seu número correspondente:")

    dadosCompartilhamento = []
    dadosCompartilhamento.append(nomeUsuarioACompartilhar)
    dadosCompartilhamento.append(nomeConteudoEscolhido)
    dadosCompartilhamento.append(nomeDiretorioRespectivo)

    dadosCompartilhamento_JS = json.dumps(dadosCompartilhamento)
    clientSocket.send(dadosCompartilhamento_JS.encode("utf-8"))

    input("\nConteúdo '%s' foi compartilhado com sucesso com o usuário %s! " %(nomeConteudoEscolhido, nomeUsuarioACompartilhar) +
          "Tecle 'enter' para voltar ao Meu Drive.")

def CriarPasta(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket):
    CabecalhoUI("Criar Pasta", nomeUsuario)

    nomeNovaPasta = pegaString("► Digite o nome da nova pasta que deseja criar em '%s'." %nomeConteudoEscolhido)
    print(nomeDiretorio)
    print(nomeConteudoEscolhido)
    nomeDirCompleto = nomeDiretorio + "/" + nomeConteudoEscolhido

    clientSocket.send(nomeDirCompleto.encode("utf-8"))
    time.sleep(0.3)
    clientSocket.send(nomeNovaPasta.encode("utf-8"))

    input("\nPasta '%s' criada com sucesso! Pressione 'enter' para voltar ao Meu Drive." %nomeNovaPasta)

def TratamentoConteudo(nomeUsuario, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket):
    if tipoConteudo == "PASTA":
        print("\n\nO que você vai fazer com a pasta '%s'?\n\n" %nomeConteudoEscolhido +
             "1) Visualizar\n" +
             "2) Mandar arquivo\n" +
             "3) Criar pasta\n" +
             "4) Compartilhar")

        escolhaUsuario = LerInteiro("\nDigite o número referente à sua opção:", 1, 4)
        clientSocket.send(str(escolhaUsuario).encode("utf-8"))

        if escolhaUsuario == 1:
            pass

        elif escolhaUsuario == 2:
            UploadArquivo(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUsuario, clientSocket)

        elif escolhaUsuario == 3:
            CriarPasta(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUsuario, clientSocket)

        elif escolhaUsuario == 4:
            CompartilharConteudo(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUsuario, clientSocket)

    elif tipoConteudo == "ARQUIVO":
        print("\n\nO que você vai fazer com o arquivo '%s'?\n\n" %nomeConteudoEscolhido +
              "1) Baixar/Download\n" +
              "2) Compartilhar")

        escolhaUsuario = LerInteiro("\nDigite o número da sua opção:", 1, 2)
        clientSocket.send(str(escolhaUsuario).encode("utf-8"))

        if escolhaUsuario == 1:
            DownloadArquivo(nomeUsuario, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUsuario, clientSocket)

        if escolhaUsuario == 2:
            CompartilharConteudo(nomeUsuario, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            ChamarServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUsuario, clientSocket)

def meusArquivos(nomeUsuario, clientSocket):

    CabecalhoUI("Meu Drive", nomeUsuario)
    #clientSocket = fazerConexao()

    clientSocket.send(nomeUsuario.encode("utf-8"))

    while True:
        nomeDiretorio = clientSocket.recv(1024).decode("utf-8")
        listaConteudoDir_JS = clientSocket.recv(1024).decode("utf-8")
        listaConteudoDir = json.loads(listaConteudoDir_JS)

        nomeConteudoEscolhido, numeroPosicaoLista = EnumerarLista(listaConteudoDir,
                                                                  "Explorando o seu diretório online '%s':" %nomeDiretorio.upper(),
                                                                  "Selecione o conteúdo pelo seu respectivo número:")

        clientSocket.send(nomeConteudoEscolhido.encode("utf-8"))
        tipoConteudo = clientSocket.recv(1024).decode("utf-8")

        TratamentoConteudo(nomeUsuario, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket)

def compartilhadosComUsuario(nomeUsuario, clientSocket):

    CabecalhoUI("Compartilhados Comigo", nomeUsuario)
    #clientSocket = fazerConexao()

    clientSocket.send(nomeUsuario.encode("utf-8"))

    dadosCompartIndividual_JS = clientSocket.recv(1024).decode("utf-8")
    dadosCompartIndividual = json.loads(dadosCompartIndividual_JS)

    listaConteudoCompartilhado = dadosCompartIndividual[0]
    caminhoReferenteAoConteudo = dadosCompartIndividual[1]
    #nomeProprietario = caminhoReferenteAoConteudo[0].split("/")[0]

    nomeConteudoEscolhido, numeroPosicaoLista = EnumerarLista(listaConteudoCompartilhado,
                                                              "Conteúdo(s) compartilhado(s) com você:",
                                                              "Selecione o conteúdo pelo seu respectivo número:")

    nomeDirCompleto = caminhoReferenteAoConteudo[numeroPosicaoLista] + listaConteudoCompartilhado[numeroPosicaoLista]

    clientSocket.send(nomeDirCompleto.encode("utf-8"))
    tipoConteudo = clientSocket.recv(1024).decode("utf-8")

    if tipoConteudo == "ARQUIVO":
        nomeDiretorio = caminhoReferenteAoConteudo[numeroPosicaoLista]

        TratamentoConteudo(nomeUsuario, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
    else:
        while True:
            nomeDiretorio = clientSocket.recv(1024).decode("utf-8") + "/"
            listaConteudoDir_JS = clientSocket.recv(1024).decode("utf-8")
            listaConteudoDir = json.loads(listaConteudoDir_JS)

            nomeConteudoEscolhido, numeroPosicaoLista = EnumerarLista(listaConteudoDir,
                                                                          "Explorando o diretório online compartilhado com você:",
                                                                          "Selecione o conteúdo pelo seu respectivo número:")

            clientSocket.send(nomeConteudoEscolhido.encode("utf-8"))
            tipoConteudo = clientSocket.recv(1024).decode("utf-8")

            TratamentoConteudo(nomeUsuario, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket)

menuOp(clientSocket)
