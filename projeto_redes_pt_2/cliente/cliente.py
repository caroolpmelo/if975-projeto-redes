#!/usr/bin/env python

# cliente.py
from socket import *
import time, os, json

# # recebe no máximo 1024 bytes
# tm = s.recv(1024)

# s.close()

# print("O tempo que o servidor demorou foi %s" % tm.decode('ascii'))

def iniciaConexao():
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
        input("Conexão falhou")

def menuOp(clientSocket):
    infos("Menu de Opções")
    print("\nQual opção você deseja? \n" +
          "1 - Acessar Conta \n" +
          "2 - Criar uma Conta \n" +
          "3 - Sobre a aplicação")

    opSelecionada = pegaInteiro("\nDigite o número respectivo à sua escolha:", 1, 3)

    if opSelecionada == 1:
        chamaServidor("AcessarConta()", clientSocket)
        AcessarConta(clientSocket)

    elif opSelecionada == 2:
        chamaServidor("criarConta()", clientSocket)
        criarConta(clientSocket)

    else:
        about(clientSocket)

def menuOpLogado(nomeCliente, clientSocket):
    infos("Menu Principal", nomeCliente)

    print("\nAutenticação realizada com sucesso!\n" +
          "O que você deseja? \n" +
          "1) Meu armazenamento\n" +
          "2) Arquivos compartilhados com meu usuário")

    opSelecionada = pegaInteiro("\nDigite sua opção", 1, 2)

    if opSelecionada == 1:
        chamaServidor("meusArquivos()", clientSocket)
        meusArquivos(nomeCliente, clientSocket)

    else:
        chamaServidor("compartilhadosComUsuario()", clientSocket)
        compartilhadosComUsuario(nomeCliente, clientSocket)

def pegaString(inputComando):
    while True:
        stringUser = input("\n" + inputComando + "\n")

        if (stringUser != ""): break

    return stringUser

def pegaStringOp(inputComando):
    while True:
        opUser = input(inputComando + "\n")
        if opUser == "S" or opUser == "N": break

    return opUser

def pegaInteiro(inputComando, minValue, maxValue):
    while True:
        try:
            inputUser = int(input(inputComando + "\n"))

            while (minValue > inputUser) or (inputUser > maxValue):
                print("\nNúmero digitado é incorreto!")
                inputUser = int(input(inputComando + "\n"))

            break

        except ValueError:
            print("\nErro com entrada!\n")

    return inputUser

def infos(nomMenu, userEntrou = ""):
    print(nomMenu.upper())
    if userEntrou != "":
        print("Usuário %s" %userEntrou)
    else:
        print("Desconectou")
    print("Conectado")

def about(clientSocket):
    infos("Sobre a aplicação: ")

    print("Projeto da cadeira Redes de Computadores - CIn UFPE, com objetivo de implementar um sistema " +
          "de armazenamento e compartilhamento de arquivos." +
          "\nAluna:\n" +
          "  Carolina Maria de Paiva Melo\n")
    menuOp(clientSocket)

clientSocket = iniciaConexao()

def chamaServidor(solicitacao, clientSocket):
    clientSocket.send(solicitacao.encode("utf-8"))

def DownloadArquivo(nomeCliente, nomeArquivoSelecionado, clientSocket):
    infos("Download de Arquivo", nomeCliente)

    print("\nDeseja baixar o arquivo '%s'?" %nomeArquivoSelecionado)

    opUser = pegaStringOp("\nS/N")

    if opUser == "S":
        clientSocket.send(opUser.encode("utf-8")) # ENVIA "S" OU "N"

        arquivoRequisitado = open("./Storage/Downloads/" + nomeArquivoSelecionado, "wb")

        bytesRecebidos = clientSocket.recv(1024)
        while bytesRecebidos:
            arquivoRequisitado.write(bytesRecebidos)
            bytesRecebidos = clientSocket.recv(1024)
        arquivoRequisitado.close()

        input("\nDownload completo! Arquivo(s) baixado na pasta Downloads.\n" +
              "Tecle Enter")
    else: print("Cancelou download")

def criarConta(clientSocket):
    infos("Criar Conta")
    #clientSocket = iniciaConexao()

    print("\nDigite seus dados: ")

    while True:
        nomeUser = pegaString("Digite um nome de usuário:")
        while True:
            senhaUser = pegaString("Crie uma senha:")
            else: break

        dictDadosAutenticacao = {nomeUser: senhaUser}

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
        input("\nConta cadastrada com sucesso! Tecle 'enter' para acessar a tela de login.")

        chamaServidor("AcessarConta()", clientSocket)
        AcessarConta(clientSocket)

    elif statusCadastro == "ERRO":
        print("\nErro de cadastro. Reinicialize o programa.")
    # OK.

