"""Testes técnicos opcionais. Execute: python testes_automaticos.py"""
import csv
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from orientacao import Orientacao
from base_conhecimento import BaseConhecimento, normalizar
from assistente import Assistente

ORIGEM = Path(__file__).resolve().parent / 'data' / 'base_conhecimento.json'


class TestesCitizenAssist(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pasta = Path(self.tmp.name)
        self.base_json = self.pasta / 'base_conhecimento.json'
        self.base_json.write_text(ORIGEM.read_text(encoding='utf-8'), encoding='utf-8')
        self.base = BaseConhecimento(self.base_json)
        self.assertTrue(self.base.carregar())
        self.bot = Assistente('Teste', self.base, self.pasta)

    def test_01_11_registros_e_3_categorias(self):
        self.assertGreaterEqual(len(self.base.orientacoes), 10)
        self.assertGreaterEqual(len(self.base.categorias()), 3)

    def test_02_campos_e_fontes(self):
        for o in self.base.orientacoes:
            self.assertGreaterEqual(len(o.palavras_chave), 3)
            self.assertTrue(o.fonte.startswith('https://'))
            self.assertRegex(o.verificado_em, r'^\d{4}-\d{2}-\d{2}$')

    def test_03_normalizacao(self):
        self.assertEqual(normalizar('  Cartão do SUS?!'), ' cartao do sus ')

    def test_04_pontuacao_e_confianca_alta(self):
        resultados = self.base.buscar('Como faço a carteira de trabalho digital?')
        self.assertEqual(resultados[0][1].id, 2)
        self.assertGreaterEqual(resultados[0][0], 6)

    def test_05_busca_media(self):
        resultados = self.base.buscar('Onde vejo vagas de emprego?')
        self.assertEqual(resultados[0][1].id, 5)

    def test_06_sem_resultados(self):
        self.assertEqual(self.base.buscar('qual e o meu signo astrologico'), [])

    def test_07_ordenacao_por_pontos(self):
        resultados = self.base.buscar('jovem aprendiz aprendizagem profissional')
        self.assertEqual([p for p, _ in resultados], sorted([p for p, _ in resultados], reverse=True))

    def test_08_categoria(self):
        self.assertEqual(len(self.base.por_categoria('Trabalho')), 3)

    def test_09_bloqueio_de_pii(self):
        self.assertTrue(self.bot.contem_dado_pessoal('meu cpf e 123.456.789-00'))
        self.assertTrue(self.bot.contem_dado_pessoal('meu email e abc@teste.com'))
        self.assertFalse(self.bot.contem_dado_pessoal('como fazer carteira de trabalho'))

    def test_10_bloqueio_nao_salva_historico(self):
        self.bot.registrar('pergunta', '123.456.789-00', None)
        self.assertEqual(len(self.bot.historico), 0)

    def test_11_registro_salva_json(self):
        self.bot.registrar('pergunta','Quero jovem aprendiz', self.base.orientacoes[5], True, 2)
        gravados = json.loads((self.pasta/'historico.json').read_text(encoding='utf-8'))
        self.assertEqual(gravados[0]['tentativas'], 2)
        self.assertEqual(gravados[0]['origem'], 'pergunta')

    def test_12_csv(self):
        self.bot.registrar('pergunta', 'Preciso de emprego', self.base.orientacoes[4], True)
        self.assertTrue(self.bot.exportar_csv())
        with (self.pasta/'atendimentos.csv').open(encoding='utf-8-sig',newline='') as f:
            linhas = list(csv.DictReader(f))
        self.assertEqual(len(linhas),1)
        self.assertEqual(linhas[0]['encontrou'], 'True')

    def test_13_indicadores_sem_crash(self):
        with redirect_stdout(StringIO()) as buf:
            self.bot.indicadores()
        self.assertIn('sem dados',buf.getvalue())

    def test_14_json_ausente_nao_trava(self):
        b = BaseConhecimento(self.pasta / 'arquivo_inexistente.json')
        with redirect_stdout(StringIO()):
            ok = b.carregar()
        self.assertFalse(ok)
        self.assertEqual(b.orientacoes, [])

    def test_15_json_corrompido_nao_trava(self):
        caminho = self.pasta / 'errado.json'
        caminho.write_text('{quebrado', encoding='utf-8')
        b = BaseConhecimento(caminho)
        with redirect_stdout(StringIO()):
            ok = b.carregar()
        self.assertFalse(ok)

    def test_16_exibir_fontes_e_aviso(self):
        with redirect_stdout(StringIO()) as buf:
            self.base.orientacoes[0].exibir()
        self.assertIn('não', buf.getvalue().lower())
        self.assertIn('Fonte:',buf.getvalue())

    def test_17_teste_palavra_chave_ao_vivo(self):
        pergunta = 'registro laboral virtual'
        self.assertEqual(self.base.buscar(pergunta), [])
        data = json.loads(self.base_json.read_text(encoding='utf-8'))
        data[1]['palavras_chave'].append(pergunta)
        self.base_json.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
        self.base.carregar()
        self.assertEqual(self.base.buscar(pergunta)[0][1].id, 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
