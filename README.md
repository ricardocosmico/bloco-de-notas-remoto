# Bloco de Notas Remoto — Redes de Computadores I

**Tema 4 — Nuvem de Textos**  
**Tecnologia:** Sockets TCP / arquitetura cliente-servidor  
**Ambiente recomendado:** Linux Debian em duas VMs do VirtualBox na mesma rede local.

## 1. Descrição

O projeto implementa um serviço de anotações pessoais. O cliente conecta-se ao servidor por TCP, informa seu nome e pode salvar, consultar ou apagar suas próprias notas.

Cada usuário possui uma lista independente. O servidor registra automaticamente a data e a hora de criação de cada anotação e mantém os dados em arquivos `.txt`, permitindo que as notas continuem disponíveis após o encerramento do programa.

A implementação é feita em **Python** por meio dos arquivos `cliente.py`, `servidor.py` e `protocolo.py`.

## 2. Funcionalidades implementadas

| Requisito | Implementação |
|---|---|
| Servidor solicita IP e porta | Sim |
| Cliente solicita IP, porta e usuário | Sim |
| Salvar anotação | Comando `SAVE` |
| Listar anotações do usuário | Comando `LIST` |
| Apagar anotações do usuário | Comando `CLEAR` |
| Separação das notas por usuário | Dicionário/lista no servidor |
| Data e hora automáticas | Sim |
| Persistência em arquivos `.txt` | Sim |
| Menu de opções 1, 2, 3 e 0 | Sim |
| Comunicação TCP | Sim |

## 3. Estrutura dos arquivos

```text
bloco_notas_remoto/
├── README.md
└── python/
    ├── cliente.py
    ├── servidor.py
    └── protocolo.py