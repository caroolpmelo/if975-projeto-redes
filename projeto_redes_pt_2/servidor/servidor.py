#!/usr/bin/env python

# servidor.py
from socket import *
import time, os, json

# cria um objeto socket
serverSocket = socket(AF_INET, SOCK_STREAM)
# pega nome do host local
serverHost = gethostname()
serverPort = 9999
# liga host à porta
serverSocket.bind((serverHost, serverPort))
print('Servidor aguardando conexão...')
# até 25 requests na fila
serverSocket.listen(25)
# estabelece conexão
clientSocket,addr = serverSocket.accept()
print("O servidor conectou-se a %s" % str(addr))

### Métodos:

def statusCliente(status):
	print(status.upper())

def escutarCliente():
    while True:
        requisicaoCliente = clientSocket.recv(1024).decode("utf-8")
        statusCliente("Solicitação: %s" %requisicaoCliente)

        if requisicaoCliente == "acessarConta()":
        	acessarConta()
        elif requisicaoCliente == "meusArquivos()":
            meusArquivos()
        elif requisicaoCliente == "compartilhadosComUsuario()":
            compartilhadosComUsuario()
        elif requisicaoCliente == "criarConta()":
            criarConta()
        elif requisicaoCliente == "Encerrar": break
    clientSocket.close()

def criarConta():
    arquivoSegurancaLeitura = open("./jsons/Seguranca.json", "rb")
    leituraString = arquivoSegurancaLeitura.readline()
    leituraStringDecode = leituraString.decode() # PRECISA DECODAR PRA QUE A BIBLIOTECA JSON CONSIGA LER
    dictDadosUsuario = json.loads(leituraStringDecode)
    arquivoSegurancaLeitura.close()

    arquivoPermissoesLeitura = open("./jsons/Permissoes.json", "rb")
    arquivoPermissoesLeitura_STRING = arquivoPermissoesLeitura.readline()
    arquivoPermissoesLeitura_DECODE = arquivoPermissoesLeitura_STRING.decode()
    dictPermissoesUsuario = json.loads(arquivoPermissoesLeitura_DECODE)
    arquivoPermissoesLeitura.close()

    while True:
        dictDadosAutenticacao_JS = clientSocket.recv(1024).decode("utf-8")
        dictDadosAutenticacao = json.loads(dictDadosAutenticacao_JS)

        for x in dictDadosAutenticacao: # COLETA APENAS O NOME DO USUARIO QUE ESTA NO DICIONARIO
            nomeUser = x

        if nomeUser in dictDadosUsuario:
            statusExistencia = "EXISTENTE"
            clientSocket.send(statusExistencia.encode("utf-8"))

        else: break

    try:
        statusExistencia = "INEXISTENTE" # TEM COMO ENVIAR UM BOOL AO INVÉS DE STR?
        clientSocket.send(statusExistencia.encode("utf-8"))

        arquivoSegurancaEscrita = open("./jsons/Seguranca.json", "wb")
        dictDadosUsuario.update(dictDadosAutenticacao)
        dictAtualizado = json.dumps(dictDadosUsuario, ensure_ascii = False)
        arquivoSegurancaEscrita.write(dictAtualizado.encode())
        arquivoSegurancaEscrita.close()

        pastasOrigens = ["Documentos", "Imagens", "Músicas", "Atividades", "Quaisquer"]

        for nomePasta in pastasOrigens:
            pasta = ""
            pasta += nomeUser + "/" + nomePasta

            os.makedirs("./users/" + pasta)

        arquivoPermissoesEscrita = open("./jsons/Permissoes.json", "wb")
        dictConteudoPermitido = {nomeUser : [[], []]}
        dictPermissoesUsuario.update(dictConteudoPermitido)
        dictConteudoPermitido_JS = json.dumps(dictPermissoesUsuario, ensure_ascii = False)
        arquivoPermissoesEscrita.write(dictConteudoPermitido_JS.encode())
        arquivoPermissoesEscrita.close()

        statusCliente("Novo usuário '%s' cadastrado" %nomeUser)
        statusCadastro = "SUCESSO"
        clientSocket.send(statusCadastro.encode("utf-8"))

        escutarCliente()

    except:
        statusCliente("Erro inesperado")
        statusCadastro = "ERRO"
        clientSocket.send(statusCadastro.encode("utf-8"))

