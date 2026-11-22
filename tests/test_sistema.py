"""Testes unitários. Execute na raiz do repositório:
    python -m unittest discover -s tests -v
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from base import ErroBase, carregar_base, carregar_temas, indexar  # noqa: E402
from busca import buscar, normalizar, validar_entrada  # noqa: E402
from grafo import construir_grafo, sugerir_relacionados  # noqa: E402
from respostas import formatar  # noqa: E402


class TestBase(unittest.TestCase):
    def setUp(self):
        self.temas = carregar_temas()
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def arquivo(self, conteudo):
        caminho = os.path.join(self.tmp.name, "base.json")
        with open(caminho, "w", encoding="utf-8") as arq:
            arq.write(conteudo)
        return caminho

    def test_base_real_tem_minimos_exigidos(self):
        registros, avisos = carregar_base(temas=self.temas)
        self.assertGreaterEqual(len(registros), 15)
        self.assertGreaterEqual(len({r["tema"] for r in registros}), 3)
        self.assertEqual(avisos, [])

    def test_arquivo_ausente(self):
        with self.assertRaises(ErroBase):
            carregar_base(os.path.join(self.tmp.name, "nao_existe.json"), self.temas)

    def test_arquivo_vazio(self):
        with self.assertRaises(ErroBase):
            carregar_base(self.arquivo(""), self.temas)

    def test_json_invalido(self):
        with self.assertRaises(ErroBase):
            carregar_base(self.arquivo("[{"), self.temas)

    def test_registro_inconsistente_e_ignorado(self):
        bom = {"id": "X1", "tema": "documentos", "pergunta": "p", "palavras_chave": ["a"],
               "orientacao": "o", "referencia": {"titulo": "t", "url": "u"},
               "data_verificacao": "2026-01-01"}
        sem_fonte = dict(bom, id="X2", referencia={})
        tema_errado = dict(bom, id="X3", tema="inexistente")
        duplicado = dict(bom)
        registros, avisos = carregar_base(
            self.arquivo(json.dumps([bom, sem_fonte, tema_errado, duplicado])), self.temas)
        self.assertEqual([r["id"] for r in registros], ["X1"])
        self.assertEqual(len(avisos), 3)


class TestBusca(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temas = carregar_temas()
        cls.registros, _ = carregar_base(temas=cls.temas)

    def test_normalizar(self):
        self.assertEqual(normalizar("Certidão  de NASCIMENTO?"), "certidao de nascimento")

    def test_validacoes(self):
        self.assertEqual(validar_entrada(""), "vazia")
        self.assertEqual(validar_entrada("   "), "vazia")
        self.assertEqual(validar_entrada("123"), "invalida")
        self.assertEqual(validar_entrada("meu email é a@b.com"), "dados_pessoais")
        self.assertEqual(validar_entrada("o de a"), "sem_termos")
        self.assertIsNone(validar_entrada("como tirar cpf"))

    def test_resposta_direta(self):
        r = buscar("certidão de nascimento", self.registros)
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["resultados"][0][1]["id"], "DOC03")

    def test_sem_resposta(self):
        self.assertEqual(buscar("previsão do tempo para amanhã", self.registros)["status"], "sem_resposta")

    def test_regressao_falsos_positivos_v1(self):
        # Na versão 1 da busca estas perguntas eram respondidas (errado) com DOC02.
        for pergunta in ["receita de bolo de chocolate", "Como faço para tirar passaporte?"]:
            self.assertEqual(buscar(pergunta, self.registros)["status"], "sem_resposta", pergunta)

    def test_limitacao_conhecida_v2(self):
        # Limitação ainda aberta (documentada no README): "telefone" é palavra-chave de CON01.
        self.assertEqual(buscar("qual o telefone dos bombeiros", self.registros)["resultados"][0][1]["id"], "CON01")

    def test_ambigua(self):
        r = buscar("prioridade", self.registros)
        self.assertEqual(r["status"], "ambigua")
        self.assertGreater(len(r["resultados"]), 1)


class TestGrafoERespostas(unittest.TestCase):
    def test_sugestoes_e_formato(self):
        temas = carregar_temas()
        registros, _ = carregar_base(temas=temas)
        por_id, _ = indexar(registros)
        grafo = construir_grafo(temas, registros)
        sugestoes = sugerir_relacionados(grafo, por_id, "CON01")
        self.assertTrue(sugestoes)
        self.assertNotIn("CON01", [s["id"] for s in sugestoes])
        texto = formatar(por_id["CON01"], "B")
        self.assertIn(por_id["CON01"]["referencia"]["url"], texto)
        self.assertIn("não é canal oficial", texto.lower())


if __name__ == "__main__":
    unittest.main()
