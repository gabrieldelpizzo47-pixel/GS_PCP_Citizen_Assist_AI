# Roteiro sugerido para vídeo técnico (5 a 8 minutos)

**Todos os integrantes falam com a própria voz.** Não é pitch e não pode usar voz sintética. Mostre o VS Code e o terminal, com letras legíveis.

| Tempo | Responsável sugerido | O que mostrar/explicar |
|---|---|---|
| 0:00–0:30 | Patrick | Integrantes, público (jovens no primeiro emprego) e problema da informação dispersa |
| 0:30–1:15 | Patrick | `data/base_conhecimento.json`: abrir registro da CTPS, explicar campos, dicionários e a lista de registros |
| 1:15–2:15 | Gabriel | `orientacao.py`, `base_conhecimento.py`, `assistente.py`: 3 classes, atributos, métodos, `self`, composição `Assistente -> BaseConhecimento -> Orientacao` |
| 2:15–3:20 | Gabriel | `normalizar()` e `pontuar()`, +3 por palavra-chave e +1 por palavra do título. Mostrar a lista de tuplas `(pontos, orientacao)` e confiança ALTA/MÉDIA |
| 3:20–4:30 | Ian | Executar `python main.py`: pergunta encontrada, pergunta sem resposta, opção inválida, CPF/e-mail bloqueado e navegação por categoria |
| 4:30–5:20 | Gabriel | Modificação ao vivo: perguntar `registro laboral virtual` (não acha); abrir JSON e adicionar `"registro laboral virtual"` à lista `palavras_chave` do registro de CTPS; reiniciar o programa e repetir pergunta (agora acha) |
| 5:20–6:20 | Ian | `data/historico.json`, `data/atendimentos.csv` e indicadores reais dos 3 usuários e 10 atendimentos; facilidade de uso |
| 6:20–7:00 | Patrick | Justificativa técnica: busca por pontuação sem API externa; limitação: não entende todos os sinônimos e dados precisam de revisão oficial |

**Atenção:** o roteiro é uma sugestão de divisão de fala, não contém dados reais dos testes. Atualize a demonstração, os indicadores e as falas conforme o código efetivamente executado. Não ultrapasse 8 minutos.
