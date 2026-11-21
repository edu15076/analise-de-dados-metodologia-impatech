# Projeto: Metodologias de ensino no IMPA Tech — análise do questionário

**O que vai para o artigo:** segue o [`docs/interno/briefing_analise.md`](docs/interno/briefing_analise.md) (15/11/2026), que prevalece sobre o `docs/interno/roteiro_artigo.md`. O repositório é público e acompanha o artigo: o `README.md` é para leitores externos. A única análise inferencial do artigo é a seção 11; a seção 12 (respostas abertas, análise de conteúdo descritiva) entra como complemento: codificação e consenso concluídos em 20/11/2026; as seções 01–10 e 05a–05i são exploração interna.

**Numeração das perguntas:** neste arquivo e nos nomes de coluna (`q22_sugestoes`, `q26_trancou`…) vale a do **CSV**. Em textos, gráficos e relatórios vale a do **Apêndice A do artigo = CSV − 1** (21 sugestões, 22 neurodivergência, 23 métodos, 24 conteúdo novo/absorção/monitorias, 25 trancou/reprovou, 26 sorteio).

## Objetivo do notebook
Um único notebook (`analise.ipynb`) que roda em dois modos, sem alterar código:
- `MODO = "previa"` → dados parciais, para apresentar à orientadora. Todo teste é rotulado como **exploratório**.
- `MODO = "final"` → CSV completo ao fim da coleta. **O estudo é exploratório:** todas as respostas são analisadas juntas, sem separar as anteriores e as posteriores à prévia, e nenhum teste é confirmatório.

Trocar de modo = mudar só a célula de CONFIG. Nenhuma outra célula tem valores fixos (n, nomes de arquivo, contagens).

## Célula de CONFIG (primeira célula)
```python
MODO = "previa"                      # "previa" | "final"
ARQUIVO = "raw/respostas.csv"        # CSV exportado do UmfrageOnline (sep=';')
INCLUIR_QUASE_COMPLETOS = False      # incluir 'não concluído' com todas as escalas preenchidas?
ALPHA = 0.05
N_MIN_GRUPO = 10                     # abaixo disso: só descritiva, sem teste
N_MIN_CELULA = 5                     # abaixo disso: suprimir contagem em tabelas (privacidade)
```

## Regras de dados
- Ler com `pd.read_csv(ARQUIVO, sep=';', dtype=str)`.
- **Anonimização logo após a leitura:** remover `Endereço de IP`, `Resume-Code`, a coluna do sorteio (Q27) e qualquer coluna `Unnamed`. Nunca imprimir nem salvar essas colunas.
- **Remover as perguntas distratoras logo após a anonimização** (enunciado + coluna de valor): Q5 (Rio, `1 - 10`), Q11 (hotel, `0 - 10`), Q16 (77+33) e Q20 (casa, `0 - 10.3`). Elas só servem para disfarçar o objetivo do questionário e não entram em nenhuma análise, gráfico ou tabela. **Única exceção:** a Q16 (77 + 33) vira só a flag `verif_atencao` (acertou/errou), usada só na análise de sensibilidade da seção 11 (resumo expandido).
- **Inclusão na amostra:** `Estado da participação == "participado e completo"` E consentimento (Q1) `== "sim"`. Com `INCLUIR_QUASE_COMPLETOS=True`, aceitar também "não concluído" com todas as escalas centrais preenchidas. Imprimir uma tabela de fluxo: total → completos → com consentimento → amostra final.
- **Os valores das escalas estão na coluna seguinte ao enunciado** (a coluna do enunciado vem vazia). Mapear pela POSIÇÃO do cabeçalho, porque os nomes se repetem (`0 - 10`, `0 - 10.1`…):

| Variável | Coluna no CSV |
|---|---|
| q08_impacto_grad | `Impactou:` |
| q12_transicao | `Nível de dificuldade` |
| q13_expectativa | `0 - 10.1` |
| q14_prereq | `O quanto você sentiu/sente dificuldade` |
| q17_aulas | `0 - 10.2` |
| q25_novo / q25_absorveu / q25_monitoria | as 3 colunas após o enunciado da Q25 |

