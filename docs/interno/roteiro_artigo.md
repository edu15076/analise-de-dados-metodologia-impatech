# Roteiro do artigo: o que entra em cada parte

Guia para redigir o resumo expandido *Metodologias de ensino e aprendizagem na visão de estudantes do IMPA Tech*.

Segue o [briefing da análise](briefing_analise.md) de 15/11/2026, que prevalece em caso de conflito. Os números são os **finais** (`MODO = "final"`, 117 registros, última resposta em 17/11/2026) e saem da **seção 11** do notebook (`relatorio_resumo_expandido.md` e `tabelas/artigo/`). **Atualize-os ao rodar com `MODO = "final"`.**

Convenções: **[decidir]** = escolha do grupo.

---

## 0. O que entra e o que não entra

**Entra no artigo:**
- **Seção 11 do notebook:** a família fixa de 29 associações. É a única análise inferencial do artigo. Não alterar a família, os critérios nem a classificação depois de ver resultados novos.
- **Seção 12, se o grupo decidir incluir:** a análise de conteúdo categorial das sugestões.

**Não entra** (fica no repositório como exploração interna, em `tabelas/exploratorio/` e `figuras/exploratorio/`):
- o mapa de 151 associações (05d/05f);
- as hipóteses H01–H52 e C01–C22 (`docs/hipoteses.md`);
- a matriz de 27 variáveis;
- a variável "permanência em risco";
- o teste binomial da lacuna de absorção;
- os contrastes entre turmas;
- a análise lexical (seção 07);
- a neurodivergência (seções 08–09).

**Mudanças que não devem voltar:**
- O artigo trata de **estudantes**, não de "alunos e ex-alunos": quase não há ex-estudantes na amostra.
- Não há comparação por histórico de reprovação: só 11 de 97 relataram reprovação ou trancamento, grupo pequeno demais e identificável.

## 1. Regras de redação
1. **Associação, não causa.** Usar "está associado a", "relataram". Nunca "causa", "leva a", "para compensar".
2. **Níveis de evidência:**
   - **associação**: Holm < 0,05;
   - **indício**: IC 95% exclui zero, sem Holm;
   - **ausência confirmada**: TOST ±0,2, com Holm < 0,05;
   - **inconclusivo**: nenhum dos anteriores. Inconclusivo não é "não há relação".
3. **Variável de IA:** "inclinação a recorrer à IA devido ao ritmo do curso". Na prática, compara "sempre uso" com "usei algumas vezes": "Não" e "Sim, mas nunca usei" somam menos de 5 pessoas.
4. **Privacidade:**
   - nenhum grupo com menos de 5 pessoas em tabela, figura ou texto (escrever "menos de 5");
   - a pergunta de neurodivergência não é analisada nem cruzada com nada.
5. **Numeração das perguntas = Apêndice A do artigo**, não a do CSV.

   | Nº | Pergunta |
   |---|---|
   | 11 | transição |
   | 12 | expectativa |
   | 13 | pré-requisitos |
   | 14 | apoio |
   | 15 | 77 + 33, distratora |
   | 16 | aulas |
   | 17 | IA |
   | 18 | desafios |
   | 20 | intenção de concluir |
   | 21 | sugestões |
   | 22 | neurodivergência |
   | 23 | métodos de estudo |
   | 24 | conteúdo novo, absorção e monitorias |
   | 25 | trancou ou reprovou |
   | 26 | sorteio |

## 2. Resumo
- **Problema e método:** já estão no texto. Completar o N: 114 incluídos; **97** nas associações (o texto trocava "81 estudantes" por "97").
- **Uma frase de resultado,** em linguagem de associação:
  - dificuldade com pré-requisitos e com a transição associadas a precisar de apoio em mais disciplinas;
  - inclinação a recorrer à IA associada a mais apoio e a menos absorção percebida.
