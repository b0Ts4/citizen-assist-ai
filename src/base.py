"""Leitura e validação da base de conhecimento (JSON).

A base fica em data/base_conhecimento.json e os temas em data/temas.json.
Para acrescentar ou corrigir orientações basta editar o JSON: as regras
do programa não mudam. Registros com problema são ignorados e geram um
aviso, para que um erro em um registro não derrube o sistema inteiro.
"""

import json
import os
import re

PASTA_DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
ARQ_BASE = os.path.join(PASTA_DADOS, "base_conhecimento.json")
ARQ_TEMAS = os.path.join(PASTA_DADOS, "temas.json")

# Campos que todo registro precisa ter, e o tipo esperado de cada um.
CAMPOS_OBRIGATORIOS = {
    "id": str,
    "tema": str,
    "pergunta": str,
    "palavras_chave": list,
    "orientacao": str,
    "referencia": dict,
    "data_verificacao": str,
}
PADRAO_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class ErroBase(Exception):
    """Erro que impede o uso da base (arquivo ausente, vazio ou ilegível)."""


def ler_json(caminho):
    if not os.path.exists(caminho):
        raise ErroBase(f"Arquivo não encontrado: {caminho}")
    # utf-8-sig aceita arquivos salvos com ou sem BOM (comum em editores do Windows)
    with open(caminho, encoding="utf-8-sig") as arq:
        conteudo = arq.read().strip()
    if not conteudo:
        raise ErroBase(f"Arquivo vazio: {caminho}")
    try:
        return json.loads(conteudo)
    except json.JSONDecodeError as erro:
        raise ErroBase(f"JSON inválido em {caminho} (linha {erro.lineno}): {erro.msg}")


def carregar_temas(caminho=ARQ_TEMAS):
    temas = ler_json(caminho)
    if not isinstance(temas, dict) or not temas:
        raise ErroBase("O arquivo de temas deve conter um objeto com pelo menos um tema.")
    return temas


def validar_registro(reg, temas, ids_vistos):
    """Devolve a lista de problemas do registro (lista vazia = registro válido)."""
    if not isinstance(reg, dict):
        return ["registro não é um objeto JSON"]
    problemas = []
    for campo, tipo in CAMPOS_OBRIGATORIOS.items():
        valor = reg.get(campo)
        if valor is None or (isinstance(valor, (str, list, dict)) and not valor):
            problemas.append(f"campo obrigatório ausente ou vazio: '{campo}'")
        elif not isinstance(valor, tipo):
            problemas.append(f"campo '{campo}' deveria ser {tipo.__name__}")
    if problemas:
        return problemas
    if reg["id"] in ids_vistos:
        problemas.append(f"id duplicado: {reg['id']}")
    if reg["tema"] not in temas:
        problemas.append(f"tema inexistente em temas.json: {reg['tema']}")
    elif reg.get("subtema") and reg["subtema"] not in temas[reg["tema"]].get("subtemas", {}):
        problemas.append(f"subtema inexistente: {reg['subtema']}")
    if not reg["referencia"].get("url") or not reg["referencia"].get("titulo"):
        problemas.append("referência precisa de 'titulo' e 'url'")
    if not PADRAO_DATA.match(reg["data_verificacao"]):
        problemas.append("data_verificacao deve estar no formato AAAA-MM-DD")
    return problemas


def carregar_base(caminho=ARQ_BASE, temas=None):
    """Lê a base e devolve (registros_validos, avisos)."""
    if temas is None:
        temas = carregar_temas()
    dados = ler_json(caminho)
    if not isinstance(dados, list) or not dados:
        raise ErroBase("A base deve ser uma lista com pelo menos um registro.")

    registros, avisos, ids_vistos = [], [], set()
    for posicao, reg in enumerate(dados, start=1):
        problemas = validar_registro(reg, temas, ids_vistos)
        if problemas:
            ident = reg.get("id", f"posição {posicao}") if isinstance(reg, dict) else f"posição {posicao}"
            avisos.append(f"Registro {ident} ignorado: " + "; ".join(problemas))
            continue
        reg.setdefault("subtema", "")
        reg.setdefault("passos", [])
        reg.setdefault("relacionados", [])
        reg.setdefault("requer_confirmacao", True)
        ids_vistos.add(reg["id"])
        registros.append(reg)

    if not registros:
        raise ErroBase("Nenhum registro válido na base.")

    # Relacionamentos que apontam para ids inexistentes são removidos.
    for reg in registros:
        invalidos = [r for r in reg["relacionados"] if r not in ids_vistos]
        if invalidos:
            avisos.append(f"Registro {reg['id']}: relacionados inexistentes ignorados {invalidos}")
            reg["relacionados"] = [r for r in reg["relacionados"] if r in ids_vistos]
    return registros, avisos


def indexar(registros):
    """Cria dicionários de acesso rápido: por id e por tema -> subtema -> lista."""
    por_id = {reg["id"]: reg for reg in registros}
    por_tema = {}
    for reg in registros:
        por_tema.setdefault(reg["tema"], {}).setdefault(reg["subtema"], []).append(reg)
    return por_id, por_tema
