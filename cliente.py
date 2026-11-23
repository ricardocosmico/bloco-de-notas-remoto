"""Cliente TCP do Bloco de Notas Remoto."""
import socket
from protocolo import codificar, decodificar

def receber_linha(arquivo):
    linha = arquivo.readline()
    if not linha:
        raise ConnectionError("O servidor encerrou a conexão.")
    return linha.decode("utf-8").rstrip("\n")

def iniciar_cliente():
    ip = input("IP do servidor: ").strip()
    porta = int(input("Porta do servidor: "))
    usuario = input("Nome do usuário: ").strip()
    if not usuario:
        print("O nome do usuário não pode ficar vazio.")
        return

    try:
        with socket.create_connection((ip, porta)) as conexao:
            arquivo = conexao.makefile("rwb")
            print(f"\nConectado como {usuario}!")
            while True:
                print("\n===== BLOCO DE NOTAS REMOTO =====")
                print("1 - Escrever nova anotação")
                print("2 - Ler minhas anotações")
                print("3 - Apagar minhas anotações")
                print("0 - Sair")
                opcao = input("Escolha: ").strip()

                if opcao == "1":
                    nota = input("Digite sua anotação: ")
                    arquivo.write(f"SAVE|{codificar(usuario)}|{codificar(nota)}\n".encode("utf-8"))
                    arquivo.flush()
                    print(receber_linha(arquivo).split("|", 1)[-1])
                elif opcao == "2":
                    arquivo.write(f"LIST|{codificar(usuario)}\n".encode("utf-8"))
                    arquivo.flush()
                    resposta = receber_linha(arquivo)
                    if resposta.startswith("ERRO|"):
                        print("Erro ao listar as notas.")
                        continue
                    notas = []
                    while True:
                        linha = receber_linha(arquivo)
                        if linha == "END":
                            break
                        if linha.startswith("NOTE|"):
                            notas.append(decodificar(linha.split("|", 1)[1]))
                    if notas:
                        print("\n--- SUAS ANOTAÇÕES ---")
                        for numero, nota in enumerate(notas, start=1):
                            print(f"\n{numero}. {nota}")
                    else:
                        print("Você ainda não possui anotações.")
                elif opcao == "3":
                    confirmacao = input("Tem certeza que deseja apagar todas as notas? (s/n): ").lower()
                    if confirmacao == "s":
                        arquivo.write(f"CLEAR|{codificar(usuario)}\n".encode("utf-8"))
                        arquivo.flush()
                        print(receber_linha(arquivo).split("|", 1)[-1])
                    else:
                        print("Operação cancelada.")
                elif opcao == "0":
                    print("Até mais!")
                    break
                else:
                    print("Opção inválida. Escolha 0, 1, 2 ou 3.")
    except (OSError, ValueError, ConnectionError) as erro:
        print(f"Não foi possível conectar ou continuar: {erro}")

if __name__ == "__main__":
    iniciar_cliente()
