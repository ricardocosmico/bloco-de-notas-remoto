"""Servidor TCP do Bloco de Notas Remoto."""
import socket
import threading
from datetime import datetime
from pathlib import Path
from protocolo import codificar, decodificar

PASTA_NOTAS = Path("notas")
PASTA_NOTAS.mkdir(exist_ok=True)
notas_por_usuario = {}
trava = threading.Lock()

def arquivo_usuario(usuario):
    # O nome do arquivo é derivado de uma versão segura do nome do usuário.
    seguro = "".join(c if c.isalnum() or c in "-_" else "_" for c in usuario).strip("_")
    if not seguro:
        seguro = "usuario"
    return PASTA_NOTAS / f"notas_{seguro}.txt"

def carregar_notas(usuario):
    caminho = arquivo_usuario(usuario)
    notas = []
    if caminho.exists():
        for linha in caminho.read_text(encoding="utf-8").splitlines():
            try:
                notas.append(decodificar(linha))
            except Exception:
                continue
    return notas

def salvar_arquivo(usuario):
    caminho = arquivo_usuario(usuario)
    conteudo = "\n".join(codificar(nota) for nota in notas_por_usuario[usuario])
    caminho.write_text(conteudo + ("\n" if conteudo else ""), encoding="utf-8")

def atender_cliente(conexao, endereco):
    print(f"[CONECTADO] {endereco}")
    try:
        arquivo = conexao.makefile("rwb")
        while True:
            linha = arquivo.readline()
            if not linha:
                break
            try:
                partes = linha.decode("utf-8").rstrip("\n").split("|")
                comando, usuario_cod = partes[0], partes[1]
                usuario = decodificar(usuario_cod)

                with trava:
                    if usuario not in notas_por_usuario:
                        notas_por_usuario[usuario] = carregar_notas(usuario)

                    if comando == "SAVE":
                        nota = decodificar(partes[2])
                        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        notas_por_usuario[usuario].append(f"[{horario}] {nota}")
                        salvar_arquivo(usuario)
                        arquivo.write(b"OK|Nota salva com sucesso.\n")
                    elif comando == "LIST":
                        arquivo.write(b"OK|Notas encontradas.\n")
                        for nota in notas_por_usuario[usuario]:
                            arquivo.write(f"NOTE|{codificar(nota)}\n".encode("utf-8"))
                        arquivo.write(b"END\n")
                    elif comando == "CLEAR":
                        notas_por_usuario[usuario].clear()
                        salvar_arquivo(usuario)
                        arquivo.write(b"OK|Todas as suas notas foram apagadas.\n")
                    else:
                        arquivo.write(b"ERRO|Comando desconhecido.\n")
                arquivo.flush()
            except Exception as erro:
                arquivo.write(f"ERRO|{codificar(str(erro))}\n".encode("utf-8"))
                arquivo.flush()
    except Exception as erro:
        print(f"[ERRO] {endereco}: {erro}")
    finally:
        conexao.close()
        print(f"[DESCONECTADO] {endereco}")

def iniciar_servidor():
    ip = input("IP para escuta (use 0.0.0.0 para aceitar conexões da rede): ").strip()
    porta = int(input("Porta: "))
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((ip, porta))
    servidor.listen()
    print(f"Servidor ativo em {ip}:{porta}")
    print("Pressione Ctrl+C para encerrar.")
    try:
        while True:
            conexao, endereco = servidor.accept()
            threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True).start()
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()
