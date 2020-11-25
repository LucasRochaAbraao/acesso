#!/usr/bin/env python3
# coding=utf-8

import os
import pathlib
import pexpect
import subprocess
from configparser import ConfigParser
from datetime import datetime
from PyInquirer import style_from_dict, Token, prompt, Separator

# TODO:
# - Nome do usuário no log
# - Change lists to tuples
# (same syntax, faster for fixed size)

creds_config = ConfigParser()
creds_config.read(str(pathlib.Path(__file__).parent.absolute()) + '/secrets.ini')
creds = creds_config['OLTS']

olts_config = ConfigParser()
olts_config.read(str(pathlib.Path(__file__).parent.absolute()) + '/config.ini')
olts = olts_config['OLTS']

hosts = {}
for olt in olts:
    hosts[olt] = olts[olt]

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
print(Figlet("eftifont").renderText('OLTS'))

hostnames = tuple(olts)
hostname_choices = []
for host in hostnames:
    hostname_choices.append({'name': host})
hostname_choices.append({'name': 'voltar'})

while True:
    opcoes = [{
        'type': 'list',
        'message': 'Selecione a olt desejada:',
        'name': 'olts',
        'choices': hostname_choices}]

    resposta = prompt(opcoes, style=style) # dicionário no formato {'olts': 'nome-da-olt'}
    olt = ''.join((olt for olt in resposta.values())) # extrai o valor 'nome-da-olt' do dicionário "resposta"
    destino = hosts.get(olt) # extrai o ip do dicionário "addresses" dado o valor selecionado.

    if olt == 'voltar':
        subprocess.Popen("clear")
        break

    ######## logs ########  
    script_dir    = os.path.dirname(__file__)
    relativo_dir  = datetime.now().strftime('logs/OLTs/' + olt + '-%Y_%m_%d-%H_%M_%S.log')
    abs_file_path = os.path.join(script_dir, relativo_dir)
    logs = open(abs_file_path, 'wb')

    ####### acesso ######
    connect = pexpect.spawn(f'telnet {destino}')
    connect.logfile_read = logs # linka processo "filho" do pexpect.spawn  ao arquivo log
    connect.expect(":")
    connect.sendline(creds['user'])
    connect.expect(":")
    connect.sendline(creds['passw'])
    connect.expect(">")
    connect.sendline("enable")
    connect.sendline("config")

    connect.interact()
    print('Desconectado da OLT. Caso deseje sair do menu, selecione "sair"')
    logs.close()
