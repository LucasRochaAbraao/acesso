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

    # Dispositivo    nome              usuario       senha                  ip       protocolo porta
    __OLTs =       {'OLT1':     __OLT('usuario',    'senha@segura',    '10.0.10.20',   'ssh',  22),
                    'OLT2':     __OLT('usuario',    'senha@segura',    '10.0.10.30',   'ssh',  22),
                    'OLT3':     __OLT('usuario',    'senha@segura',    '10.0.10.40',   'ssh',  22)}
    
    __SW = namedtuple('Switch', ['usuario', 'password', 'ip', 'protocolo', 'porta'])
    # Dispositivo    nome             usuario        senha                  ip       protocolo porta
    __SWs =        {'SW1':      __SW('usuario',     'senha@segura',     '10.0.0.20',    'ssh',  22),
                    'SW2':      __SW('usuario',     'senha@segura',     '10.0.0.30',    'ssh',  22),
                    'SW3':      __SW('usuario',     'senha@segura',     '10.0.0.40',    'ssh',  22)}

    __SRV = namedtuple('Servidor', ['usuario', 'password', 'ip', 'protocolo', 'porta'])
    # Dispositivo    nome             usuario        senha                  ip       protocolo porta
    __SRVs =       {'server1':  __SRV('root',       'senha@segura',     '10.0.20.20',  'ssh',   22),
                    'server2':  __SRV('usuario',    'senha@segura',     '10.0.20.30',  'chave', 22),
                    'server3':  __SRV('root',       'senha@segura',     '10.0.20.40',  'chave', 22)}
                    # obs: protocolo chave = ssh key, acesso sem senha

    @staticmethod
    def get_olt(disp=None, todas=False):
        if todas:
            return Config.__OLTs
        elif disp == None:
            print("Por favor, selecione um dispositivo.")
            exit()
        else:
            return Config.__OLTs[disp]
    
    @staticmethod
    def get_sw(disp=None, todas=False):
        if todas:
            return Config.__SWs
        elif disp == None:
            print("Por favor, selecione um dispositivo.")
            exit()
        else:
            return Config.__SWs[disp]
    
    @staticmethod
    def get_srv(disp=None, Todas=False):
        if todas:
            return Config.__SRVs
        elif disp == None:
            print("Por favor, selecione um dispositivo.")
            exit()
        else:
            return Config.__SRVs[disp]

#from config import Config
#print(Config.get_olt("OLT1"))
#print(Config.get_olt(todas=True))
#print(Config.get_olt())

