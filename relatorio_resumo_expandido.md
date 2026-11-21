# Resumo expandido — resultados exploratórios

Gerado pelo notebook `analise.ipynb` (seção 11), modo `final`. Todas as análises são exploratórias.

## Fluxo de inclusão
- Total de registros: 117.
- Removidos por recusarem o TCLE: 3. Incluídos: 114.
- Mantidos sem resposta à Q25: 17. Desses, 17 pararam no início, sem responder às escalas, e por isso não entram nas associações (cada associação usa os pares completos).
- Mantidos que erraram a verificação 77 + 33: <5.
- Com pelo menos uma escala respondida: 97.
- Última resposta incluída: 17/11/2026.
- Bloco B: o grupo que não pretende concluir ou não tem certeza tem n = 14; as associações do bloco são calculadas.
- Controle interno: 11 de 29 classificações mudaram em relação à prévia (`tabelas/artigo/11_mudancas_previa_final.csv`).

## Caracterização da amostra
- Incluídos = 114. Os percentuais são calculados sobre quem respondeu a cada pergunta.
- Turma: Turma 2026 48 (44%); Turma 2025 39 (36%); Turma 2024 21 (19%)
- Idade: 20 - 22 anos 51 (47%); 17 - 19 anos 44 (41%); 23 anos ou mais 13 (12%)
- Forma de ingresso: Medalhas 73 (75%); ENEM 24 (25%)
- Momento de ingresso após o EM: Imediatamente 69 (64%); Após 1 ano 18 (17%); Após 4 anos ou mais 11 (10%); Outras (agrupadas) 10 (9%)
- Outra graduação: Não 79 (73%); Sim (completa ou incompleta) 29 (27%)
- Relataram qualquer reprovação ou trancamento: 11 de 97 que responderam. O número é insuficiente para comparações.
- A pergunta de neurodivergência foi respondida por 56 pessoas e não é analisada aqui.
- Inclinação ao uso de IA: na prática, a variável tem dois níveis — "Sim, sempre uso" (60) e "Sim, usei algumas vezes" (34); "Não" e "Sim, mas nunca usei" somam <5. As associações com IA (A7, A8, B9) comparam, essencialmente, "sempre uso" com "usei algumas vezes".

## Resultados por bloco
Holm aplicado sobre as 29 associações calculadas da família de 29. Primeiro as associações que sobrevivem a Holm, depois os indícios (IC 95% exclui zero, sem Holm). As demais estão em `tabelas/artigo/11_tabela_associacoes.csv`; a Tabela 1 do artigo (as que resistiram a Holm), já formatada, está em `tabelas/artigo/tabela1_associacoes_holm.csv`.

### A · Percepção das aulas e da aprendizagem
**Associações (Holm):**
- A4 — Dificuldade com pré-requisitos × Conteúdo novo visto: ρ = +0,37, IC 95% [+0,18; +0,54], n = 97 pares, p Holm = 0,005
- A5 — Dificuldade com pré-requisitos × Nº de disciplinas em que precisou de apoio: ρ = +0,61, IC 95% [+0,45; +0,74], n = 97 pares, p Holm < 0,001
- A6 — Dificuldade da transição EM→superior × Nº de disciplinas em que precisou de apoio: ρ = +0,43, IC 95% [+0,24; +0,60], n = 97 pares, p Holm < 0,001
- A8 — Inclinação ao uso de IA devido ao ritmo do curso × Nº de disciplinas em que precisou de apoio: ρ = +0,40, IC 95% [+0,22; +0,55], n = 97 pares, p Holm = 0,002
**Indícios de associação:**
- A1 — Aprendizado atribuído às aulas × Quanto sente que absorveu: ρ = +0,26, IC 95% [+0,05; +0,46], n = 97 pares, p Holm = 0,219
- A7 — Inclinação ao uso de IA devido ao ritmo do curso × Quanto sente que absorveu: ρ = -0,30, IC 95% [-0,49; -0,09], n = 97 pares, p Holm = 0,074
- Inconclusivas: 2 de 8.

### B · Intenção de concluir o curso (pretende concluir = 1)
**Associações (Holm):**
- nenhuma
**Indícios de associação:**
- B1 — Pretende terminar o curso (Sim = 1) × Expectativa com a Matemática correspondida: r_rb = +0,36, IC 95% [+0,03; +0,67], n = 83 × 14, p Holm = 0,603
- Inconclusivas: 8 de 9.

### C · Métodos de estudo (marcou = 1)
**Associações (Holm):**
- nenhuma
**Indícios de associação:**
- C4 — Método: grupos de estudos × Quanto as monitorias ajudam: r_rb = +0,45, IC 95% [+0,17; +0,70], n = 17 × 80, p Holm = 0,076
- Inconclusivas: 7 de 8.