def AcessarConta(clientSocket):
    infos("Acessar Conta")
    #clientSocket = iniciaConexao()

    print("\nDados da conta: ")

    while True:
        nomeUser = pegaString("Usuário:")
        senhaUser = pegaString("Senha:")

        dictDadosAutenticacao = {nomeUser: senhaUser}

        dictDAJson = json.dumps(dictDadosAutenticacao)
        clientSocket.send(dictDAJson.encode("utf-8"))

        # dados corretos ou incorretos:
        statusLogin = clientSocket.recv(1024).decode("utf-8")

        if statusLogin == "FALHA":
            print("\nUsuário ou senha incorretos. Digite novamente.\n")

        elif statusLogin == "LOGADO": break

    menuOpLogado(nomeUser, clientSocket)

def organizaList(lista, intro, inputComando):
    print("\n" + intro + "\n")

    for x in range(len(lista)):
        print(str(x + 1) + ") " + lista[x])

    numeroEscolhido = pegaInteiro("\n" + inputComando, 1, len(lista))
    numeroPosicaoLista = (numeroEscolhido - 1)
    nomeConteudoEscolhido = lista[numeroPosicaoLista]


    return nomeConteudoEscolhido, numeroPosicaoLista

def verArquivosPasta(diretorio):
    listarArquivosPasta = (os.listdir("./" + diretorio))

    print("\nVendo conteúdo do diretório '%s'.\n" %diretorio.upper())

    for x in range(len(listarArquivosPasta)):
        print(str(x + 1) + ") " + listarArquivosPasta[x])

    return listarArquivosPasta

def UploadArquivo(nomeCliente, nomeDiretorio, nomePastaDestino, clientSocket):
    infos("Upload de Arquivo", nomeCliente)

    listarArquivosPasta = verArquivosPasta("Storage")
    historicoAcess = ""

    while True:
        opUser = pegaInteiro("\nSelecione documento pelo seu número:", 1, len(listarArquivosPasta))
        nomeConteudoEscolhido = listarArquivosPasta[opUser - 1]

        if os.path.isdir("./Storage/" + historicoAcess + nomeConteudoEscolhido) == True:
            listarArquivosPasta = verArquivosPasta("Storage/" + historicoAcess + nomeConteudoEscolhido)
            historicoAcess += (nomeConteudoEscolhido + "/")

        else:
            input("\nDeseja fazer o upload do arquivo '%s' para a pasta '%s'?" %(nomeConteudoEscolhido, nomePastaDestino))
            break

    nomeDirCompleto = nomeDiretorio + "/" + nomePastaDestino
    clientSocket.send(nomeDirCompleto.encode("utf-8"))
    time.sleep(1)
    clientSocket.send(nomeConteudoEscolhido.encode("utf-8"))

    arquivoEnvio = open("./Storage/" + historicoAcess + nomeConteudoEscolhido, "rb")

    arquivoPronto = arquivoEnvio.read(1024)
    while arquivoPronto:
        clientSocket.send(arquivoPronto)
        arquivoPronto = arquivoEnvio.read(1024)

    arquivoEnvio.close()
    #clientSocket.close()

    input("\nUpload do arquivo '%s' feito com sucesso! Pressione 'enter' para retornar ao Menu Principal." %nomeConteudoEscolhido)

    #menuOpLogado(nomeCliente)

def compartilharArquivo(nomeUser, nomeDiretorioRespectivo, nomeConteudoEscolhido, clientSocket):
    infos("Compartilhar Conteúdo", nomeUser)

    nomeDiretorioRespectivo += "/"

    # RECEBE LISTA DE USUÁRIOS CADASTRADOS E REMOVE DESTA LISTA O NOME DO USUÁRIO LOGADO
    listaUsuariosCadastrados_JS = clientSocket.recv(1024).decode("utf-8")
    listaUsuariosCadastrados = json.loads(listaUsuariosCadastrados_JS)
    listaUsuariosCadastrados.remove(nomeUser)
    # OK.

    nomeUserACompartilhar, numeroPosicaoLista = organizaList(listaUsuariosCadastrados,
                                           "Com qual usuário você gostaria de compartilhar o conteúdo '%s'?" %nomeConteudoEscolhido,
                                           "Selecione o nome do usuário pelo seu número correspondente:")

    dadosCompartilhamento = []
    dadosCompartilhamento.append(nomeUserACompartilhar)
    dadosCompartilhamento.append(nomeConteudoEscolhido)
    dadosCompartilhamento.append(nomeDiretorioRespectivo)

    dadosCompartilhamento_JS = json.dumps(dadosCompartilhamento)
    clientSocket.send(dadosCompartilhamento_JS.encode("utf-8"))

    input("\nConteúdo '%s' compartilhado com sucesso! " %(nomeConteudoEscolhido) +
          "Aperte Enter")

def criarPasta(nomeUser, nomeDiretorio, nomeConteudoEscolhido, clientSocket):
    infos("Criar Pasta", nomeUser)

    nomeNovaPasta = pegaString("► Digite o nome da nova pasta que deseja criar em '%s'." %nomeConteudoEscolhido)
    print(nomeDiretorio)
    print(nomeConteudoEscolhido)
    nomeDirCompleto = nomeDiretorio + "/" + nomeConteudoEscolhido

    clientSocket.send(nomeDirCompleto.encode("utf-8"))
    time.sleep(0.3)
    clientSocket.send(nomeNovaPasta.encode("utf-8"))

    input("\nPasta '%s' criada com sucesso! Tecle Enter" %nomeNovaPasta)

