"""Modelos de instrução de resposta (estratégias de prompt).

O protótipo não usa um modelo de IA externo: as "instruções" abaixo são
regras que o próprio código aplica para montar a resposta a partir do
registro encontrado. O texto de cada instrução está escrito como um prompt,
para que possa ser reutilizado caso um LLM seja conectado no futuro
(veja docs/prompts.md). Nenhum dos modelos cria informação: eles só
reorganizam o conteúdo verificado da base.
"""

import re

AVISO_NAO_OFICIAL = ("Este assistente é um protótipo educacional e NÃO é canal oficial "
                     "de nenhum órgão público.")

MODELOS = {
    "A": {
        "nome": "Modelo A – Resposta direta",
        "instrucao": (
            "Responda à pergunta do cidadão usando apenas a orientação do registro "
            "encontrado. Ao final, informe a fonte."
        ),
    },
    "B": {
        "nome": "Modelo B – Resposta estruturada com papel e limites",
        "instrucao": (
            "Você é um assistente de orientação cidadã, informativo e NÃO oficial. "
            "Use SOMENTE o registro verificado recebido; não acrescente regras, prazos "
            "ou valores. Responda em linguagem simples, com frases curtas, no formato: "
            "1) Resumo; 2) O que fazer (passos numerados); 3) Fonte com título e link; "
            "4) Data de verificação; 5) Aviso para confirmar requisitos no canal oficial "
            "quando a orientação puder mudar. Se não houver registro, diga que não sabe "
            "e sugira temas disponíveis."
        ),
    },
}


def formatar_modelo_a(reg):
    return (f"{reg['orientacao']}\n"
            f"Fonte: {reg['referencia']['url']}")


def formatar_modelo_b(reg):
    linhas = ["RESUMO", f"  {reg['orientacao']}"]
    if reg["passos"]:
        linhas.append("O QUE FAZER")
        linhas += [f"  {i}. {passo}" for i, passo in enumerate(reg["passos"], start=1)]
    linhas.append("FONTE")
    linhas.append(f"  {reg['referencia']['titulo']}")
    linhas.append(f"  {reg['referencia']['url']}")
    linhas.append(f"  Informação conferida em: {reg['data_verificacao']}")
    if reg["requer_confirmacao"]:
        linhas.append("ATENÇÃO: requisitos, taxas e prazos podem mudar ou variar por "
                      "estado/município. Confirme no canal oficial antes de ir.")
    linhas.append(f"({AVISO_NAO_OFICIAL})")
    return "\n".join(linhas)


FORMATADORES = {"A": formatar_modelo_a, "B": formatar_modelo_b}


def formatar(reg, modelo="B"):
    return FORMATADORES[modelo](reg)


MENSAGENS_ENTRADA = {
    "vazia": "Você não digitou nada. Escreva uma pergunta, por exemplo: 'como tirar o CPF?'.",
    "curta": "A pergunta ficou muito curta. Tente usar pelo menos uma palavra completa.",
    "invalida": "Não entendi a entrada. Use palavras, por exemplo: 'onde reclamar de uma empresa'.",
    "sem_termos": "Sua pergunta não tem palavras de assunto. Diga sobre o que quer saber "
                  "(ex.: 'certidão de nascimento').",
    "dados_pessoais": "Parece que você digitou um dado pessoal (CPF, e-mail ou telefone). "
                      "Não é preciso informar dados pessoais. A consulta não foi feita nem "
                      "registrada. Reescreva a pergunta sem esses dados.",
}


def mensagem_sem_resposta(temas):
    nomes = ", ".join(info["nome"] for info in temas.values())
    return ("Não encontrei uma orientação confiável na base para essa pergunta. "
            "Prefiro não responder a arriscar uma informação errada.\n"
            f"Temas disponíveis: {nomes}.\n"
            "Dica: tente outras palavras ou navegue pelos temas no menu. Para assuntos "
            "fora da base, procure o canal oficial do órgão responsável.")


# ---------- Critérios objetivos usados para comparar os modelos ----------

def avaliar_texto(texto, reg):
    sem_links = re.sub(r"https?://\S+", "", texto)  # os pontos das URLs não são fim de frase
    frases = [f for f in re.split(r"[.!?\n]+", sem_links) if len(f.split()) > 1]
    palavras = len(texto.split())
    return {
        "cita_fonte": reg["referencia"]["url"] in texto,
        "titulo_fonte": reg["referencia"]["titulo"] in texto,
        "data_verificacao": reg["data_verificacao"] in texto,
        "passos": bool(reg["passos"]) and "1." in texto,
        "aviso_nao_oficial": "não é canal oficial" in texto.lower(),
        "aviso_confirmacao": (not reg["requer_confirmacao"]) or "confirme" in texto.lower(),
        "palavras": palavras,
        "palavras_por_frase": round(palavras / max(len(frases), 1), 1),
    }
