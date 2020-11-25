#!/usr/bin/env python3
# coding=utf-8

#################################
#      Lucas Rocha Abraao       #
#     lucasrabraao@gmail.com    #
#           25/11/2020          #
#################################


from collections import namedtuple

class Config:
    __OLT = namedtuple('OLT', ['usuario', 'password', 'ip', 'protocolo', 'porta'])
    __SW = namedtuple('Switch', ['usuario', 'password', 'ip', 'protocolo', 'porta'])
    __SRV = namedtuple('Servidor', ['usuario', 'password', 'ip', 'protocolo', 'porta'])

    __categorias = {
        # Dispositivo nome           usuario      senha            ip       protocolo porta
        'OLTs':     {'OLT1':   __OLT('usuario',  'senha@dificil',  '10.0.10.2',   'ssh',  22),
                    'OLT2':    __OLT('usuario',  'senha#segura',   '10.0.10.6',   'ssh',  22),
                    'OLT3':    __OLT('usuario',  'senha_unica',    '10.0.10.10',  'ssh',  22)},

        # Dispositivo    nome                usuario      senha            ip        protocolo porta
        'SWs':      {'PE1 (s6720)':     __SW('lucas',   'senha@dificil', '10.0.20.2',   'ssh',  22),
                    'PPPoE Srv (NE20)': __SW('usuario', 'senha#segura',  '10.0.20.6',   'ssh',  22),
                    'BGP (NE40)':       __SW('admin',   'senha_unica',   '10.0.20.10',  'ssh',  22)},

        # Dispositivo    nome                  usuario        senha             ip       protocolo porta
        'SRVs':     {'MKSolutions':      __SRV('root',     'senha@dificil',  '10.0.30.2',  'ssh',   22),
                    'DNS Autoritativo 1':__SRV('usuario',  'senha#segura',   '10.0.30.6',  'chave', 22),
                    'Flask Projects':    __SRV('lucas',    'senha_unica',    '10.0.30.10', 'chave', 22)}
                    # obs: protocolo chave = ssh key, acesso sem senha
    }

    @staticmethod
    def get_olt(disp=None, todas=False):
        if disp == None and todas == False:
            print("Por favor, selecione um dispositivo.")
            exit()
        elif disp:
            return Config.categorias['OLTs'][disp]
        else: # todas = True
            return Config.categorias['OLTs']

    @staticmethod
    def get_sw(disp=None, todas=False):
        if disp == None and todas == False:
            print("Por favor, selecione um dispositivo.")
            exit()
        elif disp:
            return Config.categorias['SWs'][disp]
        else: # todas = True
            return Config.categorias['SWs']

    @staticmethod
    def get_srv(disp=None, todas=False):
        if disp == None and todas == False:
            print("Por favor, selecione um dispositivo.")
            exit()
        elif disp:
            return Config.categorias['SRVs'][disp]
        else: # todas = True
            return Config.categorias['SRVs']

#from config import Config
#print(Config.get_olt(todas=True))
#print(Config.get_olt(disp='Bela Roma'))
#print(Config.get_olt()) # dá erro e sai do script


