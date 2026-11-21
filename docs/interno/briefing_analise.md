# Briefing para a análise de dados: resumo expandido IMPA Tech

Atualizado em 15/11/2026. Este documento orienta a análise neste repositório para que ela sirva diretamente ao artigo. **Quando houver conflito entre este briefing e o `roteiro_artigo.md`, vale este briefing.**

## 1. Objetivo atual do artigo
- **Título:** "Metodologias de ensino e aprendizagem na visão de estudantes do IMPA Tech".
- **Objetivo:** analisar a percepção de estudantes do IMPA Tech sobre as metodologias de ensino adotadas e suas próprias formas de estudo, relacionando-a à aprendizagem, a fim de identificar aspectos que dificultam a aprendizagem e discutir práticas pedagógicas mais adequadas.
- **Desenho:** exploratório, transversal, com questionário próprio sem validação psicométrica. O estudo identifica associações e gera hipóteses; não confirma nada.

**O que mudou em relação ao plano original e não deve voltar:**
- O artigo trata de estudantes, não de "alunos e ex-alunos": quase não há ex-estudantes na amostra.
- Não há comparação por histórico de reprovação: 7 de 81 relataram reprovação ou trancamento, grupos pequenos demais e identificáveis.
- O artigo não usa:
  - o mapa de 151 associações;
  - as hipóteses H01–H52 e C01–C22;
  - a matriz de 27 variáveis;
  - a variável agregada "permanência em risco";
  - o teste binomial da "lacuna de absorção".

  Esses materiais continuam no repositório como exploração interna (`tabelas/exploratorio/`, `figuras/exploratorio/`), mas não alimentam o texto.

## 2. Trilha quantitativa (principal, já no texto)
A única análise inferencial do artigo é a **seção 11** do notebook (família fixa de 29 associações). Não alterar a família, os critérios nem a classificação depois de ver resultados novos.

**Especificação que o texto do artigo já descreve (manter idêntica):**

| Item | Especificação |
|---|---|
| Inclusão | Só TCLE ≠ "não". Quem não respondeu às escalas fica fora das associações (pares completos). |
| Verificação de atenção | Quem errou 77 + 33 é mantido. |
| Sensibilidade | Sem quem errou 77 + 33 e sem quem não respondeu à pergunta de trancamento/reprovação. |
| Blocos | A (percepção das aulas e da aprendizagem), B (intenção de concluir o curso), C (métodos de estudo), D (forma de ingresso). |
| n mínimo | 10 por grupo para calcular uma associação; abaixo disso, só medianas descritivas. |
| Medidas | ρ de Spearman (ordinal × ordinal); r_rb com p de Mann-Whitney (dicotômica × ordinal). |
| IC | bootstrap percentil, 10.000 reamostragens, semente 42 (`B_RESUMO`, `SEMENTE_RESUMO`). |
| Correção | Holm sobre as associações efetivamente calculadas. |
| Classificação | associação (Holm < 0,05); indício (IC 95% exclui zero, sem Holm); ausência confirmada (TOST ±0,2 com Holm < 0,05); inconclusivo. |
| Variável de IA | descrever como "inclinação a recorrer à IA devido ao ritmo do curso"; na prática compara "sempre uso" × "usei algumas vezes". |

**Números da prévia (histórico; os finais, de 20/11/2026, estão no `relatorio_resumo_expandido.md` e no roteiro):**
- **Fluxo:** 96 registros; 3 recusas; 12 sem escalas; n = 81.
- **Holm sobre 20 associações; 5 sobrevivem:**

  | Associação | Efeito |
  |---|---|
  | pré-requisitos × apoio | 0,63 |
  | IA × apoio | 0,43 |
  | transição × apoio | 0,41 |
  | pré-requisitos × conteúdo novo | 0,38 |
  | IA × absorção | −0,33 (vira indício na sensibilidade) |

- **Indícios:** aulas × absorção (0,30); grupos de estudo × monitorias (r_rb = 0,45).
- **Bloco D:** inconclusivo.
- **Bloco B:** não calculado (grupo n = 9). Medianas: expectativa 6 × 8; absorção 4 × 6,5.

