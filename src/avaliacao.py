"""Executa as perguntas de teste, calcula indicadores e compara os modelos de resposta.

Uso (na raiz do repositório):
    python src/avaliacao.py

Gera:
    docs/resultados_testes.csv   – registro de cada teste
    docs/resultados_testes.md    – tabela, taxa de acerto e tempo médio
    docs/comparacao_modelos.md   – comparação objetiva Modelo A x Modelo B
"""

import csv
import json
import os
import statistics
import sys
import time

from base import PASTA_DADOS, carregar_base, carregar_temas, indexar
from busca import buscar
from respostas import MODELOS, avaliar_texto, formatar

RAIZ = os.path.dirname(PASTA_DADOS)
PASTA_DOCS = os.path.join(RAIZ, "docs")
REPETICOES = 50  # cada consulta é repetida para medir o tempo com mais estabilidade

STATUS_INVALIDOS = {"vazia", "curta", "invalida", "sem_termos", "dados_pessoais"}


def classificar(resultado):
    status = resultado["status"]
    if status in STATUS_INVALIDOS:
        return "ENTRADA_INVALIDA", status
    if status == "sem_resposta":
        return "SEM_RESPOSTA", status
    ids = [r["id"] for _, r in resultado["resultados"]]
    if status == "ambigua":
        return "AMBIGUA", "opções: " + ", ".join(ids)
    return ids[0], f"pontos: {resultado['resultados'][0][0]}"


def executar_testes(registros):
    with open(os.path.join(PASTA_DADOS, "perguntas_teste.json"), encoding="utf-8") as arq:
        testes = json.load(arq)

    linhas = []
    for t in testes:
        inicio = time.perf_counter()
        for _ in range(REPETICOES):
            resultado = buscar(t["pergunta"], registros)
        tempo_ms = (time.perf_counter() - inicio) * 1000 / REPETICOES

        obtido, detalhe = classificar(resultado)
        acerto = obtido == t["esperado"]
        if acerto and obtido == "AMBIGUA" and t.get("candidatos"):
            ids = {r["id"] for _, r in resultado["resultados"]}
            acerto = set(t["candidatos"]) <= ids
        linhas.append({
            "id": t["id"], "tipo": t["tipo"], "pergunta": t["pergunta"].strip() or "(vazia)",
            "esperado": t["esperado"], "obtido": obtido, "detalhe": detalhe,
            "acerto": "ACERTO" if acerto else "ERRO", "tempo_ms": round(tempo_ms, 4),
        })
    return linhas


