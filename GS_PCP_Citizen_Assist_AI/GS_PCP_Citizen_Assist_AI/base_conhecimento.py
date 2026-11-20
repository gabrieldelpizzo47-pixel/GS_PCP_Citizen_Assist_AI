"""Carregamento de JSON e busca por pontuação (sem IA generativa)."""
import json
import re
import unicodedata
from pathlib import Path
from orientacao import Orientacao


def normalizar(texto):
    """Remove acentos/pontuação; devolve palavras minúsculas com bordas espaços."""
    texto = unicodedata.normalize("NFD", str(texto).lower().strip())
    texto = "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    OBRIGATORIOS = {"id", "categoria", "titulo", "palavras_chave", "resposta",
                    "documentos", "onde", "fonte", "verificado_em"}

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []  # Composição: objetos Orientacao pertencem à BaseConhecimento

    def carregar(self):
        self.orientacoes = []
        try:
            with self.caminho.open("r", encoding="utf-8") as arq:
                registros = json.load(arq)
            if not isinstance(registros, list):
                raise ValueError("o JSON deve conter uma lista")
            ids = set()
            objetos = []
            for indice, item in enumerate(registros, start=1):
                if not isinstance(item, dict) or not self.OBRIGATORIOS.issubset(item):
                    raise ValueError(f"registro {indice} sem campos obrigatórios")
                if not isinstance(item["palavras_chave"], list) or len(item["palavras_chave"]) < 3:
                    raise ValueError(f"registro {indice} exige 3 palavras-chave")
                if not isinstance(item["documentos"], list) or not item["categoria"] or not item["titulo"]:
                    raise ValueError(f"registro {indice} possui campos inválidos")
                obj = Orientacao(item)
                if obj.id in ids:
                    raise ValueError(f"ID repetido: {obj.id}")
                ids.add(obj.id)
                objetos.append(obj)
            self.orientacoes = objetos
            return True
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as erro:
            print(f"Aviso: não foi possível carregar a base ({erro}). O programa continuará sem registros.")
            return False

    def categorias(self):
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """+3 por expressão-chave presente; +1 por palavra única >=4 no título."""
        p = normalizar(pergunta)
        titulo = normalizar(orientacao.titulo)
        pontos = 0
        for chave in orientacao.palavras_chave:
            chave_norm = normalizar(chave).strip()
            if chave_norm and f" {chave_norm} " in p:
                pontos += 3
        for palavra in set(p.strip().split()):
            if len(palavra) >= 4 and f" {palavra} " in titulo:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        """Lista de tuplas (pontos, orientação), ordem decrescente; só pontos >=3."""
        resultados = [(self.pontuar(pergunta, o), o) for o in self.orientacoes]
        resultados = [(p, o) for p, o in resultados if p >= 3]
        return sorted(resultados, key=lambda item: (-item[0], item[1].titulo))
