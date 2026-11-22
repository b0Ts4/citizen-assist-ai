"""Organização hierárquica e grafo simples de assuntos.

Hierarquia: tema -> subtema -> registros (orientações).
Grafo: cada tema e cada registro é um nó; as arestas vêm do campo
"relacionados" (temas.json e base_conhecimento.json) e são tratadas
como não direcionadas (se A se relaciona com B, B se relaciona com A).
"""

from collections import deque


def construir_grafo(temas, registros):
    grafo = {}

    def ligar(a, b):
        grafo.setdefault(a, set()).add(b)
        grafo.setdefault(b, set()).add(a)

    for tema, info in temas.items():
        grafo.setdefault(f"tema:{tema}", set())
        for outro in info.get("relacionados", []):
            if outro in temas:
                ligar(f"tema:{tema}", f"tema:{outro}")
    for reg in registros:
        ligar(reg["id"], f"tema:{reg['tema']}")
        for rel in reg["relacionados"]:
            ligar(reg["id"], rel)
    return grafo


def temas_vizinhos(grafo, tema):
    return sorted(n[5:] for n in grafo.get(f"tema:{tema}", ()) if n.startswith("tema:"))


def sugerir_relacionados(grafo, por_id, reg_id, limite=3):
    """Sugestões de continuidade por busca em largura (BFS) a partir do registro.

    Primeiro vêm os registros ligados diretamente (distância 1), depois os
    que estão a dois passos (ex.: outros registros do mesmo tema).
    """
    visitados, fila, sugestoes = {reg_id}, deque([(reg_id, 0)]), []
    while fila and len(sugestoes) < limite:
        no, dist = fila.popleft()
        if dist >= 2:
            continue
        for viz in sorted(grafo.get(no, ())):
            if viz in visitados:
                continue
            visitados.add(viz)
            if viz in por_id:
                sugestoes.append(por_id[viz])
                if len(sugestoes) >= limite:
                    break
            fila.append((viz, dist + 1))
    return sugestoes
