"""Representação de um registro da base de conhecimento (POO)."""


class Orientacao:
    def __init__(self, dados):
        self.id = int(dados["id"])
        self.categoria = str(dados["categoria"])
        self.titulo = str(dados["titulo"])
        self.palavras_chave = list(dados["palavras_chave"])
        self.resposta = str(dados["resposta"])
        self.documentos = list(dados["documentos"])
        self.onde = str(dados["onde"])
        self.fonte = str(dados["fonte"])
        self.verificado_em = str(dados["verificado_em"])

    def exibir(self):
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(self.resposta)
        print("Documentos e requisitos:")
        for documento in self.documentos:
            print("  -", documento)
        print("Onde:", self.onde)
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print("Aviso: este assistente NÃO é um canal oficial.")
