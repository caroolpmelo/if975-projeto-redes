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
    # arquivoSegurancaLeitura = open("./Sistema/Seguranca.json", "rb")
    # leituraString = arquivoSegurancaLeitura.readline()
    # leituraStringDecode = leituraString.decode() # PRECISA DECODAR PRA QUE A BIBLIOTECA JSON CONSIGA LER
    # dictDadosUsuario = json.loads(leituraStringDecode)
    # arquivoSegurancaLeitura.close()

    # arquivoPermissoesLeitura = open("./Sistema/Permissoes.json", "rb")
    # arquivoPermissoesLeitura_STRING = arquivoPermissoesLeitura.readline()
    # arquivoPermissoesLeitura_DECODE = arquivoPermissoesLeitura_STRING.decode()
    # dictPermissoesUsuario = json.loads(arquivoPermissoesLeitura_DECODE)
    # arquivoPermissoesLeitura.close()

    while True:
    #     dictDadosAutenticacao_JS = clientSocket.recv(1024).decode("utf-8")
    #     dictDadosAutenticacao = json.loads(dictDadosAutenticacao_JS)

    #     for x in dictDadosAutenticacao: # COLETA APENAS O NOME DO USUARIO QUE ESTA NO DICIONARIO
    #         nomeUsuario = x

    #     if nomeUsuario in dictDadosUsuario:
    #         statusExistencia = "EXISTENTE"
    #         clientSocket.send(statusExistencia.encode("utf-8"))

    #     else: break

    try:
    #     statusExistencia = "INEXISTENTE" # TEM COMO ENVIAR UM BOOL AO INVÉS DE STR?
    #     clientSocket.send(statusExistencia.encode("utf-8"))

    #     arquivoSegurancaEscrita = open("./Sistema/Seguranca.json", "wb")
    #     dictDadosUsuario.update(dictDadosAutenticacao)
    #     dictAtualizado = json.dumps(dictDadosUsuario, ensure_ascii = False)
    #     arquivoSegurancaEscrita.write(dictAtualizado.encode())
    #     arquivoSegurancaEscrita.close()

    #     pastaPadroes = ["Documentos", "Imagens", "Músicas", "Atividades", "Quaisquer"]

    #     for nomePasta in pastaPadroes:
    #         diretorio = ""
    #         diretorio += nomeUsuario + "/" + nomePasta

    #         os.makedirs("./Usuários/" + diretorio)

    #     arquivoPermissoesEscrita = open("./Sistema/Permissoes.json", "wb")
    #     dictConteudoPermitido = {nomeUsuario : [[], []]}
    #     dictPermissoesUsuario.update(dictConteudoPermitido)
    #     dictConteudoPermitido_JS = json.dumps(dictPermissoesUsuario, ensure_ascii = False)
    #     arquivoPermissoesEscrita.write(dictConteudoPermitido_JS.encode())
    #     arquivoPermissoesEscrita.close()

    #     statusCliente("Novo usuário '%s' cadastrado" %nomeUsuario)
    #     statusCadastro = "SUCESSO"
    #     clientSocket.send(statusCadastro.encode("utf-8"))

        escutarCliente()

    # except:
    #     statusCliente("Erro inesperado")
    #     statusCadastro = "ERRO"
    #     clientSocket.send(statusCadastro.encode("utf-8"))

def acessarConta():
    # arquivoSegurancaLeitura = open("./Sistema/Seguranca.json", "rb")
    # leituraString = arquivoSegurancaLeitura.readline()
    # leituraStringDecode = leituraString.decode()
    # dictDadosUsuario = json.loads(leituraStringDecode)
    # arquivoSegurancaLeitura.close()

    # while True:
    #     dadosAutenticacaoJS = clientSocket.recv(1024).decode("utf-8") # RECEBE OS DADOS DE AUTENTICAÇÃO DO CLIENTE {NOME: SENHA}
    #     dictDadosAutenticacao = json.loads(dadosAutenticacaoJS)

    #     for x in dictDadosAutenticacao:
    #         nomeUsuario = x

    #     senhaUsuario = dictDadosAutenticacao[nomeUsuario]

    #     if (nomeUsuario in dictDadosUsuario) and (senhaUsuario == dictDadosUsuario[nomeUsuario]):
    #         statusCliente("Usuário '%s' logado" %nomeUsuario)
    #         statusLogin = "LOGADO"
    #         clientSocket.send(statusLogin.encode("utf-8"))
    #         break

    #     else:
    #         statusCliente("Falha na autenticação — dados incorretos")
    #         statusLogin = "FALHA"
    #         clientSocket.send(statusLogin.encode("utf-8"))