def criarPasta():
    nomePastaInteiro = clientSocket.recv(1024).decode("utf-8")
    nomePastaNova = clientSocket.recv(1024).decode("utf-8")

    os.makedirs("./users/" + nomePastaInteiro + "/" + nomePastaNova)

def acessarConta():
    arquivoSegurancaLeitura = open("./jsons/Seguranca.json", "rb")
    leituraString = arquivoSegurancaLeitura.readline()
    leituraStringDecode = leituraString.decode()
    dictDadosUsuario = json.loads(leituraStringDecode)
    arquivoSegurancaLeitura.close()

    while True:
        dadosAutenticacaoJS = clientSocket.recv(1024).decode("utf-8") # RECEBE OS DADOS DE AUTENTICAÇÃO DO CLIENTE {NOME: SENHA}
        dictDadosAutenticacao = json.loads(dadosAutenticacaoJS)

        for x in dictDadosAutenticacao:
            nomeUser = x

        senhaUsuario = dictDadosAutenticacao[nomeUser]

        if (nomeUser in dictDadosUsuario) and (senhaUsuario == dictDadosUsuario[nomeUser]):
            statusCliente("Usuário '%s' logado" %nomeUser)
            statusLogin = "LOGADO"
            clientSocket.send(statusLogin.encode("utf-8"))
            break

        else:
            statusCliente("Falha na autenticação — dados incorretos")
            statusLogin = "FALHA"
            clientSocket.send(statusLogin.encode("utf-8"))

def upload():
    nomePastaInteiro = clientSocket.recv(1024).decode("utf-8")
    nomeArquivo = clientSocket.recv(1024).decode("utf-8")

    arquivoBaixadoServidor = open("./users/" + nomePastaInteiro + "/" + nomeArquivo, "wb")

    bytesRecebidos = clientSocket.recv(1024)
    while bytesRecebidos:
        arquivoBaixadoServidor.write(bytesRecebidos)
        bytesRecebidos = clientSocket.recv(1024)
    arquivoBaixadoServidor.close()

    statusCliente("Arquivo '%s' recebido com sucesso" %nomeArquivo)

def download(nomePastaOrigem):
    confirmacaoDownload = clientSocket.recv(1024).decode("utf-8") # RECEBE "S" OU "N".

    if confirmacaoDownload == "S":

        arquivoRequisitado = open("./users/" + nomePastaOrigem, "rb")

        bytesEnviados = arquivoRequisitado.read(1024)
        while bytesEnviados:
            clientSocket.send(bytesEnviados)
            bytesEnviados = arquivoRequisitado.read(1024)
        arquivoRequisitado.close()

        statusCliente("Arquivo enviado com sucesso")

    else: statusCliente("Envio cancelado pelo usuário")

def compartilharArquivo():
    arquivoPermissoesLeitura = open("./jsons/Permissoes.json", "rb")
    arquivoPermissoesLeitura_STRING = arquivoPermissoesLeitura.readline()
    arquivoPermissoesLeitura_DECODE = arquivoPermissoesLeitura_STRING.decode()
    dictPermissoesUsuario = json.loads(arquivoPermissoesLeitura_DECODE)
    arquivoPermissoesLeitura.close()

    listaUsuariosCadastrados = []

    for usuariosCadastrados in dictPermissoesUsuario:
        listaUsuariosCadastrados.append(usuariosCadastrados)

    # ENVIA LISTA DE users CADASTRADOS:
    listaUsuariosCadastrados_JS = json.dumps(listaUsuariosCadastrados)
    clientSocket.send(listaUsuariosCadastrados_JS.encode("utf-8"))
    # OK.

    dadosCompartilhamento_JS = clientSocket.recv(1024).decode("utf-8")
    dadosCompartilhamento = json.loads(dadosCompartilhamento_JS)

    nomeUserACompartilhar = dadosCompartilhamento[0]
    nomeConteudoEscolhido = dadosCompartilhamento[1]
    nomePastaOrigemRespectivo = dadosCompartilhamento[2]

    listarConteudoSelecionado = dictPermissoesUsuario[nomeUserACompartilhar][0]
    listarPastaSelecionada = dictPermissoesUsuario[nomeUserACompartilhar][1]


    if (nomeConteudoEscolhido not in listarConteudoSelecionado) and (listarPastaSelecionada not in listarPastaSelecionada):
        listarConteudoSelecionado.append(nomeConteudoEscolhido)
        listarPastaSelecionada.append(nomePastaOrigemRespectivo)

    listaDadosCompartilhamento = []
    listaDadosCompartilhamento.append(listarConteudoSelecionado)
    listaDadosCompartilhamento.append(listarPastaSelecionada)
    dictConteudoPermitido = {nomeUserACompartilhar : listaDadosCompartilhamento} # Atualiza o dicionário

    arquivoPermissoesEscrita = open("./jsons/Permissoes.json", "wb")
    dictPermissoesUsuario.update(dictConteudoPermitido)
    dictConteudoPermitido_JS = json.dumps(dictPermissoesUsuario, ensure_ascii = False)
    arquivoPermissoesEscrita.write(dictConteudoPermitido_JS.encode())
    arquivoPermissoesEscrita.close()

