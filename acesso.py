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
# - criar um script para atualizar os arquivos .ini. Adicionar
# hosts e usuário+senha.
# -


import argparse
from PyInquirer import style_from_dict, Token, prompt, Separator
import os
import sys
import time
import subprocess
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
    opcoes = [{
        'type': 'list',
        'message': 'Selecione a categoria desejada:',
        'name': 'olts',
        'choices': [{'name': 'OLTs'},
                    {'name': 'Switches'},
                    {'name': 'CEs'},
                    {'name': 'sair'}]
}]

    # resposta é um dicionário no formato {'olts': 'nome-da-olt'}
    resposta = prompt(opcoes, style=style)

    # extrai o valor 'nome-da-olt' do dicionário "resposta"
    valor = ''.join(valor for valor in resposta.values())

    if valor == 'sair':
        print('Volte sempre!')
        time.sleep(0.5)
        subprocess.Popen("clear")
        sys.exit()

    ######## rodar scripts selecionados ########
    base_file = os.readlink(os.path.abspath(__file__))
    # Preciso extrair um symlink aqui pq crio um para manter o código
    # no diretório com git, e o executável (softlink) em outro diretório (no $PATH)

    if valor == 'OLTs':
        destino = os.path.dirname(base_file) + '/olts.py'
    elif valor == 'Switches':
        destino = os.path.dirname(base_file) + '/switches.py'
    elif valor == 'CEs':
        destino = os.path.dirname(base_file) + '/concentradores.py'


    subprocess.call(["python3", destino])

    # desenha o banner de novo, agora no loop infinito do menu principal
    print(Figlet("eftifont").renderText('MENU PRINCIPAL'))