def upload():
    nomeDirCompleto = clientSocket.recv(1024).decode("utf-8") # RECEBE O NOME COMPLETO DO DIRETORIO PRA ONDE VAI O ARQUIVO
    nomeArquivo = clientSocket.recv(1024).decode("utf-8")

    arquivoBaixadoServidor = open("./Usuários/" + nomeDirCompleto + "/" + nomeArquivo, "wb")

    bytesRecebidos = clientSocket.recv(1024)
    while bytesRecebidos:
        arquivoBaixadoServidor.write(bytesRecebidos)
        bytesRecebidos = clientSocket.recv(1024)
    arquivoBaixadoServidor.close()

    statusCliente("Arquivo '%s' recebido com sucesso" %nomeArquivo)

def download(nomePastaOrigem):
    # confirmacaoDownload = clientSocket.recv(1024).decode("utf-8") # RECEBE "S" OU "N".

    # if confirmacaoDownload == "S":

    #     arquivoRequisitado = open("./Usuários/" + nomePastaOrigem, "rb")

    #     bytesEnviados = arquivoRequisitado.read(1024)
    #     while bytesEnviados:
    #         clientSocket.send(bytesEnviados)
    #         bytesEnviados = arquivoRequisitado.read(1024)
    #     arquivoRequisitado.close()

    #     statusCliente("Arquivo enviado com sucesso")

    # else: statusCliente("Envio cancelado pelo usuário")

def compartilharArquivo():
    # arquivoPermissoesLeitura = open("./Sistema/Permissoes.json", "rb")
    # arquivoPermissoesLeitura_STRING = arquivoPermissoesLeitura.readline()
    # arquivoPermissoesLeitura_DECODE = arquivoPermissoesLeitura_STRING.decode()
    # dictPermissoesUsuario = json.loads(arquivoPermissoesLeitura_DECODE)
    # arquivoPermissoesLeitura.close()

    # listaUsuariosCadastrados = []

    # for usuariosCadastrados in dictPermissoesUsuario:
    #     listaUsuariosCadastrados.append(usuariosCadastrados)

    # # ENVIA LISTA DE USUÁRIOS CADASTRADOS:
    # listaUsuariosCadastrados_JS = json.dumps(listaUsuariosCadastrados)
    # clientSocket.send(listaUsuariosCadastrados_JS.encode("utf-8"))
    # # OK.

    # dadosCompartilhamento_JS = clientSocket.recv(1024).decode("utf-8")
    # dadosCompartilhamento = json.loads(dadosCompartilhamento_JS)

    # nomeUsuarioACompartilhar = dadosCompartilhamento[0]
    # nomeConteudoEscolhido = dadosCompartilhamento[1]
    # nomePastaOrigemRespectivo = dadosCompartilhamento[2]

    # listaConteudoEscolhido = dictPermissoesUsuario[nomeUsuarioACompartilhar][0]
    # listaDiretorioRespectivo = dictPermissoesUsuario[nomeUsuarioACompartilhar][1]


    # if (nomeConteudoEscolhido not in listaConteudoEscolhido) and (listaDiretorioRespectivo not in listaDiretorioRespectivo):
    #     listaConteudoEscolhido.append(nomeConteudoEscolhido)
    #     listaDiretorioRespectivo.append(nomePastaOrigemRespectivo)

    # listaDadosCompartilhamento = []
    # listaDadosCompartilhamento.append(listaConteudoEscolhido)
    # listaDadosCompartilhamento.append(listaDiretorioRespectivo)
    # dictConteudoPermitido = {nomeUsuarioACompartilhar : listaDadosCompartilhamento} # Atualiza o dicionário

    # arquivoPermissoesEscrita = open("./Sistema/Permissoes.json", "wb")
    # dictPermissoesUsuario.update(dictConteudoPermitido)
    # dictConteudoPermitido_JS = json.dumps(dictPermissoesUsuario, ensure_ascii = False)
    # arquivoPermissoesEscrita.write(dictConteudoPermitido_JS.encode())
    # arquivoPermissoesEscrita.close()

