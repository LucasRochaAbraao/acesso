#!/usr/bin/env python3
# coding=utf-8

import os
import pathlib
import pexpect
import subprocess
from datetime import datetime
from PyInquirer import style_from_dict, Token, prompt, Separator
from configparser import ConfigParser

# TODO
# - Nome do usuário no log

ce_secret = ConfigParser()
ce_secret.read(str(pathlib.Path(__file__).parent.absolute()) + '/secrets.ini')
creds = ce_secret['CONCENTRADOR']
usuario = creds['user']
passw = creds['passw']

######## endereços dos concentradores ########
ce_config = ConfigParser()
ce_config.read(str(pathlib.Path(__file__).parent.absolute()) + '/config.ini')
CEs = ce_config['CONCENTRADORES']

hosts = {}
for ce in CEs:
    # concentrado > endereço
    hosts[ce] = CEs[ce]
hostnames = tuple(CEs)

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

subprocess.Popen("clear")
from pyfiglet import Figlet
# http://www.figlet.org/examples.html
print(Figlet("eftifont").renderText('CONCENTRADORES'))

hostname_choices = []
for host in hostnames:
    hostname_choices.append({'name': host})
hostname_choices.append({'name': 'voltar'})

while True:
    opcoes = [{
        'type': 'list',
        'message': 'Selecione o CE desejado:',
        'name': 'concentradores',
        'choices': hostname_choices
    }]

    resposta = prompt(opcoes, style=style) # dicionário no formato {'concentradores': 'nome-do-ce'}
    ce = ''.join((ce for ce in resposta.values())) # extrai o valor 'nome-do-ce' do dicionário "answers"
    destino = CEs.get(ce) # extrai o ip do dicionário "addresses" dado o valor selecionado.

    if ce == 'voltar':
        subprocess.Popen("clear")
        break

    ######## logs ########
    dir_atual    = os.path.dirname(__file__)
    dir_relativo = datetime.now().strftime('logs/CEs/' + ce + '-%Y_%m_%d-%H_%M_%S.log')
    dir_absoluto = os.path.join(dir_atual, dir_relativo)
    logs = open(dir_absoluto, 'wb')

    ####### acesso winbox #######
    subprocess.call(["wine","/home/lucas/bin/winbox-318.exe", destino])

    ####### acesso ssh #######
    #connect = pexpect.spawn(f'ssh {usuario}@{destino})
    #connect.logfile= logs # linka processo "filho" do pexpect.spawn  ao arquivo log
    #connect.expect(":")
    #connect.sendline(passw)
    #connect.interact()

    subprocess.Popen("clear")
    logs.close()
