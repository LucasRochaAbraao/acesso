#!/usr/bin/env python3
# coding=utf-8

import os
import pathlib
import pexpect
import subprocess
from datetime import datetime
from PyInquirer import style_from_dict, Token, prompt, Separator
from configparser import ConfigParser

# TODO:
# - Nome do usuário no log

switches_config = ConfigParser()
switches_config.read(str(pathlib.Path(__file__).parent.absolute()) + '/config.ini')
switches = switches_config['SWITCHES']

hosts = {}
for sw in switches:
    # switch > ['endereço','porta','protocolo','usuario','senha']
    hosts[sw] = [switches[sw].split()[0],  # endereço
                 switches[sw].split()[1],  # porta
                 switches[sw].split()[2],  # protocolo
                 switches[sw].split()[3],  # usuario
                 switches[sw].split()[4]]  # senha

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
print(Figlet("eftifont").renderText('SWITCHES'))

hostnames = tuple(switches)
hostname_choices = []
for host in hostnames:
    hostname_choices.append({'name': host})
hostname_choices.append({'name': 'voltar'})

while True:
    opcoes = [{
        'type': 'list',
        'message': 'Selecione o switch desejado:',
        'name': 'switches',
        'choices': hostname_choices
    }]

    resposta = prompt(opcoes, style=style) # dicionário no formato {'switches': 'nome-do-switch'}
    switch = ''.join((switch for switch in resposta.values())) # extrai o valor 'nome-do-switch' do dicionário "resposta"
    #destino = hosts.get(switch) # extrai o ip do dicionário "addresses" dado o valor selecionado.
    if switch == 'voltar':
        subprocess.Popen("clear")
        break
    destino, porta, protocolo, usuario, senha = hosts[switch]

    ######## logs ########
    script_dir    = os.path.dirname(__file__)
    relativo_dir  = datetime.now().strftime('logs/SWs/' + switch + '-%Y_%m_%d-%H_%M_%S.log')
    abs_file_path = os.path.join(script_dir, relativo_dir)
    logs = open(abs_file_path, 'wb')

    ####### acesso #######
    if protocolo == 'telnet':
        connect = pexpect.spawn(f'{protocolo} {destino} {porta}')
        connect.expect(":")
        connect.sendline(usuario)
    else:
        connect = pexpect.spawn(f'{protocolo} -p {porta} {usuario}@{destino}')

    connect.logfile_read = logs # linka processo "filho" do pexpect.spawn  ao arquivo log
    connect.expect(":")
    connect.sendline(senha)
    connect.sendline('\r\n')

    connect.interact()
    print('Desconectado do switch. Selecione "voltar" para retornar ao menu anterior')
    logs.close()
