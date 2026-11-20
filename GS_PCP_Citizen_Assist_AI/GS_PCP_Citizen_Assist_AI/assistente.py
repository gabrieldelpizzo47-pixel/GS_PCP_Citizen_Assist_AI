"""Atendimentos, navegação, histórico sem PII, indicadores e exportação CSV."""
import csv
import json
import time
from datetime import datetime
from pathlib import Path


class Assistente:
    CAMPOS = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
              "ajudou", "tentativas", "tempo_segundos"]

    def __init__(self, nome, base, pasta_dados):
        self.nome = nome
        self.base = base  # Composição: Assistente contém BaseConhecimento
        self.pasta = Path(pasta_dados)
        self.pasta.mkdir(parents=True, exist_ok=True)
        self.historico = self._ler_lista("historico.json")
        self.avaliacoes = self._ler_lista("avaliacoes.json")

    def _ler_lista(self, arquivo):
        try:
            with (self.pasta / arquivo).open("r", encoding="utf-8") as arq:
                dados = json.load(arq)
            return dados if isinstance(dados, list) else []
        except (OSError, ValueError, json.JSONDecodeError):
            print(f"Aviso: {arquivo} ausente/corrompido; iniciando lista vazia.")
            return []

    def _salvar_lista(self, arquivo, lista):
        try:
            (self.pasta / arquivo).write_text(json.dumps(lista, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except OSError as erro:
            print("Não foi possível salvar", arquivo, ":", erro)

    @staticmethod
    def contem_dado_pessoal(pergunta):
        """Regra da atividade: rejeitar @ ou >=8 dígitos, mesmo com pontuação."""
        return "@" in pergunta or sum(ch.isdigit() for ch in pergunta) >= 8

    @staticmethod
    def pedir_sim_nao(texto):
        while True:
            escolha = input(texto + " (s/n, 0 para voltar): ").strip().lower()
            if escolha == "s":
                return True
            if escolha == "n":
                return False
            if escolha == "0":
                return None
            print("Resposta inválida. Use s, n ou 0.")

    def registrar(self, origem, pergunta, orientacao=None, ajudou=None, tentativas=1, inicio=None):
        if self.contem_dado_pessoal(pergunta):
            return  # jamais armazenar pergunta bloqueada
        item = {
            "data": datetime.now().isoformat(timespec="seconds"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao.id if orientacao else None,
            "encontrou": orientacao is not None,
            "ajudou": ajudou,
            "tentativas": max(1, int(tentativas)),
            "tempo_segundos": round(max(0.0, time.time() - inicio), 1) if inicio is not None else 0.0,
        }
        self.historico.append(item)
        self._salvar_lista("historico.json", self.historico)
        return item

    def perguntar(self):
        print("\nFaça sua pergunta. Digite 0 para voltar.")
        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""
        while True:
            pergunta = input("Sua dúvida (0 para voltar): ").strip()
            if pergunta == "0":
                if tentativas and ultima_pergunta:
                    self.registrar("pergunta", ultima_pergunta, tentativas=tentativas, inicio=inicio)
                return
            if not pergunta:
                print("A pergunta não pode ficar vazia.")
                continue
            if self.contem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva sem dados pessoais.")
                continue  # Nem a entrada nem o histórico registram a pergunta
            tentativas += 1
            ultima_pergunta = pergunta
            resultados = self.base.buscar(pergunta)
            if not resultados:
                print("Não encontrei orientação. Tente outras palavras ou navegue pelas categorias.")
                continue
            pontos, orientacao = resultados[0]
            confianca = "ALTA" if pontos >= 6 else "MÉDIA"
            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            orientacao.exibir()
            if len(resultados) > 1:
                print("\nOutras opções relacionadas:")
                for score, alternativa in resultados[1:3]:
                    print(f"  - {alternativa.titulo}: {score} pontos")
            ajudou = self.pedir_sim_nao("Essa orientação respondeu sua dúvida?")
            self.registrar("pergunta", pergunta, orientacao, ajudou, tentativas, inicio)
            return

    def navegar(self):
        while True:
            categorias = self.base.categorias()
            print("\nCATEGORIAS (0 para voltar)")
            for i, cat in enumerate(categorias, 1):
                print(f"{i} - {cat}")
            escolha = input("Escolha: ").strip()
            if escolha == "0":
                return
            if not escolha.isdigit() or not (1 <= int(escolha) <= len(categorias)):
                print("Categoria inválida.")
                continue
            cat = categorias[int(escolha)-1]
            itens = self.base.por_categoria(cat)
            while True:
                print(f"\n{cat.upper()} (0 para voltar)")
                for i, o in enumerate(itens, 1):
                    print(f"{i} - {o.titulo}")
                op = input("Escolha orientação: ").strip()
                if op == "0":
                    break
                if not op.isdigit() or not (1 <= int(op) <= len(itens)):
                    print("Opção inválida.")
                    continue
                inicio = time.time()
                o = itens[int(op)-1]
                o.exibir()
                ajudou = self.pedir_sim_nao("Essa orientação respondeu sua dúvida?")
                self.registrar("categoria", o.titulo, o, ajudou, 1, inicio)

    def indicadores(self):
        n = len(self.historico)
        achados = sum(bool(item.get("encontrou")) for item in self.historico)
        avaliados = [item for item in self.historico if item.get("ajudou") is not None]
        uteis = sum(item.get("ajudou") is True for item in avaliados)
        tempos = [float(item.get("tempo_segundos", 0)) for item in self.historico]
        tentativas = [int(item.get("tentativas", 1)) for item in self.historico]
        facilidade = sum(self.avaliacoes) / len(self.avaliacoes) if self.avaliacoes else None
        print("\nINDICADORES")
        print("Atendimentos:", n)
        print(f"Resposta encontrada: {100*achados/n:.1f}%" if n else "Resposta encontrada: sem dados")
        print(f"Taxa de acerto percebido (ajudou): {100*uteis/len(avaliados):.1f}%" if avaliados else "Taxa de acerto percebido: sem respostas de avaliação")
        print(f"Tempo médio para encontrar informação: {sum(tempos)/n:.1f} s" if n else "Tempo médio: sem dados")
        print(f"Tentativas por atendimento: {sum(tentativas)/n:.2f}" if n else "Tentativas: sem dados")
        print(f"Facilidade de uso: {facilidade:.1f}/5" if facilidade is not None else "Facilidade de uso: sem avaliações")
        duvidas = [item["pergunta"] for item in self.historico if not item.get("encontrou")]
        print("Dúvidas sem solução:", "; ".join(duvidas) if duvidas else "nenhuma registrada")

    def exportar_csv(self):
        arquivo = self.pasta / "atendimentos.csv"
        try:
            with arquivo.open("w", encoding="utf-8-sig", newline="") as fp:
                escritor = csv.DictWriter(fp, fieldnames=self.CAMPOS)
                escritor.writeheader()
                escritor.writerows(self.historico)
            print(f"CSV exportado: {arquivo}")
            return True
        except OSError as erro:
            print("Falha na exportação:", erro)
            return False

    def avaliar_facilidade(self):
        while True:
            nota = input("\nFacilidade de uso: nota de 1 a 5 (0 para pular): ").strip()
            if nota == "0":
                break
            if nota in ("1", "2", "3", "4", "5"):
                self.avaliacoes.append(int(nota))
                self._salvar_lista("avaliacoes.json", self.avaliacoes)
                print("Obrigado pela avaliação!")
                break
            print("Digite uma nota de 1 a 5 ou 0 para pular.")