def conteudoOp(nomeUser, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket):
    if tipoConteudo == "PASTA":
        print("\nO que você vai fazer com a pasta '%s'?\n" %nomeConteudoEscolhido +
             "1) Visualizar\n" +
             "2) Mandar arquivo\n" +
             "3) Criar pasta\n" +
             "4) Compartilhar")

        opUser = pegaInteiro("\nDigite o número referente à sua opção:", 1, 4)
        clientSocket.send(str(opUser).encode("utf-8"))

        if opUser == 1:
            pass

        elif opUser == 2:
            UploadArquivo(nomeUser, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            chamaServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUser, clientSocket)

        elif opUser == 3:
            criarPasta(nomeUser, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            chamaServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUser, clientSocket)

        elif opUser == 4:
            compartilharArquivo(nomeUser, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            chamaServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUser, clientSocket)

    elif tipoConteudo == "ARQUIVO":
        print("\nO que você vai fazer com o arquivo '%s'?\n" %nomeConteudoEscolhido +
              "1) Baixar/Download\n" +
              "2) Compartilhar")

        opUser = pegaInteiro("\nDigite o número da sua opção:", 1, 2)
        clientSocket.send(str(opUser).encode("utf-8"))

        if opUser == 1:
            DownloadArquivo(nomeUser, nomeConteudoEscolhido, clientSocket)
            chamaServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUser, clientSocket)

        if opUser == 2:
            compartilharArquivo(nomeUser, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
            chamaServidor("meusArquivos()", clientSocket)
            meusArquivos(nomeUser, clientSocket)

def meusArquivos(nomeUser, clientSocket):

    infos("Meus Arquivos", nomeUser)
    #clientSocket = iniciaConexao()

    clientSocket.send(nomeUser.encode("utf-8"))

    while True:
        nomeDiretorio = clientSocket.recv(1024).decode("utf-8")
        listarArquivosPasta_JS = clientSocket.recv(1024).decode("utf-8")
        listarArquivosPasta = json.loads(listarArquivosPasta_JS)

        nomeConteudoEscolhido, numeroPosicaoLista = organizaList(listarArquivosPasta,
                                                                  "Explorando o seu diretório online '%s':" %nomeDiretorio.upper(),
                                                                  "Selecione o conteúdo pelo seu respectivo número:")

        clientSocket.send(nomeConteudoEscolhido.encode("utf-8"))
        tipoConteudo = clientSocket.recv(1024).decode("utf-8")

        conteudoOp(nomeUser, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket)

def compartilhadosComUsuario(nomeUser, clientSocket):

    infos("Compartilhados Comigo", nomeUser)
    #clientSocket = iniciaConexao()

    clientSocket.send(nomeUser.encode("utf-8"))

    dadosCompartIndividual_JS = clientSocket.recv(1024).decode("utf-8")
    dadosCompartIndividual = json.loads(dadosCompartIndividual_JS)

    listaConteudoCompartilhado = dadosCompartIndividual[0]
    caminhoReferenteAoConteudo = dadosCompartIndividual[1]
    #nomeProprietario = caminhoReferenteAoConteudo[0].split("/")[0]

    nomeConteudoEscolhido, numeroPosicaoLista = organizaList(listaConteudoCompartilhado,
                                                              "Conteúdo(s) compartilhado(s) com você:",
                                                              "Selecione o conteúdo pelo seu respectivo número:")

    nomeDirCompleto = caminhoReferenteAoConteudo[numeroPosicaoLista] + listaConteudoCompartilhado[numeroPosicaoLista]

    clientSocket.send(nomeDirCompleto.encode("utf-8"))
    tipoConteudo = clientSocket.recv(1024).decode("utf-8")

    if tipoConteudo == "ARQUIVO":
        nomeDiretorio = caminhoReferenteAoConteudo[numeroPosicaoLista]

        conteudoOp(nomeUser, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket)
    else:
        while True:
            nomeDiretorio = clientSocket.recv(1024).decode("utf-8") + "/"
            listarArquivosPasta_JS = clientSocket.recv(1024).decode("utf-8")
            listarArquivosPasta = json.loads(listarArquivosPasta_JS)

            nomeConteudoEscolhido, numeroPosicaoLista = organizaList(listarArquivosPasta,
                                                                          "Explorando o diretório online compartilhado com você:",
                                                                          "Selecione o conteúdo pelo seu respectivo número:")

            clientSocket.send(nomeConteudoEscolhido.encode("utf-8"))
            tipoConteudo = clientSocket.recv(1024).decode("utf-8")

            conteudoOp(nomeUser, tipoConteudo, nomeDiretorio, nomeConteudoEscolhido, clientSocket)

menuOp(clientSocket)
