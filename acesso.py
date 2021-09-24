#!/usr/bin/env python3
# coding=utf-8

#################################
#      Lucas Rocha Abraao       #
#     lucasrabraao@gmail.com    #
#################################
"""
OBS:
Foi testado apenas no Linux. Se o windows não for capaz
de rodar, ativem o subsistema do linux que deve funcionar.

Instalar:
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
pip3 install PyInquirer
pip3 install pyfiglet
pip3 install pexpect

Esse script cria um menu para abrir outros scirpts, que contém
outros menus para acessar equipamentos de forma ágil. Sinta se
à vontade para editar/alterar o que precisar. Retirei meus
hosts e credenciais, deixei apenas um exemplo. Tomem cuidado
para fazer o mesmo ao compartilhar com outras pessoas.
Um dia vou refazer esse script usando o módulo curses...
"""

# TODO
# - Eu tinha em mente colocar um menu para inclur e excluir hosts,
# mas acho desnecessário, prefiro editar o arquivo config.py msm.
# - Adicionar credenciais de acesso.
# -


import argparse
from PyInquirer import style_from_dict, Token, prompt, Separator
import os
import sys
import time
import subprocess
import pathlib
import pexpect
from datetime import datetime
from config import Config
from pyfiglet import Figlet
# http://www.figlet.org/examples.html
print(Figlet("eftifont").renderText('MENU PRINCIPAL'))  # banner inicial



########## estilo + opções do menu #########
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

while True:
    
    categorias = list()
    for categ in Config.get_categorias():
        categorias.append({'name': categ})
    categorias.append({'name': 'sair'})

    opcoes = [{
        'type': 'list',
        'message': 'Selecione a categoria desejada:',
        'name': 'menu',
        'choices': categorias
}]

    # resposta é um dicionário no formato {'menu': 'categoria'}
    resposta = prompt(opcoes, style=style)

    # extrai o valor 'categoria' do dicionário "resposta"
    categoria = ''.join(valor for valor in resposta.values())

    if categoria == 'sair':
        print('Volte sempre!')
        time.sleep(0.5)
        #subprocess.Popen("clear")
        sys.exit()
    
    
    # retorna um namedtuple de todos dispositivos
    hosts = Config.get_dispositivos(opcao=categoria)

    hostname_choices = [{'name': host} for host in hosts]
    hostname_choices.append({'name': 'voltar'})

    while True:
        opcoes = [{
            'type': 'list',
            'message': 'Selecione o dispositivo desejado:',
            'name': 'dispositivos',
            'choices': hostname_choices}]

        resposta = prompt(opcoes, style=style) # dicionário no formato {'dispositivos': 'dispositivo'}
        dispositivo = ''.join((disp for disp in resposta.values())) # extrai o valor 'dispositivo' do dicionário "resposta"

        if dispositivo == 'voltar':
            subprocess.Popen("clear")
            break

        destino = hosts.get(dispositivo) # extrai o namedtuple de um dispositivo do arquivo config.py
        ######## logs ########  
        script_dir    = os.path.dirname(__file__)
        dispositivo_name = dispositivo.replace(' ', '_') # substitui espaço por underscore para o nome do log sem espaço
        relativo_dir  = datetime.now().strftime(f'logs/{categoria}/{dispositivo_name}-%Y_%m_%d-%H_%M_%S.log')
        abs_file_path = os.path.join(script_dir, relativo_dir)
        logs = open(abs_file_path, 'wb')

        ####### acesso ######
        PROMPT = ["#", ">", ":"]
       
        # ssh com senha
        if destino.protocolo == 'ssh':
            connect = pexpect.spawn(f'ssh -p {destino.porta} {destino.usuario}@{destino.ip}')
            connect.logfile_read = logs
            connect.expect(PROMPT)
            connect.sendline(destino.senha)
            connect.expect(PROMPT)
            if destino.fabricante == 'huawei':
                if isinstance(destino, Config._Config__OLT):
                    connect.sendline("enable")
                    connect.expect(PROMPT)
                    connect.sendline("config")
                    connect.expect(PROMPT)
                    connect.sendline("\r")
        
        # ssh com chave
        elif destino.protocolo == 'chave':
            connect = pexpect.spawn(f'ssh -p {destino.porta} {destino.usuario}@{destino.ip}')
            connect.logfile_read = logs
            connect.expect(PROMPT)


        else: # telnet
            connect = pexpect.spawn(f'telnet {destino.ip} {destino.porta}')
            connect.logfile_read = logs # linka processo "filho" do pexpect.spawn  ao arquivo log
            connect.expect(PROMPT)
            connect.sendline(destino.usuario)
            connect.expect(PROMPT)
            connect.sendline(destino.senha)
            if destino.fabricante == 'huawei':
                if isinstance(destino, Config._Config__OLT):
                    connect.sendline("enable")
                    connect.expect(PROMPT)
                    connect.sendline("config")
                    connect.expect(PROMPT)
                    connect.sendline("\r")

        connect.interact()
        print('Desconectado do dispositivo. Caso deseje sair do menu principal, selecione "sair"')
        logs.close()



    #subprocess.call(["python3", destino])

    # desenha o banner de novo, agora no loop infinito do menu principal
    print(Figlet("eftifont").renderText('MENU PRINCIPAL'))