- **Fechar com o caráter exploratório.**
- **Se a trilha qualitativa entrar:**
  - Depois do método: "As sugestões dos estudantes foram examinadas por análise de conteúdo categorial."
  - Depois dos resultados: "Nas sugestões, destacaram-se [categoria] e [categoria]."

## 3. Introdução
- **Objetivo** (briefing): analisar a percepção de estudantes do IMPA Tech sobre as metodologias de ensino adotadas e suas próprias formas de estudo, relacionando-a à aprendizagem, para identificar aspectos que dificultam a aprendizagem e discutir práticas pedagógicas mais adequadas.
  - Tirar "e às reprovações relatadas".
  - Tirar "alunos e ex-alunos".
- **Método:** descrever como "análise de 29 associações" (seção 11), **não** "151 associações".
- **Se a trilha qualitativa entrar,** acrescentar onde o questionário é descrito: "com perguntas fechadas, analisadas estatisticamente, e abertas, examinadas por análise de conteúdo".
- **Carta aberta dos estudantes:** só citar se entrar nas Referências [decidir].

## 4. Metodologia
O texto atual já descreve a especificação da seção 11, que deve ficar idêntica.

| Ponto | O que escrever |
|---|---|
| Inclusão | Só TCLE ≠ "não". Quem não respondeu às escalas fica fora das associações (pares completos). Quem errou 77 + 33 é mantido. |
| Fluxo | 117 registros; 3 recusas; 114 incluídos; 17 sem escalas; **n = 97** nas associações |
| Blocos | A: percepção das aulas e da aprendizagem; B: intenção de concluir o curso; C: métodos de estudo; D: forma de ingresso |
| n mínimo | 10 por grupo para calcular uma associação; abaixo disso, só medianas |
| Medidas | ρ de Spearman (ordinal × ordinal); r_rb com p de Mann-Whitney (dicotômica × ordinal) |
| IC | bootstrap percentil, **10.000** reamostragens, semente 42 |
| Correção | Holm sobre as **29** associações: todas foram calculadas (tirar a frase sobre associações não calculadas) |
| Classificação | os quatro níveis da §1 |
| Sensibilidade | exclui quem errou 77 + 33 e quem não respondeu à pergunta 25 (trancou/reprovou) |

- **Trilha qualitativa (entra):** acrescentar um parágrafo depois do da análise estatística, com o texto pronto do guia "Respostas abertas no resumo expandido":
  - análise de conteúdo categorial (BARDIN, 2016) das sugestões (questão 21);
  - regra de exclusão das respostas que não eram sugestão (nesta coleta, nenhuma foi excluída: as 18 com conteúdo entraram);
  - unidade de análise = trecho com uma ideia;
  - categorias definidas a partir das respostas por dois autores;
  - codificação independente;
  - concordância de 89% nas decisões resposta × categoria, sempre com o kappa ao lado (0,67);
  - divergências resolvidas por consenso.

  A abordagem passa a ser "quali-quantitativa".
- **Tirar:**
  - spaCy, lemas e coocorrência;
  - "codificação temática manual";
  - "151 associações";
  - qualquer menção a hipóteses pré-registradas como resultado.

  Se quiserem citar as hipóteses, basta uma frase: foram registradas para estudos futuros.

## 5. Resultados
Fontes:
- `relatorio_resumo_expandido.md`;
- `tabelas/artigo/tabela1_associacoes_holm.csv` (**Tabela 1 do artigo**, já formatada);
- `tabelas/artigo/11_tabela_descritiva.csv` (caracterização, em texto);
- `tabelas/artigo/11_tabela_associacoes.csv` (as 29, com todas as colunas);
- `tabelas/artigo/11_sensibilidade.csv`;
- `figuras/artigo/11_associacoes_ic.png`, opcional.

### 5.1 Caracterização (em texto; a Tabela 1 é a das associações)
**Fonte:** `11_tabela_descritiva.csv`, com 114 incluídos e percentuais sobre quem respondeu a cada pergunta.