### D · Forma de ingresso (ENEM = 1, Medalhas = 0)
**Associações (Holm):**
- nenhuma
**Indícios de associação:**
- D1 — Ingresso por ENEM (1) × Medalhas (0) × Dificuldade com pré-requisitos: r_rb = +0,27, IC 95% [+0,01; +0,52], n = 24 × 73, p Holm = 0,868
- Inconclusivas: 3 de 4.

## Análise de sensibilidade
Excluindo quem não respondeu à Q25 e quem errou 77 + 33 (exclui menos de 5 participantes que responderam às escalas). Classificações que mudam: 5 de 29.
- B1: Indício de associação positiva → Inconclusivo
- B2: Inconclusivo → Indício de associação positiva
- B6: Inconclusivo → Indício de associação negativa
- B8: Inconclusivo → Indício de associação negativa
- D1: Indício de associação positiva → Inconclusivo

## Limitações
- Amostra de conveniência (adesão voluntária), sem garantia de representar todos os estudantes.
- Quase nenhum ex-estudante: quem trancou ou saiu do curso está sub-representado.
- A faixa etária (17–19 anos) não permite separar menores de 18 anos.
- O instrumento não tem validação psicométrica; cada construto é medido por um único item.
- Desenho transversal: as associações não indicam direção nem causa.
- A família de 29 associações foi escolhida depois de a prévia ter sido examinada; nenhuma delas é confirmatória.
- Quem errou a verificação de atenção (77 + 33) foi mantido; o resultado sem essas pessoas está na análise de sensibilidade.

## Interpretações (hipóteses — a escrever pelos autores)
_Usar linguagem de associação ("está associado a", "relataram"); nada de "causa", "leva a" ou "para compensar"._

## Respostas abertas
Análise de conteúdo categorial (BARDIN, 2016) das sugestões (questão 21 do Apêndice A). Categorias definidas pelos autores a partir das respostas; dois codificadores independentes; divergências resolvidas por consenso. Unidade de análise: trecho com uma ideia (uma resposta pode estar em mais de uma categoria).

- Respostas à pergunta de sugestões (não vazias): 18.
- Incluídas na análise: 18. Excluídas: 0 (não eram sugestão: 0; sem relação com o curso: 0).
- Concordância entre os codificadores: 89% das decisões resposta × categoria; 39% das respostas com as mesmas categorias. Kappa de Cohen (complementar, instável com n pequeno): 0,67.

**Categorias** (da mais para a menos frequente; uma resposta conta uma vez por categoria):

| Categoria | Definição | Respostas |
|---|---|---|
| Organização Didática | Planejamento e condução das disciplinas pelos professores: materiais, coerência com o plano de ensino, comunicação com os monitores e qualidade da docência. | 9 |
| Ritmo Acelerado | Velocidade do curso e volume de conteúdo, leituras e tarefas em relação ao tempo disponível. | 7 |
| Avaliações e Aprendizagem | Forma de avaliar e seus efeitos sobre a aprendizagem: dificuldade e calibração das provas, número de avaliações e distribuição das notas, e avaliações de que algum aspecto do curso prejudica o aprendizado. | 5 |
| Acolhimento e Escuta | Proximidade da instituição e dos professores com os estudantes: escuta, acompanhamento, acolhimento da vida pessoal e orientação por pessoas mais experientes. | <5 |
| Desnivelamento | Diferenças na base prévia dos estudantes e pedidos de nivelamento. | <5 |
| Pressão por Reprovação | Regra de reprovação e cultura da excelência, e a pressão ou o medo associados a reprovar. | <5 |
| Uso de IA | Recurso à inteligência artificial associado às condições do curso. | <5 |
| Auxílio Financeiro | Valor e condições dos benefícios financeiros. | <5 |

**Opções "Outro"** (só descritiva, sem citações): Questão 18 (desafios), opção "Outro": 9; Questão 23 (métodos de estudo), opção "Outro": <5.

### Interpretação (respostas abertas — a escrever pelos autores)
_Perguntas-guia; sujeito = "as sugestões", nunca "os estudantes"; ligação com as associações só nas Considerações Finais, como hipótese:_
- Quais categorias reúnem mais sugestões? O que as duas mais frequentes têm em comum?
- Em que categorias A e B mais divergiram? A definição delas no livro de códigos ficou clara?
- Algum trecho candidato pode identificar quem escreveu (turma, cidade, disciplina com um só professor)?
- Alguma categoria conversa com as associações da Tabela 1? Como escrever isso como hipótese ("pode indicar")?
- O que as categorias não permitem dizer, dado que poucos participantes responderam à pergunta aberta?
