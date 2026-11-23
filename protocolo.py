"""Funções compartilhadas do protocolo cliente-servidor."""
import base64

def codificar(texto: str) -> str:
    return base64.b64encode(texto.encode("utf-8")).decode("ascii")

def decodificar(texto: str) -> str:
    return base64.b64decode(texto.encode("ascii")).decode("utf-8")
