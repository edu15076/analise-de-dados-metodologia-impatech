# Metodologias de ensino e aprendizagem na visão de estudantes do IMPA Tech: análise de dados

Este repositório reúne a análise de dados do resumo expandido *Metodologias de ensino e aprendizagem na visão de estudantes do IMPA Tech*, de David Barbosa Araujo, Eduardo Costa de Souza e Francisco Renan Vale Cardoso (2026).

O estudo é **exploratório e transversal**. Um questionário online, sem identificação dos participantes, foi aplicado a estudantes do IMPA Tech entre outubro e novembro de 2026. Ele trata da percepção dos estudantes sobre as metodologias de ensino e sobre as próprias formas de estudo. As análises identificam **associações** e geram hipóteses; nenhuma delas é confirmatória, e nenhuma indica causa.

---

## Onde estão os resultados do artigo

Tudo o que o artigo usa sai das **seções 11 e 12** do notebook [`analise.ipynb`](analise.ipynb) e fica nas pastas `artigo/`.

| No artigo | Arquivo |
|---|---|
| Fluxo de inclusão | [`tabelas/artigo/11_fluxo_inclusao.csv`](tabelas/artigo/11_fluxo_inclusao.csv) |
| Caracterização da amostra | [`tabelas/artigo/11_tabela_descritiva.csv`](tabelas/artigo/11_tabela_descritiva.csv) |
| **Tabela 1**: associações que resistiram à correção de Holm | [`tabelas/artigo/tabela1_associacoes_holm.csv`](tabelas/artigo/tabela1_associacoes_holm.csv) |
| As 29 associações, com todas as estatísticas | [`tabelas/artigo/11_tabela_associacoes.csv`](tabelas/artigo/11_tabela_associacoes.csv) |
| Análise de sensibilidade | [`tabelas/artigo/11_sensibilidade.csv`](tabelas/artigo/11_sensibilidade.csv) |
| Categorias das sugestões (respostas abertas, seção 12) | [`tabelas/artigo/12_categorias_q21.csv`](tabelas/artigo/12_categorias_q21.csv) |
| Figura complementar: as 29 associações com IC 95% | [`figuras/artigo/11_associacoes_ic.png`](figuras/artigo/11_associacoes_ic.png) |
| Relatório com todos os números citados no texto | [`relatorio_resumo_expandido.md`](relatorio_resumo_expandido.md) |

Os números são os da coleta completa: 117 registros, 114 incluídos e 97 participantes nas associações, com respostas de 30/10 a 17/11/2026. O arquivo `11_tabela_associacoes_previa.csv` guarda uma primeira rodada da análise (prévia de 09/11/2026), e `11_mudancas_previa_final.csv` lista o que mudou, só para controle.

**Respostas abertas:** as sugestões (pergunta 21 do Apêndice A) passaram por uma análise de conteúdo categorial (Bardin), descrita na seção 12 do notebook. As categorias foram definidas pelos autores; dois autores codificaram as respostas de forma independente, com concordância de 89% nas decisões resposta × categoria, e as divergências foram resolvidas por consenso. Essa análise é só descritiva: as categorias não são cruzadas com nenhuma outra variável. Nenhum texto de resposta é publicado no repositório.

---

## Método (seção 11)

| Item | Como foi feito |
|---|---|
| Inclusão | Todos os registros que aceitaram o Termo de Consentimento Livre e Esclarecido (TCLE). Quem não respondeu às escalas fica fora das associações, que usam só os pares completos. |
| Família de associações | 29 associações numa família fixa, escolhida pela ligação com o objetivo, mas depois de examinar uma primeira rodada dos dados (por isso nenhuma é confirmatória). Quatro blocos: A, percepção das aulas e da aprendizagem; B, intenção de concluir o curso; C, métodos de estudo; D, forma de ingresso (ENEM × medalhas). |
| Medidas | ρ de Spearman (ordinal × ordinal); correlação bisserial de postos r_rb, com p de Mann-Whitney (dicotômica × ordinal). |
| Intervalos de confiança | Bootstrap percentil, com 10.000 reamostragens e semente fixa (42). |
| Múltiplos testes | Correção de Holm sobre as associações efetivamente calculadas. |
| n mínimo | 10 por grupo para calcular uma associação; abaixo disso, só medianas descritivas. |
| Sensibilidade | A análise é repetida sem quem errou a pergunta de verificação de atenção e sem quem não respondeu à pergunta sobre trancamento ou reprovação. |