## 3. Trilha qualitativa (em avaliação: preparar, não decidir)
> **Atualização (20/11/2026):** codificação A/B e consenso concluídos (18 sugestões com conteúdo, concordância de 89%); o grupo escolheu dois trechos para citar, e a trilha entra no artigo. Números e redação em `roteiro_artigo.md`, seção 5.7.

O grupo ainda vai decidir se a análise das respostas abertas entra na versão final. Se entrar, a metodologia volta a ser "quali-quantitativa". A análise deve estar pronta para as duas decisões (seção 12 do notebook).

**Escopo e método:**
- **Escopo:** só a pergunta de sugestões (pergunta 21 do Apêndice A; 16 respostas com conteúdo). As opções "Outro" das perguntas de desafios e de métodos de estudo entram, no máximo, numa frase descritiva.
- **Método:** análise de conteúdo categorial (BARDIN, 2016).
  - Excluir respostas sem sugestão ("sim", "não").
  - Unidade de análise: o trecho com uma ideia; uma resposta pode estar em mais de uma categoria.
  - Categorias definidas a partir da leitura das respostas, não de um esquema pronto nem dos temas da Carta aberta.
  - Dois autores codificam de forma independente; registrar a concordância (%) e resolver as divergências por consenso.
- **A análise lexical sai do artigo** (lemas, coocorrência, spaCy): com menos de 30 textos, não sustenta conclusões.

**Produtos, se a trilha for adiante:**
- quadro com categoria, descrição, número de respostas e um trecho de exemplo (até 30 palavras, sem ID), da categoria mais para a menos frequente;
- percentual de concordância entre os codificadores;
- uma frase de resultado para o resumo e uma para as Considerações Finais.

**Redação:** o sujeito é sempre "as sugestões" ou "os participantes que responderam", nunca "os estudantes". A ligação com as associações fica só nas Considerações Finais, como hipótese.

## 4. Privacidade (vale para as duas trilhas)
- Dados brutos, `codigos.csv` e qualquer arquivo com texto literal ficam fora do git (`raw/`, `qualitativa/`).
- Antes de cada commit, conferir que nenhuma saída de célula do notebook mostra respostas abertas.
- IP, Resume-Code e palavras-código são removidos no carregamento.
- A pergunta de neurodivergência não é analisada nem cruzada com nenhuma variável.
- Nenhum grupo com menos de 5 pessoas em tabela, figura ou texto. Para contagens de categorias qualitativas, o grupo decide se mostra o número ou "menos de 5".
- Trechos citados: revisados por mais de um autor, sem nomes (usar [professor], [pessoa]), turma, cidade ou disciplina de professor único.

## 5. Quando a coleta encerrar (modo final)
1. Exportar a planilha completa, anonimizar na hora e apagar a versão bruta exportada.
2. Rodar a seção 11 sem mudar nada e atualizar os números do relatório.
3. Informar o N final e a data da última resposta incluída.
4. Verificar se o grupo "não pretende / não tem certeza" passou de 10. Só então o bloco B passa a ser calculado.
5. **Hipóteses H/C** (decisão de 20/11/2026): o artigo é exploratório, e todas as respostas são analisadas juntas, sem separar as anteriores e as posteriores à prévia. O artigo só menciona que as hipóteses foram registradas para estudos futuros.

## 6. Entregáveis para o texto
- `relatorio_resumo_expandido.md` atualizado: fluxo, amostra, resultados por bloco, sensibilidade e limitações.
- Tabela das associações que resistiram a Holm, com ρ, IC 95% e p de Holm: Tabela 1 do artigo, já formatada em `tabelas/artigo/tabela1_associacoes_holm.csv` (todas as 29 em `11_tabela_associacoes.csv`).
- Se a trilha qualitativa seguir: quadro de categorias e concordância (`tabelas/artigo/12_categorias_q21.csv`).
- Lista de mudanças entre a prévia e a versão final, só para controle interno (`tabelas/artigo/11_mudancas_previa_final.csv`).

## 7. Regras de linguagem
- **Associação, não causa:** "está associado a", "relataram"; nunca "causa", "leva a", "para compensar".
- **Níveis de evidência:** usar os nomes certos.
- **Numeração das perguntas:** usar a do Apêndice A do artigo (neurodivergência na 22, sorteio na 26), não a do CSV.