def salvar_resultados(linhas):
    os.makedirs(PASTA_DOCS, exist_ok=True)
    with open(os.path.join(PASTA_DOCS, "resultados_testes.csv"), "w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=list(linhas[0].keys()), delimiter=";")
        escritor.writeheader()
        escritor.writerows(linhas)

    total = len(linhas)
    acertos = sum(1 for l in linhas if l["acerto"] == "ACERTO")
    tempos = [l["tempo_ms"] for l in linhas]
    taxa = 100 * acertos / total

    por_tipo = {}
    for l in linhas:
        grupo = "limitacao" if l["tipo"].startswith("limitacao") else l["tipo"]
        a, n = por_tipo.get(grupo, (0, 0))
        por_tipo[grupo] = (a + (l["acerto"] == "ACERTO"), n + 1)

    md = ["# Resultados dos testes", "",
          "Arquivo gerado automaticamente por `python src/avaliacao.py`.", "",
          "| ID | Tipo | Pergunta | Esperado | Obtido | Detalhe | Resultado | Tempo (ms) |",
          "|---|---|---|---|---|---|---|---|"]
    for l in linhas:
        md.append(f"| {l['id']} | {l['tipo']} | {l['pergunta']} | {l['esperado']} | {l['obtido']} "
                  f"| {l['detalhe']} | {l['acerto']} | {l['tempo_ms']:.4f} |")
    md += ["", "## Indicadores", "",
           f"- Perguntas testadas: **{total}**",
           f"- Acertos: **{acertos}** | Erros: **{total - acertos}**",
           f"- Taxa de acerto: **{taxa:.1f}%**",
           f"- Tempo médio de consulta: **{statistics.mean(tempos):.4f} ms** "
           f"(mediana {statistics.median(tempos):.4f} ms; máximo {max(tempos):.4f} ms; "
           f"média de {REPETICOES} repetições por pergunta)", "",
           "### Acerto por tipo de pergunta", "", "| Tipo | Acertos | Total | Taxa |", "|---|---|---|---|"]
    for grupo, (a, n) in por_tipo.items():
        md.append(f"| {grupo} | {a} | {n} | {100 * a / n:.1f}% |")
    with open(os.path.join(PASTA_DOCS, "resultados_testes.md"), "w", encoding="utf-8") as arq:
        arq.write("\n".join(md) + "\n")
    return total, acertos, taxa, statistics.mean(tempos)


def comparar_modelos(linhas, por_id):
    """Aplica os dois modelos às respostas encontradas e mede critérios objetivos."""
    criterios = ["cita_fonte", "titulo_fonte", "data_verificacao", "passos",
                 "aviso_nao_oficial", "aviso_confirmacao"]
    regs = [por_id[l["obtido"]] for l in linhas if l["obtido"] in por_id]
    tabela = {}
    for modelo in MODELOS:
        avals = [avaliar_texto(formatar(r, modelo), r) for r in regs]
        tabela[modelo] = {c: 100 * sum(a[c] for a in avals) / len(avals) for c in criterios}
        tabela[modelo]["palavras"] = statistics.mean(a["palavras"] for a in avals)
        tabela[modelo]["palavras_por_frase"] = statistics.mean(a["palavras_por_frase"] for a in avals)

    nomes = {
        "cita_fonte": "Mostra o link da fonte",
        "titulo_fonte": "Mostra o nome da fonte (lei/página)",
        "data_verificacao": "Mostra a data de verificação",
        "passos": "Mostra passos numerados",
        "aviso_nao_oficial": "Avisa que não é canal oficial",
        "aviso_confirmacao": "Pede confirmação quando necessário",
    }
    md = ["# Comparação dos modelos de resposta", "",
          "Arquivo gerado por `python src/avaliacao.py`. Os dois modelos foram aplicados às "
          f"{len(regs)} perguntas de teste que retornaram uma orientação.", "",
          f"| Critério | {MODELOS['A']['nome']} | {MODELOS['B']['nome']} |", "|---|---|---|"]
    for c in criterios:
        md.append(f"| {nomes[c]} | {tabela['A'][c]:.0f}% | {tabela['B'][c]:.0f}% |")
    md.append(f"| Média de palavras por resposta | {tabela['A']['palavras']:.0f} | {tabela['B']['palavras']:.0f} |")
    md.append(f"| Média de palavras por frase | {tabela['A']['palavras_por_frase']:.1f} | "
              f"{tabela['B']['palavras_por_frase']:.1f} |")
    if regs:
        md += ["", f"## Exemplo ({regs[0]['id']})", "", "**Modelo A**", "", "```",
               formatar(regs[0], "A"), "```", "", "**Modelo B**", "", "```", formatar(regs[0], "B"), "```"]
    with open(os.path.join(PASTA_DOCS, "comparacao_modelos.md"), "w", encoding="utf-8") as arq:
        arq.write("\n".join(md) + "\n")
    return tabela


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    temas = carregar_temas()
    registros, avisos = carregar_base(temas=temas)
    for aviso in avisos:
        print(f"[aviso] {aviso}")
    por_id, _ = indexar(registros)

    linhas = executar_testes(registros)
    for l in linhas:
        print(f"{l['id']} {l['acerto']:6} esperado={l['esperado']:16} obtido={l['obtido']:16} | {l['pergunta']}")
    total, acertos, taxa, tempo = salvar_resultados(linhas)
    comparar_modelos(linhas, por_id)
    print(f"\nTaxa de acerto: {acertos}/{total} = {taxa:.1f}%")
    print(f"Tempo médio de consulta: {tempo:.4f} ms")
    print("Relatórios gravados em docs/resultados_testes.md, docs/resultados_testes.csv "
          "e docs/comparacao_modelos.md")


if __name__ == "__main__":
    main()
