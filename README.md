# Citizen Assist AI — Primeiro Emprego

**Global Solution 2026.2 | Pensamento Computacional e Automação com Python (PCP) | FIAP 1CC**

## Integrantes
- RM 572899 — Patrick Fernandes Martins Pais
- RM 570436 — Gabriel Del Pizzo Pintor
- RM 570540 — Ian Rodrigues Martins

**Público atendido:** jovens buscando o primeiro emprego, serviços documentais e qualificação profissional.

**Problema:** informações sobre documentação, vagas e oportunidades educacionais aparecem dispersas em vários portais. O sistema reúne orientações claras com referências oficiais para reduzir o tempo de busca, sem substituir os serviços públicos.

**ODS relacionados:** ODS 4 (Educação de Qualidade), ODS 8 (Trabalho Decente e Crescimento Econômico) e ODS 10 (Redução das Desigualdades).

## Como executar

Requer **Python 3.9+**, sem bibliotecas externas. No terminal, dentro da pasta do projeto:

```bash
python main.py
```

Menu: **1** pergunta livre; **2** navegação por categoria; **3** indicadores; **4** exportar CSV; **0** sair (com avaliação de facilidade de 1 a 5). Digite **0** nas telas de pergunta, categoria ou seleção para voltar.

## Estrutura

```text
citizen-assist-ai/
├── main.py                # menu e integração
├── orientacao.py          # classe Orientacao: atributos e exibir()
├── base_conhecimento.py   # classe BaseConhecimento: JSON, busca, pontuação
├── assistente.py          # classe Assistente: atendimento, histórico, indicadores, CSV
├── testes_automaticos.py  # testes técnicos adicionais (opcional)
├── README.md
├── TESTES_MANUAIS.md      # plano, resultados a preencher com testes reais
├── ROTEIRO_VIDEO.md       # apoio para a apresentação
├── ENTREGA_PORTAL_MODELO.txt
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    ├── avaliacoes.json
    └── atendimentos.csv
```

## Orientações da base e fontes

São **11 orientações** distribuídas em **3 categorias**: Documentos (4), Trabalho (3), Educação (4). Cada registro contém `id`, `categoria`, `titulo`, `palavras_chave` (mínimo 3), `resposta`, `documentos`, `onde`, `fonte`, `verificado_em`. As referências oficiais de Receita Federal, TSE, Ministério do Trabalho, MEC e Inep estão no próprio JSON, associadas a cada registro; consulta inicial realizada em **19/11/2026**. As orientações não afirmam que um serviço está aberto neste momento: prazos, regras e documentos devem ser checados na fonte.

## Programação orientada a objetos e composição

- `Orientacao`: um registro do JSON; `exibir()` apresenta resposta, documentos, local, fonte e data.
- `BaseConhecimento`: carrega e mantém uma **lista de objetos `Orientacao`**; contém `carregar`, `categorias`, `por_categoria`, `pontuar` e `buscar`.
- `Assistente`: possui uma **instância de `BaseConhecimento`** (`self.base`), além do histórico, com `perguntar`, `navegar`, `registrar`, `indicadores`, `exportar_csv`.
- `self`: referência ao objeto atual em cada método de instância. Exemplo: `self.orientacoes` é a lista de registros daquela base.
- O JSON é uma lista de **dicionários**. A busca gera lista de **tuplas** `(pontuacao, objeto_orientacao)`.

## Regra da busca inteligente

1. `normalizar()` converte perguntas, palavras-chave e títulos para minúsculas, remove acentos e pontuação e normaliza espaços.
2. `pontuar()` adiciona **+3 pontos** por palavra-chave ou expressão completa encontrada e **+1 ponto** para cada palavra distinta de 4 ou mais letras da pergunta presente no título.
3. `buscar()` filtra os resultados abaixo de 3 pontos e ordena por pontuação decrescente, retornando lista de tuplas `(pontos, orientacao)`.
4. **6+ pontos:** confiança ALTA; **3–5:** MÉDIA; **menos de 3:** sem resposta. Exibimos melhor resposta e até 2 alternativas.