def meusArquivos():
    nomeUser = clientSocket.recv(1024).decode("utf-8")
    nomePastaOrigem = nomeUser # Para que explore primeiro a pasta inicial do usuário.

    while True:
        listaConteudoDir = os.listdir("users/" + nomePastaOrigem)

        clientSocket.send(nomePastaOrigem.encode("utf-8"))
        time.sleep(0.7)
        listaConteudoDir_JS = json.dumps(listaConteudoDir)
        clientSocket.send(listaConteudoDir_JS.encode("utf-8"))

        nomeConteudoEscolhido = clientSocket.recv(1024).decode("utf-8")
        nomePastaOrigem += "/" + nomeConteudoEscolhido

        trataObjeto(nomePastaOrigem, arquivo = False)

def compartilhadosComUsuario():
    arquivoPermissoesLeitura = open("./jsons/Permissoes.json", "rb")
    arquivoPermissoesLeitura_STRING = arquivoPermissoesLeitura.readline()
    arquivoPermissoesLeitura_DECODE = arquivoPermissoesLeitura_STRING.decode()
    dictPermissoesUsuario = json.loads(arquivoPermissoesLeitura_DECODE)
    arquivoPermissoesLeitura.close()

    nomeUser = clientSocket.recv(1024).decode("utf-8")

    dadosCompartIndividual = dictPermissoesUsuario[nomeUser]

    dadosCompartIndividual_JS = json.dumps(dadosCompartIndividual)
    clientSocket.send(dadosCompartIndividual_JS.encode("utf-8"))

    nomePastaInteiro = clientSocket.recv(1024).decode("utf-8")

    if os.path.isfile("users/" + nomePastaInteiro) == True:
        tipoConteudo = "ARQUIVO"
        clientSocket.send(tipoConteudo.encode("utf-8"))
        time.sleep(0.3)

        trataObjeto(nomePastaInteiro, arquivo = True)
    else:
        tipoConteudo = "PASTA"
        clientSocket.send(tipoConteudo.encode("utf-8"))
        time.sleep(0.3)

        while True:
            listaConteudoDir = os.listdir("users/" + nomePastaInteiro + "/")

            clientSocket.send(nomePastaInteiro.encode("utf-8"))
            time.sleep(0.7)
            listaConteudoDir_JS = json.dumps(listaConteudoDir)
            clientSocket.send(listaConteudoDir_JS.encode("utf-8"))

            nomeConteudoEscolhido = clientSocket.recv(1024).decode("utf-8")
            nomePastaInteiro += nomeConteudoEscolhido + "/"

            trataObjeto(nomePastaInteiro, arquivo = False)

def trataObjeto(nomePastaOrigem, arquivo):
    if os.path.isdir("users/" + nomePastaOrigem + "/") == True:
        tipoConteudo = "Pasta"
        clientSocket.send(tipoConteudo.encode("utf-8"))

        escolhaUsuario = clientSocket.recv(1024).decode("utf-8")

        if escolhaUsuario == "1":
            pass

        elif escolhaUsuario == "2":
            upload()
            escutarCliente()

        elif escolhaUsuario == "3":
            criarPasta()
            escutarCliente()

        elif escolhaUsuario == "4":
            compartilharArquivo()
            escutarCliente()
    else:
        if arquivo == False:
            tipoConteudo = "Arquivo"
            clientSocket.send(tipoConteudo.encode("utf-8"))
            time.sleep(0.5)

        escolhaUsuario = clientSocket.recv(1024).decode("utf-8")

        if escolhaUsuario == "1":
            download(nomePastaOrigem)
            escutarCliente()
        elif escolhaUsuario == "2":
            compartilharArquivo()
            escutarCliente()

escutarCliente()
