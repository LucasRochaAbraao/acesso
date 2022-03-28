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

Esse script cria um menu para acessar equipamentos de forma ágil.
Sinta se à vontade para editar/alterar o que precisar. Retirei
meus hosts e credenciais, deixei apenas um exemplo. Tomem cuidado
para fazer o mesmo ao compartilhar com outras pessoas.
"""

# TODO
# - Eu tinha em mente colocar um menu para inclur e excluir hosts,
# mas acho desnecessário, prefiro editar o arquivo config.py msm.
# - Adicionar credenciais de acesso.
# -


import inquirer
import argparse
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
TEMA = inquirer.themes.GreenPassion()

if __name__ == '__main__':

    # print(answers)
    while True:
        categorias = list()
        for categ in Config.get_categorias():
            categorias.append(categ)
        categorias.append('sair')

        # resposta é um dicionário no formato {'menu': 'categoria'}
        categorias_opcoes = [
            inquirer.List(
                'categoria',
                message="O que você deseja acessar?",
                choices=categorias,
                carousel=True,
            ),
        ]
        categoria = inquirer.prompt(categorias_opcoes, theme=TEMA)['categoria']

        if categoria == 'sair':
            print('Volte sempre!')
            time.sleep(0.5)
            subprocess.run('clear -x', shell=True)
            sys.exit()

        # retorna um namedtuple de todos dispositivos
        hosts = Config.get_dispositivos(opcao=categoria)

        hostname_choices = [host for host in hosts]
        hostname_choices.append('voltar')

        subprocess.run('clear -x', shell=True)
        while True:
            print(Figlet("eftifont").renderText(categoria.upper())) # Banner da categoria atual
            host_options = [
                inquirer.List(
                    'hosts',
                    message=f"Qual {categoria} gostaria de acessar?",
                    choices=hostname_choices,
                    carousel=True,
                ),
            ]
            host = inquirer.prompt(host_options, theme=TEMA)['hosts']
            subprocess.run('clear -x', shell=True)
            if host == 'voltar':
                print(Figlet("eftifont").renderText("MENU PRINCIPAL")) # Banner menu principal
                break

            destino = hosts.get(host) # extrai o namedtuple de um host do arquivo config.py
            ######## logs ########  
            script_dir    = os.path.dirname(__file__)
            host_name = host.replace(' ', '_') # substitui espaço por underscore para o nome do log sem espaço
            relativo_dir  = datetime.now().strftime(f'logs/{categoria}/{host_name}-%Y_%m_%d-%H_%M_%S.log')
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
            
            elif destino.protocolo == 'web':
                subprocess.Popen(f"google-chrome-stable {destino.ip} &>/dev/null", shell=True)
                break


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
            print('Desconectado do dispositivo. Caso deseje voltar ao menu principal, selecione "voltar".')
            subprocess.run('clear -x', shell=True)
            logs.close()



    #subprocess.call(["python3", destino])

    # desenha o banner de novo, agora no loop infinito do menu principal
    print(Figlet("eftifont").renderText('MENU PRINCIPAL'))



##### INQUIRER CHEATSHEET #####
# questions = [
#     inquirer.List(
#         'tipo',
#         message="O que você deseja acessar?",
#         choices=['OLT', 'Switch', 'Cliente', 'Servidor, Config'],
#         carousel=True,
#     ),
#     inquirer.Text('user', message='Please enter your github username', validate=lambda _, x: x != '.'),
#     inquirer.Password('password', message='Please enter your password'),
#     inquirer.Text('repo', message='Please enter the repo name', default='default'),
#     inquirer.Checkbox('topics', message='Please define your type of project?', choices=['common', 'backend', 'frontend'], default='backend'),
#     inquirer.Text('organization', message='If this is a repo from a organization please enter the organization name, if not just leave this blank'),
#     inquirer.Confirm('correct',  message='This will delete all your current labels and create a new ones. Continue?', default=False),
# ]

# answers = inquirer.prompt(questions, theme=inquirer.themes.GreenPassion())