**Perfil:**
- **Turma:** 2026 44%, 2025 36%, 2024 19%.
- **Idade:** 17–19 anos 41%, 20–22 anos 47%, 23 anos ou mais 12%.
- **Forma de ingresso:** medalhas 75%, ENEM 25%.
- **Tempo até o ingresso:** imediatamente após o EM 64%.
- **Outra graduação:** 27% iniciaram.
- **Intenção de concluir:** 86% pretendem concluir.

**Escalas de 1 a 10 (mediana [IQR], n = 97):** nos dados, nenhuma resposta foi 0, embora o cabeçalho da exportação diga "0 - 10"; conferir no formulário e escrever "1 a 10" se for o caso.

| Escala | Mediana [IQR] |
|---|---|
| Transição | 8 [6–9] |
| Expectativa correspondida | 8 [6–9] |
| Pré-requisitos | 6 [3–8] |
| Aulas | 5 [3–7] |
| Conteúdo novo | 9 [7–10] |
| Absorção | 6 [5–7] |
| Monitorias | 4 [2–6] |
| Disciplinas com apoio | 1 [0–2] |
| IA | 3 [2–3] |

**Desafios e métodos:**
- **Desafios:** gerenciar tempo 84%, organização de estudos 64%, tarefas de casa 31%.
- **Métodos:** leitura e resumos 77%, perguntar a uma IA 70%, cronograma 24%, grupos de estudo 18%.
- **Variável de IA:** "sempre uso" 60 e "usei algumas vezes" 34; as outras duas opções somam menos de 5.
- **Reprovação ou trancamento:** 11 de 97 relataram. Dizer que o número não permite comparações.

### 5.2 Bloco A: percepção das aulas e da aprendizagem
**Associações (Holm) = Tabela 1 do artigo** (`tabela1_associacoes_holm.csv`), agora com **4 linhas**:

| Associação | ρ | IC95 | p Holm |
|---|---|---|---|
| Pré-requisitos × apoio (A5) | 0,61 | [0,45; 0,74] | < 0,001 |
| Transição × apoio (A6) | 0,43 | [0,24; 0,60] | < 0,001 |
| IA × apoio (A8) | 0,40 | [0,22; 0,55] | 0,002 |
| Pré-requisitos × conteúdo novo (A4) | 0,37 | [0,18; 0,54] | 0,005 |

- **Sensibilidade:** as quatro se mantêm.
- **Nota da Tabela 1:** "A variável de uso de IA compara, na prática, os estudantes que sempre recorrem à IA com os que recorrem algumas vezes. Fonte: elaborado pelos autores (2026)." O asterisco da prévia sai, porque a A7 não está mais na tabela.
- **Indícios:**
  - IA × absorção (A7): ρ = −0,30 [−0,49; −0,09], p Holm = 0,074. Na prévia, era associação. O texto passa a dizer que ela **não resistiu** à correção. Mantém-se como indício na sensibilidade.
  - Aulas × absorção (A1): ρ = 0,26 [0,05; 0,46], p Holm = 0,219. Mantém-se na sensibilidade.
- **A2 e A3:** inconclusivas.

### 5.3 Bloco B: intenção de concluir o curso
- **Agora calculado:** o grupo "não pretende / não tem certeza" chegou a n = 14 (83 × 14).
- **Associações (Holm):** nenhuma.
- **Indício:** expectativa (B1), r_rb = 0,36 [0,03; 0,67], p Holm = 0,603. Medianas: 8 (pretende concluir) × 6,5 (não pretende / não tem certeza).
- **As outras 8:** inconclusivas. Por exemplo, absorção (B2): medianas 6 × 5, r_rb = 0,31, IC incluindo zero.
- **Frase a reescrever no texto:** "essas diferenças não foram testadas" deixou de valer; agora foram testadas, e só a expectativa ficou como indício.
- **Instabilidade, para dizer no texto:** na sensibilidade, B1 vira inconclusivo, e absorção (B2), pré-requisitos (B6) e apoio (B8) viram indícios. O bloco depende de quem entra na amostra; tratar com cautela.

