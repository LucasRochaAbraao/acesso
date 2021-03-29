#!/usr/bin/env python3
# coding=utf-8

import os
import pathlib
import pexpect
import subprocess
from datetime import datetime
from PyInquirer import style_from_dict, Token, prompt, Separator
from config import Config

# TODO:
# - Nome do usuário no log
# - mudar arquivo todo pra uma classe, ou no mínimo uma func main().

subprocess.Popen("clear")
from pyfiglet import Figlet
# http://www.figlet.org/examples.html
print(Figlet("eftifont").renderText('SERVIDORES'))

########## estilo + opções #########
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

# retorna um namedtuple de todos dispositivos
hosts = Config.get_dispositivos(opcao='SRV')

hostname_choices = [{'name': host} for host in hosts]
hostname_choices.append({'name': 'voltar'})

while True:
    opcoes = [{
        'type': 'list',
        'message': 'Selecione o servidor desejada:',
        'name': 'servidores',
        'choices': hostname_choices}]

    resposta = prompt(opcoes, style=style) # dicionário no formato {'olts': 'nome-da-olt'}
    servidor = ''.join((servidor for servidor in resposta.values())) # extrai o valor 'nome-da-olt' do dicionário "resposta"

    if servidor == 'voltar':
        subprocess.Popen("clear")
        break

    destino = hosts.get(servidor) # extrai o ip do dicionário "addresses" dado o valor selecionado.

    ######## logs ########  
    script_dir    = os.path.dirname(__file__)
    relativo_dir  = datetime.now().strftime('logs/SRVs/' + servidor + '-%Y_%m_%d-%H_%M_%S.log')
    abs_file_path = os.path.join(script_dir, relativo_dir)
    logs = open(abs_file_path, 'wb')

    ####### acesso ######
    PROMPT = ["#", ">", ":", "$"]
    if destino.protocolo == 'chave' or destino.protocolo == 'ssh':
        connect = pexpect.spawn(f'ssh -p {destino.porta} {destino.usuario}@{destino.ip}')
        connect.logfile_read = logs
        connect.expect(PROMPT)
        if destino.protocolo == 'ssh':
            connect.expect(PROMPT)
            connect.sendline(destino.senha)
            connect.expect(PROMPT)
            connect.sendline("\r")
    else: # telnet
        connect = pexpect.spawn(f'telnet {destino.ip} {destino.porta}')
        connect.logfile_read = logs # linka processo "filho" do pexpect.spawn  ao arquivo log
        connect.expect(PROMPT)
        connect.sendline(destino.usuario)
        connect.expect(PROMPT)
        connect.sendline(destino.senha)
        connect.sendline("\r")

    connect.interact()
    print('Desconectado da OLT. Caso deseje sair do menu, selecione "sair"')
    logs.close()