def criarPasta():
    nomeDirCompleto = clientSocket.recv(1024).decode("utf-8")
    nomeNovaPasta = clientSocket.recv(1024).decode("utf-8")

    os.makedirs("./Usuários/" + nomeDirCompleto + "/" + nomeNovaPasta)

def SERVIDOR_TratamentoConteudo(nomePastaOrigem, arquivo):
    if os.path.isdir("Usuários/" + nomePastaOrigem + "/") == True:
        msgTipoConteudo = "PASTA"
        clientSocket.send(msgTipoConteudo.encode("utf-8"))

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
            msgTipoConteudo = "ARQUIVO"
            clientSocket.send(msgTipoConteudo.encode("utf-8"))
            time.sleep(0.5)

        escolhaUsuario = clientSocket.recv(1024).decode("utf-8")

        if escolhaUsuario == "1":
            download(nomePastaOrigem)
            escutarCliente()

        elif escolhaUsuario == "2":
            compartilharArquivo()
            escutarCliente()

def meusArquivos():
    nomeUsuario = clientSocket.recv(1024).decode("utf-8")
    nomePastaOrigem = nomeUsuario # Para que explore primeiro a pasta inicial do usuário.

    while True:
        listaConteudoDir = os.listdir("Usuários/" + nomePastaOrigem)

        clientSocket.send(nomePastaOrigem.encode("utf-8"))
        time.sleep(0.7)
        listaConteudoDir_JS = json.dumps(listaConteudoDir)
        clientSocket.send(listaConteudoDir_JS.encode("utf-8"))

        nomeConteudoEscolhido = clientSocket.recv(1024).decode("utf-8")
        nomePastaOrigem += "/" + nomeConteudoEscolhido

        SERVIDOR_TratamentoConteudo(nomePastaOrigem, arquivo = False)

def compartilhadosComUsuario():
    # arquivoPermissoesLeitura = open("./Sistema/Permissoes.json", "rb")
    # arquivoPermissoesLeitura_STRING = arquivoPermissoesLeitura.readline()
    # arquivoPermissoesLeitura_DECODE = arquivoPermissoesLeitura_STRING.decode()
    # dictPermissoesUsuario = json.loads(arquivoPermissoesLeitura_DECODE)
    # arquivoPermissoesLeitura.close()

    # nomeUsuario = clientSocket.recv(1024).decode("utf-8")

    # dadosCompartIndividual = dictPermissoesUsuario[nomeUsuario]

    # dadosCompartIndividual_JS = json.dumps(dadosCompartIndividual)
    # clientSocket.send(dadosCompartIndividual_JS.encode("utf-8"))

    # nomeDirCompleto = clientSocket.recv(1024).decode("utf-8")

    # if os.path.isfile("Usuários/" + nomeDirCompleto) == True:

    #     msgTipoConteudo = "ARQUIVO"
    #     clientSocket.send(msgTipoConteudo.encode("utf-8"))
    #     time.sleep(0.3)

    #     SERVIDOR_TratamentoConteudo(nomeDirCompleto, arquivo = True)
    # else:
    #     msgTipoConteudo = "PASTA"
    #     clientSocket.send(msgTipoConteudo.encode("utf-8"))
    #     time.sleep(0.3)

    #     while True:
    #         listaConteudoDir = os.listdir("Usuários/" + nomeDirCompleto + "/")

    #         clientSocket.send(nomeDirCompleto.encode("utf-8"))
    #         time.sleep(0.7)
    #         listaConteudoDir_JS = json.dumps(listaConteudoDir)
    #         clientSocket.send(listaConteudoDir_JS.encode("utf-8"))

    #         nomeConteudoEscolhido = clientSocket.recv(1024).decode("utf-8")
    #         nomeDirCompleto += nomeConteudoEscolhido + "/"

    #         SERVIDOR_TratamentoConteudo(nomeDirCompleto, arquivo = False)

escutarCliente()
