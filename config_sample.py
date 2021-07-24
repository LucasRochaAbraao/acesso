#!/usr/bin/env python3
# coding=utf-8

#################################
#      Lucas Rocha Abraao       #
#     lucasrabraao@gmail.com    #
#           25/11/2020          #
#################################

from collections import namedtuple


class Config:
    __OLT = namedtuple('OLT', ['usuario', 'senha', 'ip', 'protocolo', 'porta', 'fabricante'])
    __SW = namedtuple('Switch', ['usuario', 'senha', 'ip', 'protocolo', 'porta', 'fabricante'])
    __SRV = namedtuple('Servidor', ['usuario', 'senha', 'ip', 'protocolo', 'porta', 'fabricante'])


    __categorias = {
        # Dispositivo      usuario          senha                ip       protocolo    porta  fabricante
        'OLT': {
            'OLT1': __OLT('usuario',    'senha@dificil',    '10.0.10.2',    'ssh',      22,     'huawei'),
            'OLT2': __OLT('usuario',    'senha#segura',     '10.0.10.6',    'ssh',      2222,   'huawei'),
            'OLT3': __OLT('usuario',    'senha_unica',      '10.0.10.10',   'telnet',   23,     'huawei'),
            'OLT4': __OLT('usuario',    'senha_123',        '10.0.10.14',   'telnet',   23,     'huawei'),
        },
        
        # Dispositivo      nome                   usuario      senha            ip           protocolo porta
        'SW': {
            'PE 1': __SW('lucas',   'Lucas93@huawei',   '10.0.99.1',    'ssh',  22, 'huawei'),
            'PE 2': __SW('user',    'Lucas93@huawei',   '10.222.212.2', 'ssh',  22, 'huawei'),
            'PE n': __SW('usuario', 'Lucas93@huawei',   '10.0.99.2',    'ssh',  22, 'huawei'),
            'BGP':  __SW('admin',   'Lucas93@huawei',   '10.0.99.3',    'ssh',  22, 'huawei'),
        },

        # Dispositivo      nome                   usuario      senha            ip          protocolo porta
        'SRV': {
            'Server1':              __SRV('root',   'senha@DIFICIL',    '10.0.30.2',    'ssh',      22,     'linux'),
            'DNS Autoritativo 1':   __SRV('admin',  'SENHA#segura',     '10.0.30.6',    'chave',    22,     'linux'),
            'Flask Projects':       __SRV('lucas',  'alguma_senha',     '10.0.30.10',   'chave',    2217,   'linux'),
        }   # obs: protocolo chave = ssh key, acesso sem senha
    }

    @staticmethod
    def get_dispositivos(opcao=None, disp=False):
        if disp:
            return Config.__categorias[opcao][disp]
        else:
            return Config.__categorias[opcao]

#from config import Config
#print(Config.get_dispositivos(opcao='OLT'))