Cada associação recebe uma de quatro classificações:
- **associação:** p ajustado por Holm < 0,05;
- **indício:** o IC 95% exclui zero, mas a associação não resiste a Holm;
- **ausência confirmada:** teste de equivalência (TOST) com margem ±0,2 e Holm < 0,05;
- **inconclusivo:** nenhum dos casos anteriores.

A variável de inteligência artificial mede a *inclinação a recorrer à IA devido ao ritmo do curso*, e não a frequência de uso. Na prática, ela compara quem "sempre usa" com quem "usou algumas vezes".

---

## Estrutura do repositório

```
analise.ipynb                  notebook único (seções 00–12)
utils.py                       funções usadas pelo notebook
relatorio_resumo_expandido.md  relatório gerado pela seção 11 (números do artigo)
requirements.txt               versões dos pacotes

tabelas/artigo/                ← usado no artigo (seções 11 e 12)
figuras/artigo/                ← usado no artigo
tabelas/exploratorio/          exploração interna (seções 01–10); não entra no artigo
figuras/exploratorio/          exploração interna; não entra no artigo

docs/hipoteses.md              hipóteses registradas para estudos futuros (exploratório)
docs/interno/                  documentos de trabalho dos autores (briefing e roteiro de redação)
```

### O que **não** é usado no artigo
As seções 01–10 do notebook ficam como **exploração interna** e não sustentam nenhuma afirmação do texto. São elas:
- perfil e escalas;
- comparações entre grupos;
- um mapa de 151 associações;
- contrastes entre turmas;
- variáveis agregadas;
- uma matriz de relações entre 27 variáveis;
- análise lexical das respostas abertas;
- poder estatístico.

Essas análises orientaram a formulação de hipóteses, mas foram feitas depois de ver os dados.

As hipóteses H01–H52 e C01–C22 estão em [`docs/hipoteses.md`](docs/hipoteses.md). Foram formuladas olhando uma primeira rodada das respostas e testadas, de forma exploratória, com todas as respostas juntas. Não confirmam nada: ficam registradas para estudos futuros.

---

## Reprodução

**O repositório só tem dados agregados.** O TCLE garantiu que as respostas seriam tratadas "de forma estritamente confidencial e agregada", e por isso nenhuma resposta individual é publicada, nem mesmo anonimizada. Os resultados aparecem só como contagens, porcentagens, medianas e medidas de associação, e nenhum grupo com menos de 5 pessoas é mostrado.

O notebook completo só roda no ambiente dos autores, que guardam os dados fora do repositório. O código, as saídas (tabelas, figuras e o notebook executado) e todos os parâmetros da análise estão aqui, para que o procedimento possa ser conferido.

Para os autores:

```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

1. Coloque a exportação do formulário em `raw/respostas.csv`.
2. Escolha `MODO = "previa"` ou `"final"` na célula de configuração do notebook.
3. Execute o notebook inteiro.

Nenhuma outra célula tem valores fixos.

---

## Privacidade e ética

- O questionário não pediu nome, e-mail nem matrícula. A plataforma registrou automaticamente o endereço de IP e um código de retomada (Resume-Code), e o sorteio coletou palavras-código. Esses campos são removidos logo após a leitura: não aparecem em nenhuma saída da análise e nunca são publicados.
- **As respostas abertas não são publicadas.** O texto das respostas fica fora do repositório, e o notebook mostra apenas contagens.
- Nenhuma tabela, figura ou texto mostra grupos com menos de 5 pessoas: essas contagens aparecem como "<5" ou são agrupadas.
- A pergunta sobre neurodivergência, incluída durante a coleta, não é analisada nem cruzada com outras variáveis.
- A pesquisa foi dispensada de registro e avaliação pelo sistema CEP/CONEP, por se tratar de pesquisa de opinião com participantes não identificados (Resolução CNS nº 510/2016, art. 1º, parágrafo único, inciso I).

## Numeração das perguntas

Textos, gráficos e relatórios usam a numeração do **Apêndice A do artigo**. Os nomes de coluna no código (`q22_sugestoes`, `q26_trancou`…) seguem a numeração da exportação do formulário, que é a do Apêndice A mais 1.

## Licença

O código está sob a licença MIT (ver [`LICENSE`](LICENSE)). A licença não cobre os dados dos participantes, que não estão no repositório.
