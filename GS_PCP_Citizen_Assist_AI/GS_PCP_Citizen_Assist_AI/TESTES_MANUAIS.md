# Evidências — Citizen Assist AI (PCP)

## Testes técnicos

Execute `python testes_automaticos.py` e registre a saída verdadeira. As verificações automatizadas não substituem testes reais com pessoas.

## Casos funcionais para demonstrar

| Caso | Entrada | Esperado | Observado |
|---|---|---|---|
| Busca com confiança alta | `Como faço a carteira de trabalho digital?` | Carteira de Trabalho Digital, fontes e aviso | PENDENTE |
| Busca sem resultado | `Qual é meu signo astrológico?` | Não encontrei; solicitar novas palavras | PENDENTE |
| Dados pessoais | `Meu CPF é 123.456.789-00` | Bloquear e não registrar | PENDENTE |
| E-mail | `meu@email.com` | Bloquear e não registrar | PENDENTE |
| Navegação | Menu 2, selecionar categoria e orientação | Exibir resposta completa | PENDENTE |
| Entrada inválida | `abc`, `99`, texto vazio, resposta `x` para s/n | Repetir a pergunta e não encerrar | PENDENTE |
| CSV | Menu 4 | Exportar data/atendimentos.csv | PENDENTE |
| Base ausente/corrompida | Renomear temporariamente JSON ou inserir JSON inválido | Programa não encerra abruptamente | PENDENTE |
| Melhoria ao vivo | Antes: `registro laboral virtual`; depois incluir exatamente essa expressão nas palavras-chave da CTPS e reiniciar | Antes sem resposta, depois confiança MÉDIA | PENDENTE |

## Testes com pessoas reais (obrigatórios)

**Mínimo do enunciado: 3 participantes externos, somando 10 atendimentos.** Não registre nomes, CPFs, telefones ou e-mails.

| Pessoa anônima | Quantidade de atendimentos | Encontrou orientação? | Compreendeu/ajudou? | Comentário real | Mudança sugerida |
|---|---:|---|---|---|---|
| Pessoa A | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| Pessoa B | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |
| Pessoa C | PENDENTE | PENDENTE | PENDENTE | PENDENTE | PENDENTE |

### Indicadores reais após os testes

- Participantes externos: PENDENTE
- Atendimentos totais: PENDENTE
- Respostas encontradas: PENDENTE
- Taxa de acerto percebido/ajudou: PENDENTE
- Tempo médio e tentativas por atendimento: PENDENTE
- Facilidade de uso de 1 a 5: PENDENTE
- Dúvidas sem solução: PENDENTE
- **Melhoria implementada com base no feedback:** PENDENTE (é obrigatório registrar pelo menos uma melhoria real)

> Antes de publicar o GitHub, remova perguntas reais do histórico/CSV se contiverem informações pessoais não previstas. Compartilhe apenas indicadores agregados e registros anonimizados.
