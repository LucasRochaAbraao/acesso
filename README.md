# ACESSO
This tool allows me to access all cli hosts in my network, by categories.
Steps to use it:

- Clone the repo.
- Rename config_sample.py to config.py and edit it to fit your network needs.
- Pip install the required packages (`PyInquirer, Figlet, pexpect`):
`pip install -r requirements.txt`
- Make a symbolic link to a directory that's part of your **$PATH**:
`ln -s /home/USER/Dev/access/access.py /home/USER/.local/bin/access`
- Run `access` from your terminal (or what ever you called the sym link).

---

Essa ferramenta me permite acessar todos hosts na minha rede via cli e por categorias.
Passos para usá-la:

- Clone o repo.
- Renomeie o arquivo config_sample.py para config.py e edite de acordo com as necessidades da sua rede.
- Pip install os pacotes exigidos (`PyInquirer, Figlet, pexpect`):
`pip install -r requirements.txt`
- Faça um symbolic link para um diretório que faça parte do seu **$PATH**:
`ln -s /home/USER/Dev/access/access.py /home/USER/.local/bin/access`
- Execute `acesso` pelo terminal (ou onde for que salvou o sym link).
