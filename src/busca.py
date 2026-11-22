"""Validação da pergunta e busca por palavras-chave com pontuação.

Estratégia (explicada no README):
1. A pergunta é normalizada: minúsculas, sem acentos e sem pontuação.
2. Palavras sem significado (stopwords: "o", "de", "como"...) são removidas.
3. Cada palavra vira um "radical" simples (primeiras 6 letras, sem plural),
   para que "documentos" e "documento" se encontrem.
4. Cada registro recebe pontos:
   +3 por radical da pergunta que aparece nas palavras-chave do registro;
   +2 por expressão de várias palavras encontrada inteira (ex.: "segunda via");
   +1 por radical que aparece só no texto da pergunta cadastrada.
5. Abaixo de LIMIAR_MINIMO não há resposta confiável.
   Se o 2º colocado tiver pelo menos RAZAO_AMBIGUIDADE da nota do 1º,
   a consulta é tratada como ambígua e o usuário escolhe entre as opções.
"""

import re
import unicodedata

LIMIAR_MINIMO = 3
RAZAO_AMBIGUIDADE = 0.8
MAX_OPCOES = 4

STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas", "por", "para", "pra", "com", "sem", "e", "ou",
    "que", "qual", "quais", "quem", "como", "onde", "quando", "porque", "se", "me",
    "meu", "minha", "meus", "minhas", "eu", "voce", "ele", "ela", "isso", "esse",
    "essa", "este", "esta", "ao", "aos", "sobre", "posso", "pode", "preciso", "quero",
    "ter", "tem", "tenho", "fazer", "faco", "sao", "ser", "e", "ja", "mais", "muito",
    "algo", "alguma", "algum", "gostaria", "saber", "favor", "ola", "oi", "bom", "dia",
}

# Verbos que aparecem em perguntas de qualquer assunto ("tirar passaporte", "tirar CPF").
# Valem só 1 ponto, para não decidirem a resposta sozinhos (versão 2 da busca).
GENERICOS = {"tirar", "pedir", "obter", "consul", "solici", "emitir", "receber", "ver"}

PADROES_DADOS_PESSOAIS = [
    re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),          # CPF
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),                    # e-mail
    re.compile(r"\(?\b\d{2}\)?\s?9?\d{4}-?\d{4}\b"),           # telefone
]


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return " ".join(texto.split())


def radical(palavra):
    if len(palavra) > 4 and palavra.endswith("s"):
        palavra = palavra[:-1]
    return palavra[:6]


def radicais(texto):
    return {radical(p) for p in normalizar(texto).split() if p not in STOPWORDS}


def validar_entrada(texto):
    """Devolve None se a entrada é válida ou um código de problema."""
    if texto is None or not texto.strip():
        return "vazia"
    if any(p.search(texto) for p in PADROES_DADOS_PESSOAIS):
        return "dados_pessoais"
    norm = normalizar(texto)
    if not re.search(r"[a-z]", norm):
        return "invalida"
    if len(norm) < 3:
        return "curta"
    if not radicais(texto):
        return "sem_termos"
    return None


def pontuar(consulta, registro):
    """Calcula a pontuação de um registro para a consulta."""
    q_norm = " " + normalizar(consulta) + " "
    q_rad = radicais(consulta)

    rad_simples, rad_parciais, frases = set(), set(), 0
    for chave in registro["palavras_chave"]:
        chave_norm = normalizar(chave)
        if " " in chave_norm:
            rad_parciais |= radicais(chave_norm)
            if f" {chave_norm} " in q_norm:
                frases += 1
        else:
            rad_simples |= radicais(chave_norm)

    rad_pergunta = radicais(registro["pergunta"])
    pontos = 2 * frases
    for r in q_rad:
        if r in GENERICOS and (r in rad_simples or r in rad_parciais or r in rad_pergunta):
            pontos += 1          # verbo genérico: indica pouco sobre o assunto
        elif r in rad_simples:
            pontos += 3          # palavra-chave própria do registro
        elif r in rad_parciais:
            pontos += 2          # palavra solta de uma expressão ("receita" de "receita federal")
        elif r in rad_pergunta:
            pontos += 1          # aparece só no texto da pergunta cadastrada
    return pontos


def buscar(consulta, registros):
    """Busca a consulta na base.

    Retorna um dicionário com:
      status: "ok" | "ambigua" | "sem_resposta" | <código de entrada inválida>
      resultados: lista de (pontos, registro), do melhor para o pior
    """
    problema = validar_entrada(consulta)
    if problema:
        return {"status": problema, "resultados": []}

    pontuados = [(pontuar(consulta, reg), reg) for reg in registros]
    # Ordena por pontos (maior primeiro); empate desempata pelo id, para ser determinístico.
    pontuados = sorted((p for p in pontuados if p[0] >= LIMIAR_MINIMO),
                       key=lambda p: (-p[0], p[1]["id"]))
    if not pontuados:
        return {"status": "sem_resposta", "resultados": []}

    melhor = pontuados[0][0]
    proximos = [p for p in pontuados if p[0] >= melhor * RAZAO_AMBIGUIDADE]
    if len(proximos) > 1:
        return {"status": "ambigua", "resultados": proximos[:MAX_OPCOES]}
    return {"status": "ok", "resultados": pontuados[:MAX_OPCOES]}