- Múltipla escolha (Q10 escola, Q19 desafios, Q24 métodos): cada opção é uma coluna com `"1"` ou vazio → converter para 0/1. Vazio = não marcou (não é NaN).
- Q15 apoio: ordinal `Não < 1 < 2 < 3 < 4+`. Q18 IA: ordinal `Não < Sim, mas nunca usei < Sim, usei algumas vezes < Sim, sempre uso`.
- Textos abertos: Q19 "Outro" (`Área do texto`), Q22 sugestões, Q24 "Outro" (`Área do texto.1`). Respostas como "não" e "sim" na Q22 não contam como sugestão.
- Antes de exibir trechos de texto, substituir nomes próprios de pessoas por `[professor]`/`[pessoa]`.

## Regras estatísticas
- Likert é **ordinal**: reportar mediana, IQR, média e DP. Gráfico de barras divergentes ou empilhadas.
- 2 grupos → Mann-Whitney U + tamanho de efeito r. 3+ grupos → Kruskal-Wallis + ε² e, se significativo, Dunn (scikit-posthocs).
- Escala × escala → Spearman. Categórica × categórica → qui-quadrado, ou Fisher se alguma esperada < 5.
- Toda família de testes passa por correção de **Holm** (`statsmodels.stats.multitest.multipletests`). Mostrar o p bruto e o p ajustado.
- Se algum grupo tiver n < `N_MIN_GRUPO`: não testar, mostrar só a descritiva e uma nota explicando.
- Em `MODO="previa"`, cada tabela de teste traz o rótulo "EXPLORATÓRIO — dados parciais".

## Hipóteses pré-registradas
- Texto: `docs/hipoteses.md` (exploração interna; não entra no artigo). Código: `HIPOTESES` na seção 05a do notebook (52 hipóteses, ids H01–H52; a H28 não é testável como teste único).
- Hipóteses da carta aberta dos estudantes: C01–C22 (`HIPOTESES_CARTA`, seção 05i). Duas famílias de Holm: `carta` (C01–C16) e `carta-2` (C17–C22, acrescentadas depois das seções 05g–05i; a C22 é um teste binomial de uma amostra). Desfecho 0/1 (C19, C21): mascarar se alguma célula < `N_MIN_CELULA`.
- Foram formuladas olhando a prévia (respostas até 09/11/2026). São testadas **com todas as respostas juntas**, de forma exploratória: não há corte nem teste confirmatório (decisão do grupo, 20/11/2026).
- Direção: `"+"`/`"-"` unilateral, `"0"` equivalência (TOST bootstrap, ±`DELTA_EQUIV`).
- Holm dentro de cada família: `principal` (o que a prévia indicava), `secundária` (inconclusivas na prévia), `ausência` (hipóteses de "sem relação").
- Não alterar o texto das hipóteses.

## Neurodivergência (Q23) — regras especiais
- Dado sensível, e a pergunta foi incluída no meio da coleta. Analisar só quem respondeu a Q23. Imprimir n de respondentes e n por grupo.
- **Trava principal:** `ANALISAR_NEURODIVERGENCIA = False` (CONFIG, decisão do briefing): com qualquer n, imprimir só "X de Y se declararam neurodivergentes" e nenhum cruzamento. Com a flag ligada, vale ainda: se `min(n_sim, n_nao) < N_MIN_GRUPO`, **não** testar.
- **Nunca** cruzar Q23 com turma, idade, ingresso ou escola em nenhuma tabela, com qualquer n (risco de identificação).
- Incluir uma célula de **poder estatístico** (`TTestIndPower`, d = 0,3 / 0,5 / 0,8) com o n atual e cenários de adesão final (30%, 50%, 80% de ~200 alunos, lembrando que os 41 primeiros respondentes não viram a Q23).
- Interpretação: diferença entre grupos NÃO avalia política de acolhimento. Registrar isso numa célula markdown.