**Exemplos:** `Como faço a carteira de trabalho digital?` encontra a orientação correspondente. `Qual meu signo astrológico?` não encontra. **A pontuação mede correspondência com palavras, não confiabilidade de uma informação.**

## Segurança, transparência e limitações

- Perguntas com `@` ou 8 ou mais dígitos (mesmo com sinais entre eles) são **recusadas e nunca entram no histórico**. O sistema não solicita CPF, nome, e-mail ou telefone.
- Toda resposta inclui a fonte, a data da consulta e o aviso: **“este assistente NÃO é um canal oficial”**.
- Valores vazios, opções de menu inválidas e respostas inválidas de sim/não não encerram o programa.
- JSON ausente, corrompido ou com registros incompletos não derruba o programa; o assistente permanece acessível sem registros.
- A busca é baseada em regras; pode não compreender sinônimos não cadastrados, e pode ter falsos positivos. As informações oficiais e os prazos mudam, por isso as fontes precisam ser consultadas.
- O sistema grava histórico **localmente**; não publica perguntas na internet nem conecta a APIs. Antes de subir histórico real ao GitHub, revise privacidade e remova dados pessoais. Preferencialmente, publique histórico vazio.

## Histórico, indicadores e exportação

Cada atendimento aceito é registrado em `data/historico.json` com `data`, `origem`, `pergunta`, `id_orientacao`, `encontrou`, `ajudou`, `tentativas` e `tempo_segundos`. Indicadores: percentual de respostas encontradas; percentual de usuários que responderam “ajudou” (entre os que avaliaram); tempo médio; tentativas por atendimento; média de facilidade (avaliação ao sair); dúvidas sem resposta. O arquivo `data/avaliacoes.json` guarda notas de facilidade sem nome. A opção 4 e a saída exportam `data/atendimentos.csv` via `csv.DictWriter`.

## Testes com usuários reais — PENDENTE

**Obrigatório antes da entrega:** testar com **ao menos 3 pessoas de fora da equipe e somar 10 atendimentos ou mais**. Em `TESTES_MANUAIS.md`, registre somente dados agregados e comentários anônimos reais, as dúvidas sem solução, as métricas obtidas e **pelo menos uma melhoria implementada** (por exemplo, nova palavra-chave). Não invente testes ou dados. Depois copie aqui os indicadores reais e a melhoria: 

- Participantes externos: **PENDENTE**
- Total de atendimentos: **PENDENTE**
- Resposta encontrada (%): **PENDENTE**
- Taxa de acerto percebido (%): **PENDENTE**
- Tempo médio: **PENDENTE**
- Tentativas médias: **PENDENTE**
- Facilidade média (1–5): **PENDENTE**
- Dúvidas não resolvidas: **PENDENTE**
- Ajuste feito após teste: **PENDENTE**

### Testes automatizados

Execute:

```bash
python testes_automaticos.py
```

Os testes técnicos cobrem estrutura do JSON, normalização, busca, pontuação, privacidade, histórico, CSV, base ausente ou corrompida e inclusão de nova palavra-chave. **Não substituem os testes com pessoas reais.**

## Demonstração e vídeo (PENDENTE)

O professor exige **vídeo técnico de 5 a 8 minutos, no YouTube não listado**, com o código e o terminal legíveis, fala de todos os participantes e alteração ao vivo de palavra-chave. Consulte `ROTEIRO_VIDEO.md` para todos os oito tópicos obrigatórios.

**Link do vídeo:** PENDENTE

**Integração com outras disciplinas:** não implementada nesta versão. O tema CitizenTech pode ser compartilhado, mas a busca por pontuação e a POO deste código são próprias desta disciplina.

## Entrega

Publicar repositório **público** no GitHub e vídeo **não listado** no YouTube. No Portal FIAP, enviar **apenas um `.txt`** com nome do assistente, público, nomes/RMs, URL do GitHub e URL do vídeo. Veja `ENTREGA_PORTAL_MODELO.txt`. Prazo no PDF: **19/11/2026 às 23h59**; caso o Portal mostre **23h55**, siga o horário mais cedo.
