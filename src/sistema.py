"""Citizen Assist AI – assistente textual de orientação cidadã.

Execute a partir da raiz do repositório:
    python src/sistema.py
"""

import sys

from base import ErroBase, carregar_base, carregar_temas, indexar
from busca import buscar
from grafo import construir_grafo, sugerir_relacionados, temas_vizinhos
from respostas import (AVISO_NAO_OFICIAL, MENSAGENS_ENTRADA, MODELOS, formatar,
                       mensagem_sem_resposta)

LINHA = "-" * 60


class Assistente:
    def __init__(self, temas, registros):
        self.temas = temas
        self.registros = registros
        self.por_id, self.por_tema = indexar(registros)
        self.grafo = construir_grafo(temas, registros)
        self.modelo = "B"

    # ---------------- entrada ----------------
    @staticmethod
    def ler(prompt):
        try:
            return input(prompt).replace("﻿", "").strip()
        except EOFError:
            return "0"

    def escolher(self, opcoes, titulo, permitir_voltar=True):
        """Mostra uma lista numerada e devolve o item escolhido (ou None para voltar)."""
        while True:
            print(f"\n{titulo}")
            for i, (rotulo, _) in enumerate(opcoes, start=1):
                print(f"  {i}. {rotulo}")
            if permitir_voltar:
                print("  0. Voltar")
            resp = self.ler("Escolha um número: ")
            if resp == "0" and permitir_voltar:
                return None
            if not resp:
                print("Entrada vazia. Digite o número de uma das opções.")
            elif not resp.isdigit() or not 1 <= int(resp) <= len(opcoes):
                print(f"Opção '{resp}' não existe. Digite um número de 1 a {len(opcoes)}"
                      + (" ou 0 para voltar." if permitir_voltar else "."))
            else:
                return opcoes[int(resp) - 1][1]

    # ---------------- saída ----------------
    def mostrar(self, reg):
        print(LINHA)
        print(f"[{reg['id']}] {reg['pergunta']}")
        print(LINHA)
        print(formatar(reg, self.modelo))
        print(LINHA)
        self.continuar(reg)

    def continuar(self, reg):
        """Oferece assuntos relacionados para continuar a consulta (navegação pelo grafo)."""
        sugestoes = sugerir_relacionados(self.grafo, self.por_id, reg["id"])
        vizinhos = temas_vizinhos(self.grafo, reg["tema"])
        opcoes = [(f"{s['pergunta']} [{s['id']}]", ("reg", s)) for s in sugestoes]
        opcoes += [(f"Ver tema relacionado: {self.temas[t]['nome']}", ("tema", t)) for t in vizinhos]
        escolha = self.escolher(opcoes, "Quer continuar por um assunto relacionado?")
        if escolha is None:
            return
        tipo, alvo = escolha
        if tipo == "reg":
            self.mostrar(alvo)
        else:
            self.navegar_tema(alvo)

    # ---------------- fluxos ----------------
    def navegar_temas(self):
        opcoes = [(f"{info['nome']} – {info['descricao']}", tema) for tema, info in self.temas.items()
                  if tema in self.por_tema]
        tema = self.escolher(opcoes, "TEMAS DISPONÍVEIS")
        if tema:
            self.navegar_tema(tema)

    def navegar_tema(self, tema):
        info = self.temas[tema]
        opcoes = []
        for subtema, regs in self.por_tema.get(tema, {}).items():
            nome_sub = info["subtemas"].get(subtema, "Geral")
            opcoes += [(f"{nome_sub}: {r['pergunta']}", r) for r in regs]
        reg = self.escolher(opcoes, f"{info['nome'].upper()} – escolha uma orientação")
        if reg:
            self.mostrar(reg)

    def perguntar(self):
        print("\nDigite sua pergunta (não informe CPF, telefone, e-mail ou outros dados pessoais).")
        pergunta = self.ler("> ")
        resultado = buscar(pergunta, self.registros)
        status = resultado["status"]

        if status in MENSAGENS_ENTRADA:
            print(MENSAGENS_ENTRADA[status])
        elif status == "sem_resposta":
            print(mensagem_sem_resposta(self.temas))
        elif status == "ambigua":
            print("Sua pergunta pode se referir a mais de um assunto.")
            opcoes = [(f"{r['pergunta']} [{r['id']}]", r) for _, r in resultado["resultados"]]
            reg = self.escolher(opcoes, "Qual destes você procura?")
            if reg:
                self.mostrar(reg)
        else:
            self.mostrar(resultado["resultados"][0][1])

    def buscar_por_id(self):
        ident = self.ler("Digite o identificador (ex.: DOC01): ").upper()
        if not ident:
            print("Entrada vazia.")
        elif ident not in self.por_id:
            print(f"Não existe orientação com o identificador '{ident}'. "
                  f"Exemplos válidos: {', '.join(sorted(self.por_id)[:5])}...")
        else:
            self.mostrar(self.por_id[ident])

    def trocar_modelo(self):
        self.modelo = "A" if self.modelo == "B" else "B"
        print(f"Modelo de resposta agora: {MODELOS[self.modelo]['nome']}")

    def sobre(self):
        print(LINHA)
        print(AVISO_NAO_OFICIAL)
        print("- As respostas vêm de uma base com fontes públicas identificadas e data de conferência.")
        print("- O assistente não inventa respostas: se não encontrar, ele avisa.")
        print("- Nenhum dado pessoal é pedido nem armazenado.")
        print("- Leis e procedimentos mudam: confirme sempre no canal oficial.")
        print(f"- Base carregada: {len(self.registros)} orientações em {len(self.por_tema)} temas.")
        print(LINHA)

    def executar(self):
        print("=" * 60)
        print(" CITIZEN ASSIST AI – Orientação cidadã (protótipo)")
        print("=" * 60)
        print(AVISO_NAO_OFICIAL)
        acoes = {
            "1": ("Navegar por temas", self.navegar_temas),
            "2": ("Fazer uma pergunta", self.perguntar),
            "3": ("Buscar orientação pelo identificador", self.buscar_por_id),
            "4": ("Trocar modelo de resposta (A direto / B estruturado)", self.trocar_modelo),
            "5": ("Sobre o assistente e seus limites", self.sobre),
        }
        while True:
            print("\nMENU PRINCIPAL")
            for chave, (rotulo, _) in acoes.items():
                print(f"  {chave}. {rotulo}")
            print("  0. Sair")
            opcao = self.ler("Escolha uma opção: ")
            if opcao == "0":
                print("Até logo!")
                return
            if not opcao:
                print("Entrada vazia. Digite o número de uma opção.")
            elif opcao not in acoes:
                print(f"Opção '{opcao}' não existe. Escolha entre 0 e {len(acoes)}.")
            else:
                acoes[opcao][1]()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        temas = carregar_temas()
        registros, avisos = carregar_base(temas=temas)
    except ErroBase as erro:
        print(f"Não foi possível carregar a base de conhecimento: {erro}")
        print("Verifique os arquivos da pasta data/ e tente novamente.")
        sys.exit(1)
    for aviso in avisos:
        print(f"[aviso] {aviso}")
    try:
        Assistente(temas, registros).executar()
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")


if __name__ == "__main__":
    main()