## Análise de texto
- spaCy `pt_core_news_sm`. Lematizar e manter só VERB e NOUN, sem stopwords.
- Frequência de lemas (geral e por pergunta), matriz termo × texto, grafo de co-ocorrência (networkx, mesma resposta = aresta) e comunidades (Louvain).
- Com menos de 30 textos: rotular como exploratório e não interpretar clusters como achado.
- Só lemas que aparecem em ≥ 3 textos (`MIN_TEXTOS_LEMA`) vão para tabelas, figuras e saídas; perguntas com < `N_MIN_CELULA` textos não têm lemas listados.
- Sentimento por léxico (LeIA), se usado, só como apoio. A análise das sugestões que entra no artigo é a análise de conteúdo categorial da seção 12 (o antigo `qualitativa/codigos.csv` não é mais usado).
- **Texto literal e `id_resposta` nunca vão para o git nem aparecem nas saídas do notebook:** todo arquivo com texto de resposta fica em `qualitativa/` (no `.gitignore`); o notebook só exibe contagens e lemas.

## Estrutura do notebook
00 config · 01 leitura + anonimização + fluxo da amostra · 02 perfil · 03 escalas Likert · 04 múltipla escolha · 05 comparações (05a hipóteses … 05f classificação; 05g contrastes dois a dois: turmas e ingresso × outra graduação; 05h agregações: permanência em risco, índice de dificuldade, lacuna de absorção, contagens; 05i carta aberta: hipóteses C01–C22, matriz e rede das relações) · 06 correlações Spearman · 07 texto · 08 neurodivergência (com trava) · 09 poder · 10 tabela-síntese para RESULTADOS · 11 resumo expandido (família fixa de 29 associações; inclusão só pelo TCLE, mantendo quem não respondeu à pergunta de trancamento (CSV Q26) e quem errou 77 + 33; blocos A percepção, B intenção de concluir, C métodos de estudo, D forma de ingresso; no modo prévia congela `tabelas/artigo/11_tabela_associacoes_previa.csv` e no modo final lista as mudanças em `11_mudancas_previa_final.csv`; sensibilidade excluindo esses dois grupos; relatório em `relatorio_resumo_expandido.md`; base anonimizada em `raw/base_anonima.csv`, fora do git) · 12 respostas abertas: análise de conteúdo categorial (Bardin) das sugestões; passo 1 prepara `qualitativa/` (textos com `id_curto`, chave, planilhas A/B e livro de códigos em branco: as categorias são dos autores); passo 2 concordância percentual (kappa só complementar) e `divergencias.csv`; passo 3 `tabelas/artigo/12_categorias_q21.csv` (flag `SUPRIMIR_CONTAGEM_TEMAS`), trechos candidatos só em `qualitativa/`, contagem das opções "Outro" e seção "Respostas abertas" no relatório. A análise lexical (07) é exploratória e não entra no artigo

Cada seção termina com uma célula markdown "Interpretação" que a aluna escreve. Não escrever interpretação por ela, só deixar perguntas-guia.

## Como trabalhar
- Implementar uma seção por vez. Rodar e mostrar a saída antes de seguir.
- Funções reutilizáveis em `utils.py` (carregar, limpar, descrever_likert, comparar_grupos).
- Saídas com nome fixo, para regenerar no modo final, separadas pelo uso: `tabelas/artigo/` e `figuras/artigo/` = o que alimenta o texto (seções 11 e 12); `tabelas/exploratorio/` e `figuras/exploratorio/` = exploração interna (seções 01–10). Texto literal só em `qualitativa/`.
- Gráficos de efeito com IC95 e faixa ±`DELTA_EQUIV` (verde): todos com `utils.grafico_ic`, na pasta `figuras/exploratorio/efeitos_ic_faixa/` (`PASTA_IC`; o da seção 11 fica em `figuras/artigo/11_associacoes_ic.png`), agrupados pelos temas A–G (`utils.GRUPOS_TEMA`) e com a indicação de Holm em cada linha. Os principais estão embutidos em `docs/hipoteses.md`.
- `raw/` (dados brutos, com IP e Resume-Code) fica fora do git (`.gitignore`).
- **Só dados agregados no git** (o TCLE prometeu tratamento "confidencial e agregado"): nenhuma base linha a linha, nem anonimizada, vai para o repositório; tabelas e figuras mostram só resumos, sem grupos com menos de 5 pessoas.