### 5.4 Bloco C: métodos de estudo
- **Indício:** grupos de estudo × monitorias (C4), r_rb = 0,45 [0,17; 0,70], p Holm = 0,076 (17 × 80). Mantém-se na sensibilidade.
- **As outras 7:** inconclusivas.

### 5.5 Bloco D: forma de ingresso
- **Indício (novo; na prévia era inconclusivo):** ENEM × pré-requisitos (D1), r_rb = 0,27 [0,01; 0,52], p Holm = 0,868. Medianas: 7 (ENEM) × 5 (medalhas). Vira inconclusivo na sensibilidade.
- **As outras 3:** inconclusivas.
- **Não escrever "não há diferença".** Com 24 ingressantes pelo ENEM, o poder é baixo.

### 5.6 Sensibilidade
- **Amostra:** sem quem errou 77 + 33 e sem quem não respondeu à pergunta 25. Exclui menos de 5 participantes; não escrever o N (93 de 97 revelaria um grupo de 4).
- **Resultado:** 5 das 29 classificações mudam, todas nos blocos B e D (B1 e D1 viram inconclusivos; B2, B6 e B8 viram indícios). As quatro associações da Tabela 1 se mantêm.

### 5.7 Respostas abertas (entra no artigo; codificação concluída em 20/11/2026)
- **Lugar no texto:** depois do bloco B, em um parágrafo curto e no **Quadro 1**.
  - O quadro do Apêndice A vira **Quadro 2**: atualizar a legenda.
  - **Quadro 1:** categoria, descrição e nº de respostas. Os trechos ficam no corpo do texto, entre aspas, com o código aleatório (ex.: "Respondente Q21-04").
  - Da categoria mais para a menos frequente; de 3 a 5 categorias.
  - Nota: "Uma resposta pode estar em mais de uma categoria. Fonte: elaborado pelos autores (2026)."
- **Fontes:**
  - `tabelas/artigo/12_categorias_q21.csv`;
  - a concordância (%) da seção 12;
  - os trechos, escolhidos em `qualitativa/trechos_candidatos.csv` (fora do git) e revisados por mais de um autor. Tirar turma, cidade e disciplina de professor único.
- **Números:** 18 sugestões com conteúdo, todas incluídas (nenhuma exclusão).
  - **Concordância entre A e B:** 89% das decisões resposta × categoria; 39% das respostas com exatamente as mesmas categorias; kappa 0,67, só complementar. As divergências foram 16, em 11 respostas, e todas foram resolvidas por consenso.
  - **Categorias, da mais para a menos frequente:**
    - Organização Didática: 9;
    - Ritmo Acelerado: 7;
    - Avaliações e Aprendizagem: 5;
    - Acolhimento e Escuta, Desnivelamento, Pressão por Reprovação, Uso de IA e Auxílio Financeiro: menos de 5 cada.
  - **Quadro 1:** as três categorias com 5 ou mais, mais uma linha "outras categorias (menos de 5 cada)" com os cinco nomes.
  - **Trechos escolhidos** (texto em `qualitativa/trechos_escolhidos.csv`, fora do git; revisados e aprovados por dois autores em 20/11/2026):
    - Ritmo Acelerado: Respondente Q21-04;
    - Uso de IA: Respondente Q21-16 (a segunda frase da resposta).
  - **Ligação com a associação sobre IA:** o trecho da Q21-16 só se liga à associação sobre IA "pelo ritmo do curso" nas Considerações Finais, como hipótese.
  - **Opções "Outro", no máximo uma frase:** questão 18 (desafios), 9 respostas; questão 23 (métodos), menos de 5.
- **Redação:**
  - **Sujeito:** "as sugestões" ou "os participantes que responderam", nunca "os estudantes".
  - **Termos:** "categoria" (não "tema") e "análise de conteúdo" (não "codificação temática").
  - **Contagens de 1 a 4:** conforme a decisão do grupo (`SUPRIMIR_CONTAGEM_TEMAS`).
  - **Ligação com as associações:** só nas Considerações Finais.

## 6. Considerações finais
1. **Achados, sem números novos:**
   - o bloco de dificuldade: pré-requisitos e transição associados a apoio, e pré-requisitos a conteúdo novo;
   - a inclinação à IA associada a mais apoio; com menos absorção percebida, só indício;
   - o indício entre grupos de estudo e monitorias;
   - nenhuma diferença demonstrada por forma de ingresso (só um indício, instável, em pré-requisitos);
   - a intenção de concluir: só um indício (expectativa), instável na sensibilidade.
2. **Implicações, como propostas a investigar:** apoio nos pré-requisitos, ritmo do curso, orientação sobre o uso de IA, incentivo ao estudo em grupo.
3. **Respostas abertas:**
   - "Nas sugestões, destacaram-se [categoria] e [categoria], o que pode indicar [interpretação]; essa relação, porém, não foi testada e deve ser tomada como hipótese."
   - Nas limitações: "As respostas abertas foram poucas e voluntárias, e as categorias descrevem as sugestões recebidas, não a frequência dessas opiniões entre os estudantes."
4. **Limitações:**
   - amostra de conveniência e baixa adesão;
   - quase nenhum ex-estudante;
   - possível autosseleção pelo título de divulgação;
   - instrumento sem validação psicométrica, com um item por construto;
   - a pergunta 16 junta aulas teóricas e práticas;
   - a variável de IA tem, na prática, dois níveis;
   - não se perguntou sobre medalha de quem entrou pelo ENEM;
   - a faixa etária não separa menores de idade;
   - desenho transversal;
   - a família de 29 associações foi escolhida depois de ver a prévia.
5. **Estudos futuros:**
   - nova coleta para testar as hipóteses registradas (`docs/hipoteses.md`);
   - acompanhamento longitudinal;
   - questionário aos desligados;
   - escalas validadas.
6. **Revisão de texto:** "concluí-se" → "conclui-se"; "Agradeçemos" → "Agradecemos".

## 7. Referências
- **IMPA TECH (2026):** completar com o documento e a data de acesso.
- **BARDIN, L.** *Análise de conteúdo*. São Paulo: Edições 70, 2016. Conferir a edição do exemplar.
- **Carta aberta:** só se for citada.
- **spaCy e as citações das análises exploratórias** (mapa, hipóteses): não entram.

## 8. Modo final (quando a coleta encerrar)
1. Feito em 20/11/2026: planilha completa em `raw/respostas.csv`, `MODO = "final"`. Falta apagar a exportação bruta, que ainda tem IP e Resume-Code; antes, é preciso um ponto de partida anonimizado para o notebook.
2. Rodar a seção 11 **sem mudar nada**. O relatório traz:
   - N final;
   - data da última resposta incluída;
   - situação do bloco B, que só é calculado se o grupo passar de 10.
3. **Lista de mudanças** em relação à prévia, só para controle interno: `tabelas/artigo/11_mudancas_previa_final.csv`. A prévia fica congelada em `11_tabela_associacoes_previa.csv`.
4. **Hipóteses H e C:** o artigo é exploratório e usa todas as respostas juntas. As hipóteses de `docs/hipoteses.md` só são citadas como registradas para estudos futuros; nenhum teste "confirmatório" entra no texto.

## 9. Checklist antes de entregar
- [ ] Números marcados [atualizar] revistos com o modo final.
- [ ] Texto sem "alunos e ex-alunos", "reprovações relatadas", "151 associações" e análise lexical.
- [ ] Numeração das perguntas igual à do Apêndice A (§1).
- [ ] Nenhuma contagem menor que 5; nenhum cruzamento da neurodivergência.
- [ ] Toda frase de resultado com o nível certo.
- [ ] Trilha qualitativa decidida; se entrar: concordância, Quadro 1 e trechos aprovados por mais de um autor; quadro do apêndice renumerado.
