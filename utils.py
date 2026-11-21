"""Funções reutilizáveis da análise do questionário (IMPA Tech).

O CSV do UmfrageOnline repete nomes de cabeçalho ("0 - 10", "0 - 10.1"...) e
põe o valor das escalas na coluna SEGUINTE ao enunciado. Por isso o mapeamento
é feito pela POSIÇÃO da coluna, com uma checagem do início do cabeçalho em cada
posição: se o formato do export mudar, o código falha em vez de trocar colunas
em silêncio.
"""
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Mapeamento posição -> (nome da variável, início esperado do cabeçalho)
# ---------------------------------------------------------------------------
MAPA_COLUNAS = {
    0:  ("id_resposta",          "_ID da resposta"),
    4:  ("data_hora",            "Data e hora"),   # só para separar prévia × novas respostas; nunca exibida
    5:  ("estado",               "Estado da participa"),
    6:  ("q01_consentimento",    "1. Gostaria"),
    7:  ("q02_idade",            "2. Qual sua idade"),
    8:  ("q03_turma",            "3. Voc"),
    9:  ("q04_ingresso_tempo",   "4. Depois de concluir"),
    12: ("q06_outra_grad",       "6. Voc"),
    13: ("q07_correlato",        "7. Esse curso"),
    15: ("q08_impacto_grad",     "Impactou:"),
    16: ("q09_forma_ingresso",   "9. Qual foi sua forma"),
    18: ("q10_publica",          "Escola P"),
    19: ("q10_publica_seletiva", "Escola P"),
    20: ("q10_privada",          "Escola Privada"),
    24: ("q12_transicao",        "N"),            # "Nível de dificuldade"
    26: ("q13_expectativa",      "0 - 10.1"),
    28: ("q14_prereq",           "O quanto voc"),
    29: ("q15_apoio",            "15. Voc"),
    32: ("q17_aulas",            "0 - 10.2"),
    33: ("q18_ia",               "18. Voc"),
    35: ("q19_tempo",            "Gerenciar Tempo"),
    36: ("q19_organizacao",      "Organiza"),
    37: ("q19_tarefas",          "Tarefas de Casa"),
    38: ("q19_outro_txt",        "Área do texto"),
    41: ("q21_terminar",         "21. Mesmo"),
    42: ("q22_sugestoes",        "22. Voc"),
    43: ("q23_neurodiv",         "23. Voc"),
    45: ("q24_leitura",          "Leitura e anota"),
    46: ("q24_pratica",          "Pr"),
    47: ("q24_grupos",           "Grupos de Estudos"),
    48: ("q24_videoaulas",       "Videoaulas"),
    49: ("q24_pomodoro",         "M"),
    50: ("q24_cronograma",       "Cronograma"),
    51: ("q24_perguntar_ia",     "Perguntar a uma IA"),
    52: ("q24_outro_txt",        "Área do texto.1"),
    54: ("q25_novo",             "O quanto voc"),
    55: ("q25_absorveu",         "O quanto voc"),
    56: ("q25_monitoria",        "O quanto as monitorias"),
    57: ("q26_trancou",          "26. Voc"),
}

# Colunas que identificam a pessoa (removidas logo após a leitura).
POS_SENSIVEIS = {1: "Resume-Code", 2: "Endere", 58: "27. Para participar"}
# Perguntas distratoras (enunciado + coluna de valor): Q5, Q11, Q16, Q20.
POS_DISTRATORAS = {10: "5. O quanto", 11: "1 - 10", 21: "11. O quanto",
                   22: "0 - 10", 30: "16. Quanto", 39: "20. O quanto",
                   40: "0 - 10.3"}

ESCALAS = ["q08_impacto_grad", "q12_transicao", "q13_expectativa", "q14_prereq",
           "q17_aulas", "q25_novo", "q25_absorveu", "q25_monitoria"]
# Q8 só existe para quem fez outra graduação -> fora das "escalas centrais".
ESCALAS_CENTRAIS = [e for e in ESCALAS if e != "q08_impacto_grad"]

MULTIPLA = {
    "q10": ["q10_publica", "q10_publica_seletiva", "q10_privada"],
    "q19": ["q19_tempo", "q19_organizacao", "q19_tarefas"],
    "q24": ["q24_leitura", "q24_pratica", "q24_grupos", "q24_videoaulas",
            "q24_pomodoro", "q24_cronograma", "q24_perguntar_ia"],
}
TEXTOS = ["q19_outro_txt", "q22_sugestoes", "q24_outro_txt"]

ORDENS = {
    "q15_apoio": ["Não", "1", "2", "3", "4+"],
    "q18_ia": ["Não", "Sim, mas nunca usei", "Sim, usei algumas vezes",
               "Sim, sempre uso"],
    "q02_idade": ["17 - 19 anos", "20 - 22 anos", "23 - 25 anos", "26+"],
    "q04_ingresso_tempo": ["Imediatamente", "Após 1 ano", "Após 2 anos",
                           "Após 3 anos", "Após 4 anos ou mais"],
    "q03_turma": ["Turma 2024", "Turma 2025", "Turma 2026"],
    "q21_terminar": ["Não", "Não tenho certeza", "Sim"],
}

ESTADO_COMPLETO = "participado e completo"
ESTADO_INCOMPLETO = "participado, mas ainda não foi concluído"


def _checar(df, pos, prefixo):
    nome = df.columns[pos]
    if not str(nome).startswith(prefixo):
        raise ValueError(
            f"Coluna {pos} deveria começar com {prefixo!r}, mas é {nome!r}. "
            "O formato do export mudou: revise MAPA_COLUNAS em utils.py.")


def carregar(arquivo):
    """Lê o CSV, anonimiza, remove distratoras e renomeia por posição.

    Retorna um DataFrame só com as colunas de MAPA_COLUNAS (renomeadas).
    Colunas sensíveis e distratoras nunca chegam ao notebook.
    """
    bruto = pd.read_csv(arquivo, sep=";", dtype=str)
    for pos, pref in {**POS_SENSIVEIS, **POS_DISTRATORAS}.items():
        _checar(bruto, pos, pref)
    for pos, (_, pref) in MAPA_COLUNAS.items():
        _checar(bruto, pos, pref)

    # Anonimização + distratoras: descartar por posição e qualquer 'Unnamed'.
    descartar = set(POS_SENSIVEIS) | set(POS_DISTRATORAS)
    descartar |= {i for i, c in enumerate(bruto.columns)
                  if str(c).startswith("Unnamed")}
    manter = [p for p in MAPA_COLUNAS if p not in descartar]
    df = bruto.iloc[:, manter].copy()
    df.columns = [MAPA_COLUNAS[p][0] for p in manter]
    # Q16 (77 + 33, distratora) só vira uma FLAG de verificação de atenção (critério de inclusão
    # da seção 11); o conteúdo da distratora nunca entra em análise.
    df["verif_atencao"] = bruto.iloc[:, 30].str.strip().map({"110": 1.0, "100": 0.0})
    del bruto
    return limpar(df)


def limpar(df):
    """Tipos: escalas -> número, múltipla escolha -> 0/1, ordinais -> Categorical."""
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].str.strip()
    for c in ESCALAS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    # Múltipla escolha: vazio = não marcou (0). Só vale para quem chegou à
    # pergunta; quem parou antes fica NaN (decidido em filtrar_amostra).
    for cols in MULTIPLA.values():
        for c in cols:
            df[c] = (df[c] == "1").astype(int)
    for c, ordem in ORDENS.items():
        df[c] = pd.Categorical(df[c], categories=ordem, ordered=True)
    for c in TEXTOS:
        df[c] = df[c].replace("", pd.NA)
    if "data_hora" in df.columns:
        df["data_hora"] = pd.to_datetime(df["data_hora"], format="%d.%m.%Y %H:%M", errors="coerce")
    return df


def filtrar_amostra(df, incluir_quase_completos=False):
    """Aplica os critérios de inclusão e devolve (amostra, tabela_de_fluxo)."""
    total = len(df)
    completos = df["estado"] == ESTADO_COMPLETO
    consent = df["q01_consentimento"] == "sim"
    passos = [
        ("Total de registros", total),
        ("Participação completa", int(completos.sum())),
        ("Completos com consentimento (Q1 = sim)", int((completos & consent).sum())),
    ]
    incluir = completos & consent
    if incluir_quase_completos:
        quase = ((df["estado"] == ESTADO_INCOMPLETO) & consent
                 & df[ESCALAS_CENTRAIS].notna().all(axis=1))
        passos.append(("+ não concluídos com todas as escalas centrais", int(quase.sum())))
        incluir = incluir | quase
    passos.append(("Amostra final", int(incluir.sum())))
    fluxo = pd.DataFrame(passos, columns=["Etapa", "n"])
    return df[incluir].reset_index(drop=True), fluxo


# ===========================================================================
# Rótulos curtos
# ===========================================================================
ROTULOS = {
    "q08_impacto_grad": "Q7 Impacto da graduação anterior (1–5)",
    "q12_transicao": "Q11 Dificuldade da transição EM→superior",
    "q13_expectativa": "Q12 Expectativa com a Matemática correspondida",
    "q14_prereq": "Q13 Dificuldade com pré-requisitos",
    "q17_aulas": "Q16 Aprendizado atribuído às aulas",
    "q25_novo": "Q24 Conteúdo novo visto",
    "q25_absorveu": "Q24 Quanto sente que absorveu",
    "q25_monitoria": "Q24 Quanto as monitorias ajudam",
    "q15_apoio": "Q14 Nº de matérias em que precisou de apoio",
    "q18_ia": "Q17 Uso de IA pelo ritmo do curso",
    "q10_publica": "Escola pública", "q10_publica_seletiva": "Escola pública seletiva",
    "q10_privada": "Escola privada",
    "q19_tempo": "Gerenciar tempo", "q19_organizacao": "Organização de estudos",
    "q19_tarefas": "Tarefas de casa",
    "q24_leitura": "Leitura, anotação, resumos", "q24_pratica": "Prática, exercícios e listas",
    "q24_grupos": "Grupos de estudos", "q24_videoaulas": "Videoaulas",
    "q24_pomodoro": "Método Pomodoro", "q24_cronograma": "Cronograma/plano de estudos",
    "q24_perguntar_ia": "Perguntar a uma IA",
}

# Cores (paleta de referência do skill dataviz; azul = valores altos, vermelho = baixos)
COR_SERIE = "#2a78d6"
DIVERGENTE = ["#b8302f", "#f0a19f", "#cfcec6", "#86b6ef", "#1c5cab"]
TINTA, TINTA2, MUDO, GRADE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"


def estilo_graficos():
    import matplotlib as mpl
    mpl.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": 200, "savefig.bbox": "tight",
        "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
        "axes.edgecolor": "#c3c2b7", "axes.labelcolor": TINTA2,
        "xtick.color": MUDO, "ytick.color": TINTA2, "text.color": TINTA,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": GRADE, "grid.linewidth": 0.6,
        "axes.axisbelow": True, "font.size": 9,
    })


# ===========================================================================
# Privacidade
# ===========================================================================
def _num(v):
    return isinstance(v, (int, float, np.integer, np.floating)) and not pd.isna(v)


def suprimir(tabela, n_min, colunas=None):
    """Troca contagens entre 1 e n_min-1 por '<n_min' (e o % da linha por '—').

    Na coluna 'n' de uma tabela de frequências (total conhecido) aplica também
    supressão SECUNDÁRIA: se só uma célula foi suprimida, ou se a soma das
    suprimidas é < n_min, suprime a próxima menor contagem — senão o valor
    escondido sairia por subtração do total.
    """
    t = tabela.copy().astype(object)
    colunas = colunas or ([c for c in t.columns if c == "n"] or list(t.columns))
    for c in colunas:
        orig = tabela[c]
        pequeno = orig.apply(lambda v: _num(v) and 0 < v < n_min)
        if c == "n" and pequeno.any():
            while True:
                sup = orig[pequeno]
                restantes = orig[~pequeno & orig.apply(lambda v: _num(v) and v > 0)]
                if (len(sup) >= 2 and sup.sum() >= n_min) or restantes.empty:
                    break
                pequeno[restantes.astype(float).idxmin()] = True
        t.loc[pequeno, c] = f"<{n_min}" if c != "n" else "suprimido"
        if c == "n":
            t.loc[pequeno & orig.apply(lambda v: _num(v) and 0 < v < n_min), c] = f"<{n_min}"
            if "%" in t.columns:
                t.loc[pequeno, "%"] = "—"
    return t


def tem_celula_pequena(tabela, n_min):
    """True se alguma contagem da tabela estiver entre 1 e n_min-1."""
    v = tabela.values.astype(float)
    return bool(((v > 0) & (v < n_min)).any())


def frequencias(serie, n_min=None):
    categ = isinstance(serie.dtype, pd.CategoricalDtype)
    vc = serie.value_counts(sort=not categ, dropna=False)
    t = pd.DataFrame({"n": vc, "%": (100 * vc / vc.sum()).round(1)})
    t.index = ["(sem resposta)" if pd.isna(i) else str(i) for i in t.index]
    t = t[t["n"] > 0]
    return suprimir(t, n_min) if n_min else t


# ===========================================================================
# Descritivas e gráficos
# ===========================================================================
def descrever_likert(df, cols):
    linhas = []
    for c in cols:
        x = df[c].dropna()
        linhas.append({
            "variável": ROTULOS.get(c, c), "n": len(x),
            "mediana": x.median(), "Q1": x.quantile(.25), "Q3": x.quantile(.75),
            "IQR": x.quantile(.75) - x.quantile(.25),
            "média": x.mean(), "DP": x.std(),
        })
    return pd.DataFrame(linhas).set_index("variável").round(2)


FAIXAS = ["≤2", "3–4", "5–6", "7–8", "9–10"]


def faixas_likert(serie):
    """Agrupa uma escala 0/1–10 em 5 faixas para o gráfico divergente."""
    return pd.cut(serie, [-0.5, 2.5, 4.5, 6.5, 8.5, 10.5], labels=FAIXAS)


def grafico_likert(df, cols, arquivo=None, titulo=None):
    """Barras divergentes centradas na faixa do meio (5–6)."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    props = pd.DataFrame({c: faixas_likert(df[c]).value_counts(normalize=True)
                          .reindex(FAIXAS).fillna(0) * 100 for c in cols}).T
    props = props.loc[props[["7–8", "9–10"]].sum(axis=1).sort_values().index]
    fig, ax = plt.subplots(figsize=(8.5, 0.55 * len(cols) + 1.5))
    for i, (_, linha) in enumerate(props.iterrows()):
        esq = -(linha["≤2"] + linha["3–4"] + linha["5–6"] / 2)
        for faixa, cor in zip(FAIXAS, DIVERGENTE):
            w = linha[faixa]
            ax.barh(i, w, left=esq, color=cor, height=0.62, edgecolor="#fcfcfb", linewidth=2)
            if w >= 9:
                ax.text(esq + w / 2, i, f"{w:.0f}%", ha="center", va="center", fontsize=7.5,
                        color="#ffffff" if faixa in ("≤2", "9–10") else TINTA)
            esq += w
    ax.axvline(0, color="#c3c2b7", linewidth=1)
    ax.set_yticks(range(len(props)), [ROTULOS.get(v, v) for v in props.index])
    lim = max(60, *np.abs(ax.get_xlim()))
    ax.set_xlim(-lim, lim)
    ax.xaxis.set_major_formatter(lambda v, _: f"{abs(v):.0f}%")
    ax.grid(axis="y", visible=False)
    ax.legend(handles=[Patch(color=c, label=n) for n, c in zip(FAIXAS, DIVERGENTE)],
              ncol=5, loc="lower left", bbox_to_anchor=(0, 1.0), frameon=False,
              title="Faixa da escala (centro = 5–6)", fontsize=8, title_fontsize=8,
              alignment="left")
    if titulo:
        fig.suptitle(titulo, x=0.01, ha="left", fontsize=10, y=1.02)
    if arquivo:
        fig.savefig(arquivo)
    return fig


def grafico_barras(prop, arquivo=None, titulo=None, xlabel="% da amostra"):
    """Barras horizontais de série única (proporções em %)."""
    import matplotlib.pyplot as plt
    prop = prop.sort_values()
    fig, ax = plt.subplots(figsize=(7, 0.4 * len(prop) + 1.1))
    ax.barh(range(len(prop)), prop.values, color=COR_SERIE, height=0.6)
    for i, v in enumerate(prop.values):
        ax.text(v + 1, i, f"{v:.0f}%", va="center", fontsize=8, color=TINTA2)
    ax.set_yticks(range(len(prop)), [ROTULOS.get(i, i) for i in prop.index])
    ax.set_xlim(0, 108)
    ax.set_xlabel(xlabel)
    ax.grid(axis="y", visible=False)
    if titulo:
        ax.set_title(titulo, loc="left", fontsize=10)
    if arquivo:
        fig.savefig(arquivo)
    return fig


# ===========================================================================
# Testes
# ===========================================================================
def holm(p):
    from statsmodels.stats.multitest import multipletests
    p = pd.Series(p, dtype=float)
    out = pd.Series(np.nan, index=p.index)
    ok = p.notna()
    if ok.any():
        out[ok] = multipletests(p[ok], method="holm")[1]
    return out


def comparar_grupos(df, grupo, desfechos, n_min, alpha=0.05, alternativa="two-sided"):
    """Compara escalas entre os níveis de `grupo`.

    2 grupos -> Mann-Whitney U + r = |Z|/sqrt(N) (Z com correção para empates); 3+ -> Kruskal-Wallis + ε² = H/(N-1)
    (e Dunn com Holm se o KW ajustado for significativo). Holm na família
    (= os desfechos desta comparação). Se algum grupo tiver n < n_min, não testa.
    Retorna (tabela, dict de post-hoc Dunn).
    """
    from scipy import stats
    niveis = list(df[grupo].dropna().unique())
    if isinstance(df[grupo].dtype, pd.CategoricalDtype):
        niveis = [g for g in df[grupo].cat.categories if g in niveis]
    linhas = []
    for d in desfechos:
        sub = df[[grupo, d]].dropna()
        amostras = [sub.loc[sub[grupo] == g, d] for g in niveis]
        ns = [len(a) for a in amostras]
        linha = {"desfecho": ROTULOS.get(d, d)}
        for g, a in zip(niveis, amostras):
            linha[f"{g}: n"] = len(a)
            linha[f"{g}: Md [IQR]"] = (f"{a.median():.1f} [{a.quantile(.25):.1f}–"
                                       f"{a.quantile(.75):.1f}]") if len(a) else "—"
        linha.update(teste="não testado (n < N_MIN_GRUPO)", estat=np.nan, p=np.nan,
                     efeito=np.nan, medida="")
        if len(niveis) < 2:
            pass
        elif min(ns) >= n_min and len(niveis) == 2:
            u, p = stats.mannwhitneyu(*amostras, alternative=alternativa)
            n1, n2 = ns
            n = n1 + n2
            # Variância de U com correção para empates (escalas inteiras têm muitos empates)
            _, t = np.unique(np.concatenate(amostras), return_counts=True)
            var_u = n1 * n2 / 12 * ((n + 1) - (t ** 3 - t).sum() / (n * (n - 1)))
            z = (u - n1 * n2 / 2) / np.sqrt(var_u)
            linha.update(teste="Mann-Whitney U", estat=u, p=p,
                         efeito=abs(z) / np.sqrt(n), medida="r")
        elif min(ns) >= n_min:
            h, p = stats.kruskal(*amostras)
            linha.update(teste="Kruskal-Wallis", estat=h, p=p,
                         efeito=h / (sum(ns) - 1), medida="ε²")
        linhas.append(linha)
    t = pd.DataFrame(linhas).set_index("desfecho")
    t["p_holm"] = holm(t["p"]).values
    t["sig"] = np.where(t["p_holm"] < alpha, "*", "")
    dunn = {}
    if len(niveis) > 2:
        import scikit_posthocs as sp
        for d in desfechos:
            if t.loc[ROTULOS.get(d, d), "p_holm"] < alpha:
                sub = df[[grupo, d]].dropna().copy()
                sub[grupo] = sub[grupo].astype(str)
                dunn[ROTULOS.get(d, d)] = sp.posthoc_dunn(
                    sub, val_col=d, group_col=grupo, p_adjust="holm").round(4)
    cols_desc = [c for c in t.columns if ": " in c]
    t = t[cols_desc + ["teste", "estat", "p", "p_holm", "sig", "efeito", "medida"]]
    return t.round({"estat": 2, "p": 4, "p_holm": 4, "efeito": 3}), dunn


def associar_categoricas(df, pares, n_min_grupo, alpha=0.05, n_sim=20000, seed=0):
    """Categórica × categórica, com Holm sobre a família de pares.

    Qui-quadrado; se alguma frequência esperada < 5: Fisher exato (2×2) ou, em
    tabelas maiores, qui-quadrado por Monte Carlo com margens fixas (aproximação
    do Fisher R×C, que o SciPy não implementa). Se alguma linha (grupo) tiver
    n < n_min_grupo, não testa.
    """
    from scipy import stats
    rng = np.random.default_rng(seed)
    linhas, tabelas = [], {}
    for a, b in pares:
        ct = pd.crosstab(df[a], df[b])
        ct = ct.loc[ct.sum(axis=1) > 0, ct.sum(axis=0) > 0]
        nome = f"{a} × {b}"
        tabelas[nome] = ct
        linha = {"par": nome, "dimensão": f"{ct.shape[0]}×{ct.shape[1]}",
                 "N": int(ct.values.sum()), "teste": "não testado (n < N_MIN_GRUPO)",
                 "chi2": np.nan, "p": np.nan, "V de Cramér": np.nan}
        if min(ct.shape) >= 2 and ct.sum(axis=1).min() >= n_min_grupo:
            chi2, p, _, esp = stats.chi2_contingency(ct, correction=False)
            n = ct.values.sum()
            teste = "Qui-quadrado"
            if (esp < 5).any():
                if ct.shape == (2, 2):
                    _, p = stats.fisher_exact(ct)
                    teste = "Fisher exato"
                else:
                    x = np.repeat(np.arange(ct.shape[0]), ct.sum(axis=1).values)
                    y = np.concatenate([np.repeat(np.arange(ct.shape[1]), ct.iloc[i].values)
                                        for i in range(ct.shape[0])])
                    cont = 0
                    for _ in range(n_sim):
                        m = np.zeros(ct.shape)
                        np.add.at(m, (x, rng.permutation(y)), 1)
                        cont += ((m - esp) ** 2 / esp).sum() >= chi2 - 1e-12
                    p = (cont + 1) / (n_sim + 1)
                    teste = "χ² Monte Carlo (esperada < 5)"
            linha.update(teste=teste, chi2=round(chi2, 2), p=p,
                         **{"V de Cramér": np.sqrt(chi2 / (n * (min(ct.shape) - 1)))})
        linhas.append(linha)
    t = pd.DataFrame(linhas).set_index("par")
    t["p_holm"] = holm(t["p"]).values
    t["sig"] = np.where(t["p_holm"] < alpha, "*", "")
    return t.round({"p": 4, "p_holm": 4, "V de Cramér": 3}), tabelas


def spearman_matriz(df, cols, alpha=0.05):
    """Spearman par a par (casos completos do par) + Holm sobre todos os pares."""
    from scipy import stats
    linhas = []
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            sub = df[[a, b]].dropna()
            rho, p = stats.spearmanr(sub[a], sub[b])
            linhas.append({"x": a, "y": b, "n": len(sub), "rho": rho, "p": p})
    t = pd.DataFrame(linhas)
    t["p_holm"] = holm(t["p"]).values
    t["sig"] = np.where(t["p_holm"] < alpha, "*", "")
    return t.round({"rho": 3, "p": 4, "p_holm": 4})


CURTOS = {
    "q08_impacto_grad": "Q7 Impacto grad. anterior", "q12_transicao": "Q11 Dific. transição",
    "q13_expectativa": "Q12 Expectativa Mat.", "q14_prereq": "Q13 Dific. pré-requisitos",
    "q17_aulas": "Q16 Aprendizado nas aulas", "q25_novo": "Q24 Conteúdo novo",
    "q25_absorveu": "Q24 Absorveu", "q25_monitoria": "Q24 Monitorias ajudam",
    "q15_apoio_ord": "Q14 Matérias c/ apoio", "q18_ia_ord": "Q17 Uso de IA",
}


def grafico_spearman(tab, cols, arquivo=None):
    """Triângulo inferior da matriz de Spearman (* = p Holm < alpha)."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("div", [DIVERGENTE[0], "#f0efec", DIVERGENTE[4]])
    m = pd.DataFrame(np.nan, index=cols, columns=cols)
    s = pd.DataFrame("", index=cols, columns=cols)
    for r in tab.itertuples():
        m.loc[r.y, r.x] = r.rho
        s.loc[r.y, r.x] = r.sig
    m, s = m.iloc[1:, :-1], s.iloc[1:, :-1]      # sem a linha/coluna vazias
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    im = ax.imshow(m.values.astype(float), cmap=cmap, vmin=-1, vmax=1)
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            v = m.values[i, j]
            if not pd.isna(v):
                ax.text(j, i, f"{v:.2f}{s.values[i, j]}", ha="center", va="center",
                        fontsize=7.5, color="#ffffff" if abs(v) > .6 else TINTA)
    ax.set_xticks(range(m.shape[1]), [CURTOS.get(c, c) for c in m.columns],
                  rotation=40, ha="right", fontsize=8)
    ax.set_yticks(range(m.shape[0]), [CURTOS.get(c, c) for c in m.index], fontsize=8)
    ax.grid(False)
    for e in ax.spines.values():
        e.set_visible(False)
    fig.colorbar(im, ax=ax, shrink=0.75, label="ρ de Spearman  (* = p Holm < α)")
    if arquivo:
        fig.savefig(arquivo)
    return fig


def codificar_ordinal(serie):
    """Categorical ordenada -> códigos 0..k (NaN preservado)."""
    c = serie.cat.codes.astype(float)
    return c.where(c >= 0)


# ===========================================================================
# Texto
# ===========================================================================
RESPOSTAS_VAZIAS = {"não", "nao", "sim", "n", "s", "nada", "-", ".", "nenhuma",
                    "não.", "sim.", "não tenho"}


def textos_longos(df):
    """Empilha os textos abertos (id_resposta, pergunta, texto), sem 'não'/'sim'."""
    partes = []
    for c in TEXTOS:
        s = df[["id_resposta", c]].dropna()
        s = s[~s[c].str.strip().str.lower().isin(RESPOSTAS_VAZIAS)]
        partes.append(s.rename(columns={c: "texto"}).assign(pergunta=c))
    return pd.concat(partes, ignore_index=True)[["id_resposta", "pergunta", "texto"]]


# Termos do curso que o etiquetador marca como nome próprio, mas não são pessoas.
NAO_NOMES = {"impa", "tech", "grade", "curricular", "obrigatória", "disciplinas",
             "nivelamento", "inverno", "inglês", "cálculo", "física", "nap", "enem",
             "rio", "janeiro", "brasil", "organização", "estrutura", "lista"}
CTX_PROFESSOR = r"professor|professora|\bprof\b|docente|aula|prova|ementa|disciplina"


def candidatos_nomes(txt, nlp):
    """Sequências de >= 2 tokens PROPN com inicial maiúscula (e só ela), fora do
    início de frase e fora de NAO_NOMES. Ex.: 'o Fulano Beltrano fez'."""
    doc = nlp(txt)
    nomes, atual = [], []
    for tk in list(doc) + [None]:
        ok = (tk is not None and tk.pos_ == "PROPN" and tk.text.istitle()
              and not tk.is_sent_start and tk.text.lower() not in NAO_NOMES)
        if ok:
            atual.append(tk.text)
        else:
            if len(atual) >= 2:
                nomes.append(" ".join(atual))
            atual = []
    return nomes


def anonimizar_textos(textos, nlp, nomes_extra=()):
    """Troca nomes de pessoas por [professor]/[pessoa].

    Fontes: candidatos_nomes() + lista manual `nomes_extra` (um nome por linha
    em data/raw/nomes_anonimizar.txt). Vira [professor] quando o texto fala de
    professor/aula/prova; senão [pessoa]. Retorna (textos, nº de substituições).
    O NER do spaCy (PER) NÃO é usado: nestes textos ele erra mais do que acerta.
    """
    import re
    total = 0

    def troca(txt):
        nonlocal total
        nomes = set(candidatos_nomes(txt, nlp))
        nomes |= {n for n in nomes_extra if re.search(rf"\b{re.escape(n)}\b", txt, re.I)}
        rot = "[professor]" if re.search(CTX_PROFESSOR, txt, re.I) else "[pessoa]"
        for nome in sorted(nomes, key=len, reverse=True):
            txt, k = re.subn(rf"\b{re.escape(nome)}\b", rot, txt, flags=re.I)
            total += k
        return txt
    saida = textos.map(troca)
    return saida, total


def lematizar(textos, nlp, classes=("VERB", "NOUN")):
    """Lemas (minúsculos) por texto: só VERB/NOUN, sem stopwords e sem [marcadores]."""
    import re
    # Os marcadores de anonimização não podem virar lemas.
    limpos = [re.sub(r"\[(professor|pessoa)\]", " ", t) for t in textos]
    out = []
    for doc in nlp.pipe(limpos):
        out.append([t.lemma_.lower() for t in doc
                    if t.pos_ in classes and not t.is_stop and t.is_alpha and len(t) > 2])
    return out


def grafo_coocorrencia(lemas_por_texto, freq_min=2, seed=0):
    """Nós = lemas em >= freq_min respostas; aresta = mesma resposta (peso = nº de respostas).
    Comunidades por Louvain (networkx)."""
    import itertools
    from collections import Counter
    import networkx as nx
    freq = Counter(l for ls in lemas_por_texto for l in set(ls))
    g = nx.Graph()
    for ls in lemas_por_texto:
        nos = sorted({l for l in ls if freq[l] >= freq_min})
        g.add_nodes_from(nos)
        for a, b in itertools.combinations(nos, 2):
            w = g.get_edge_data(a, b, {"weight": 0})["weight"]
            g.add_edge(a, b, weight=w + 1)
    nx.set_node_attributes(g, {n: freq[n] for n in g.nodes}, "freq")
    com = (nx.community.louvain_communities(g, weight="weight", seed=seed)
           if g.number_of_edges() else [])
    return g, sorted(com, key=len, reverse=True)


# ===========================================================================
# Gráficos adicionais (perfil, grupos, pares, categóricas, poder)
# ===========================================================================
# Ordem categórica fixa (paleta de referência validada; nunca reciclar cores).
CATEGORICAS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300",
               "#6250d6", "#e34948"]


def _agrupar_pequenas(contagens, n_min):
    """Junta categorias com 0 < n < n_min num grupo 'Outras'. Se o grupo tiver
    uma só categoria ou soma < n_min, puxa também a menor categoria restante
    (supressão secundária: o total é conhecido). Retorna (contagens, nota)."""
    contagens = contagens[contagens > 0]
    juntar = contagens < n_min
    if not juntar.any():
        return contagens, ""
    while True:
        sup = contagens[juntar]
        resto = contagens[~juntar]
        if (len(sup) >= 2 and sup.sum() >= n_min) or resto.empty:
            break
        juntar[resto.idxmin()] = True
    mantidas = contagens[~juntar]
    if contagens[juntar].sum() < n_min:   # nem assim chega a n_min: omitir
        return mantidas, "categorias pequenas omitidas (privacidade)"
    outras = pd.Series({"Outras (agrupadas)": contagens[juntar].sum()})
    return pd.concat([mantidas, outras]), f"{int(juntar.sum())} categorias agrupadas em 'Outras' (privacidade)"


def grafico_categorias(serie, n_min, titulo, arquivo=None, ax=None):
    """Barras horizontais com % de uma variável categórica, preservando a ordem
    ordinal (se houver) e protegendo categorias pequenas."""
    import matplotlib.pyplot as plt
    categ = isinstance(serie.dtype, pd.CategoricalDtype)
    cont = serie.value_counts(sort=not categ)
    if categ:
        cont = cont.reindex([c for c in serie.cat.categories if c in cont.index])
    total = cont.sum()
    cont, nota = _agrupar_pequenas(cont, n_min)
    prop = 100 * cont / total
    novo = ax is None
    if novo:
        fig, ax = plt.subplots(figsize=(6.5, 0.42 * len(prop) + 1.1))
    y = np.arange(len(prop))[::-1]
    ax.barh(y, prop.values, color=COR_SERIE, height=0.6)
    for yi, v, n in zip(y, prop.values, cont.values):
        ax.text(v + 1, yi, f"{v:.0f}% (n={n})", va="center", fontsize=8, color=TINTA2)
    ax.set_yticks(y, [str(i) for i in prop.index])
    ax.set_xlim(0, 118)
    ax.set_xlabel("% dos respondentes")
    ax.grid(axis="y", visible=False)
    ax.set_title(f"{titulo} (n = {total})" + (f"\n{nota}" if nota else ""),
                 loc="left", fontsize=9.5)
    if novo:
        if arquivo:
            ax.figure.savefig(arquivo)
        return ax.figure
    return ax


def painel_categorias(df, mapa, n_min, arquivo=None, colunas=2):
    """Small multiples de grafico_categorias para um dicionário {título: coluna}."""
    import matplotlib.pyplot as plt
    itens = list(mapa.items())
    linhas = int(np.ceil(len(itens) / colunas))
    alturas = []
    for i in range(linhas):
        bloco = itens[i * colunas:(i + 1) * colunas]
        alturas.append(max(df[c].nunique() for _, c in bloco) + 1.5)
    fig, axes = plt.subplots(linhas, colunas, figsize=(13, 0.42 * sum(alturas) + 1),
                             gridspec_kw={"height_ratios": alturas}, squeeze=False)
    for ax, (titulo, col) in zip(axes.flat, itens):
        grafico_categorias(df[col].dropna() if not isinstance(df[col].dtype, pd.CategoricalDtype)
                           else df[col], n_min, titulo, ax=ax)
    for ax in axes.flat[len(itens):]:
        ax.axis("off")
    fig.tight_layout(h_pad=2.5, w_pad=3)
    if arquivo:
        fig.savefig(arquivo)
    return fig


# Escalas ordinais codificadas 0..k (ver codificar_ordinal): rótulos do eixo y nos boxplots
EIXO_ORDINAL = {
    "q15_apoio_ord": ["Não", "1", "2", "3", "4+"],
    "q18_ia_ord": ["Não", "Nunca usei", "Algumas vezes", "Sempre uso"],
}


def rotulo(c):
    """Rótulo longo (ROTULOS), senão o curto (CURTOS), senão o próprio nome."""
    return ROTULOS.get(c, CURTOS.get(c, c))


def grafico_grupos(df, grupo, desfechos, tabela=None, arquivo=None, titulo=None, ncol=4, largura=13):
    """Small multiples: um boxplot por escala, um box por grupo, pontos com jitter.
    `tabela` (saída de comparar_grupos) acrescenta p Holm ao título de cada painel."""
    import matplotlib.pyplot as plt
    niveis = list(df[grupo].dropna().unique())
    if isinstance(df[grupo].dtype, pd.CategoricalDtype):
        niveis = [g for g in df[grupo].cat.categories if g in niveis]
    cores = CATEGORICAS[:len(niveis)]
    nlin = int(np.ceil(len(desfechos) / ncol))
    fig, axes = plt.subplots(nlin, ncol, figsize=(largura, 3.1 * nlin + (0.6 if ncol == 1 else 0)),
                             squeeze=False)
    rng = np.random.default_rng(0)
    for n_ax, (ax, d) in enumerate(zip(axes.flat, desfechos)):
        dados = [df.loc[df[grupo] == g, d].dropna().values for g in niveis]
        bp = ax.boxplot(dados, positions=range(len(niveis)), widths=0.5, patch_artist=True,
                        showfliers=False, medianprops={"color": TINTA, "linewidth": 2})
        for patch, c in zip(bp["boxes"], cores):
            patch.set(facecolor=c, alpha=0.35, edgecolor=c, linewidth=1.5)
        for k, (v, c) in enumerate(zip(dados, cores)):
            ax.scatter(k + rng.uniform(-0.15, 0.15, len(v)), v, s=12, color=c,
                       edgecolors="#fcfcfb", linewidths=0.6, zorder=3)
        ax.set_xticks(range(len(niveis)), [f"{g}\n(n={len(v)})" for g, v in zip(niveis, dados)],
                      fontsize=7.5)
        rot = rotulo(d)
        sub = ""
        if tabela is not None and rot in tabela.index:
            p = tabela.loc[rot, "p_holm"]
            sub = "não testado" if pd.isna(p) else f"p Holm = {p:.3f}{' *' if tabela.loc[rot, 'sig'] else ''}"
            if "efeito" in tabela.columns and pd.notna(tabela.loc[rot, "efeito"]):
                sub = f"{tabela.loc[rot, 'medida']} = {tabela.loc[rot, 'efeito']:+.2f} · " + sub
            if "ic95_inf" in tabela.columns and pd.notna(tabela.loc[rot, "ic95_inf"]):
                sub += f"\nIC95 [{tabela.loc[rot, 'ic95_inf']:+.2f}; {tabela.loc[rot, 'ic95_sup']:+.2f}]"
        ax.set_title(f"{rot[:38]}\n{sub}", fontsize=8.5, loc="left")
        if d in EIXO_ORDINAL:
            cats = EIXO_ORDINAL[d]
            ax.set_ylim(-0.5, len(cats) - 0.5 + 0.3)
            ax.set_yticks(range(len(cats)), cats, fontsize=7.5)
        else:
            ax.set_ylim(-0.5, 10.8)
            if n_ax % ncol:
                ax.tick_params(labelleft=False)
        ax.grid(axis="x", visible=False)
    for ax in axes.flat[len(desfechos):]:
        ax.axis("off")
    if titulo:
        fig.suptitle(titulo, x=0.01, ha="left", fontsize=11)
    fig.tight_layout()
    if arquivo:
        fig.savefig(arquivo)
    return fig


def grafico_pares(df, pares, arquivo=None, titulo=None):
    """Dispersão (com jitter) dos pares correlacionados; pares = [(x, y, rho, p_holm)]."""
    import matplotlib.pyplot as plt
    if not pares:
        return None
    ncol = min(3, len(pares))
    nlin = int(np.ceil(len(pares) / ncol))
    fig, axes = plt.subplots(nlin, ncol, figsize=(4.3 * ncol, 3.6 * nlin), squeeze=False)
    rng = np.random.default_rng(0)
    for ax, (x, y, rho, p) in zip(axes.flat, pares):
        sub = df[[x, y]].dropna()
        ax.scatter(sub[x] + rng.uniform(-.2, .2, len(sub)), sub[y] + rng.uniform(-.2, .2, len(sub)),
                   s=22, color=COR_SERIE, alpha=0.75, edgecolors="#fcfcfb", linewidths=0.6)
        ax.set_xlabel(CURTOS.get(x, x), fontsize=8.5)
        ax.set_ylabel(CURTOS.get(y, y), fontsize=8.5)
        ax.set_title(f"ρ = {rho:.2f} · p Holm = {p:.3f} · n = {len(sub)}", fontsize=8.5, loc="left")
    for ax in axes.flat[len(pares):]:
        ax.axis("off")
    if titulo:
        fig.suptitle(titulo, x=0.01, ha="left", fontsize=11)
    fig.tight_layout()
    if arquivo:
        fig.savefig(arquivo)
    return fig


def grafico_cruzadas(tabelas, n_min, arquivo=None, titulo=None):
    """Barras empilhadas 100% para cada tabela cruzada (linhas = grupos).
    Linhas com n < n_min não são desenhadas (privacidade)."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    itens = list(tabelas.items())
    ncol = 2
    nlin = int(np.ceil(len(itens) / ncol))
    fig, axes = plt.subplots(nlin, ncol, figsize=(13, 2.1 * nlin + 0.6), squeeze=False)
    for ax, (nome, ct) in zip(axes.flat, itens):
        if tem_celula_pequena(ct, n_min):
            ax.axis("off")
            ax.set_title(nome.replace("g_", ""), loc="left", fontsize=9)
            ax.text(0, 0.5, f"Gráfico omitido: há célula com n < {n_min}\n"
                    "(as % revelariam a contagem).", fontsize=8.5, color=MUDO,
                    transform=ax.transAxes)
            continue
        prop = 100 * ct.div(ct.sum(axis=1), axis=0)
        esq = np.zeros(len(prop))
        for k, col in enumerate(prop.columns):
            ax.barh(range(len(prop)), prop[col], left=esq, color=CATEGORICAS[k], height=0.6,
                    edgecolor="#fcfcfb", linewidth=2)
            for i, v in enumerate(prop[col]):
                if v >= 12:
                    ax.text(esq[i] + v / 2, i, f"{v:.0f}%", ha="center", va="center", fontsize=7.5,
                            color="#ffffff")
            esq += prop[col].values
        ax.set_yticks(range(len(prop)), [f"{i} (n={n})" for i, n in zip(prop.index, ct.sum(axis=1))],
                      fontsize=8)
        ax.set_xlim(0, 100)
        ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
        ax.grid(axis="y", visible=False)
        ax.invert_yaxis()
        ax.set_title(nome.replace("g_", ""), loc="left", fontsize=9)
        ax.legend(handles=[Patch(color=CATEGORICAS[k], label=c) for k, c in enumerate(prop.columns)],
                  ncol=len(prop.columns), fontsize=7.5, frameon=False, loc="lower left",
                  bbox_to_anchor=(0, -0.42))
    for ax in axes.flat[len(itens):]:
        ax.axis("off")
    if titulo:
        fig.suptitle(titulo, x=0.01, ha="left", fontsize=11)
    fig.tight_layout(h_pad=2.2)
    if arquivo:
        fig.savefig(arquivo)
    return fig


def grafico_poder(ds, razao, alpha, cenarios, n_max=400, arquivo=None):
    """Curvas de poder (TTestIndPower) × nº total de respondentes da pergunta de neurodivergência,
    mantendo a razão neurodiv.:não observada. `cenarios` = [(rótulo, n_total)]."""
    import matplotlib.pyplot as plt
    from statsmodels.stats.power import TTestIndPower
    pw = TTestIndPower()
    ns = np.arange(6, n_max + 1, 2)
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    for k, d in enumerate(ds):
        poder = [pw.power(effect_size=d, nobs1=n / (1 + razao), ratio=razao, alpha=alpha)
                 for n in ns]
        ax.plot(ns, poder, color=CATEGORICAS[k], linewidth=2)
        ax.text(ns[-1] + 4, poder[-1], f"d = {d}", va="center", fontsize=8.5, color=TINTA2)
    ax.axhline(0.8, color=MUDO, linestyle="--", linewidth=1)
    ax.text(ns[0], 0.815, "poder = 0,80", fontsize=8, color=MUDO)
    ultimo = -1e9
    for rot, n in sorted(cenarios, key=lambda c: c[1]):
        ax.axvline(n, color="#c3c2b7", linewidth=1)
        x = max(n, ultimo + 0.035 * n_max)   # afasta rótulos de cenários próximos
        ax.text(x, 1.02, f"{rot} (n={n})", rotation=90, va="bottom", ha="center",
                fontsize=7.5, color=TINTA2)
        ultimo = x
    ax.set_xlim(0, n_max + 40)
    ax.set_ylim(0, 1)
    ax.set_xlabel(f"Nº de respondentes da pergunta de neurodivergência (razão não-ND : ND = {razao:.1f} : 1)")
    ax.set_ylabel("Poder (bilateral)")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    if arquivo:
        fig.savefig(arquivo)
    return fig


def grafico_efeitos(sig, arquivo=None, titulo=None):
    """Dot plot dos tamanhos de efeito dos resultados significativos após Holm."""
    import matplotlib.pyplot as plt
    if sig.empty:
        return None
    s = sig.copy()
    s["rot"] = s["comparação"].str.slice(0, 70)
    s = s.iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 0.45 * len(s) + 1.2))
    for i, r in enumerate(s.itertuples()):
        cor = CATEGORICAS[0] if r.medida == "ρ" else CATEGORICAS[1]
        ax.plot([0, r.efeito], [i, i], color="#c3c2b7", linewidth=1.5)
        ax.scatter(r.efeito, i, s=60, color=cor, edgecolors="#fcfcfb", linewidths=1.5, zorder=3)
        ax.text(r.efeito + 0.02, i, f"{r.medida} = {r.efeito:.2f}", va="center", fontsize=8, color=TINTA2)
    ax.set_yticks(range(len(s)), s["rot"], fontsize=8)
    ax.axvline(0, color="#c3c2b7", linewidth=1)
    ax.set_xlim(min(0, s["efeito"].min()) - 0.05, 1.05)
    ax.set_xlabel("Tamanho de efeito (ρ de Spearman · r do Mann-Whitney · V de Cramér)")
    ax.grid(axis="y", visible=False)
    if titulo:
        ax.set_title(titulo, loc="left", fontsize=10)
    fig.tight_layout()
    if arquivo:
        fig.savefig(arquivo)
    return fig


# ===========================================================================
# Mapa exploratório de associações (todos os agrupamentos × todas as escalas)
# ===========================================================================
def _indicador(df, col, positivo):
    """1 onde df[col] == positivo, 0 nos demais valores válidos, NaN se faltante."""
    s = df[col]
    return pd.Series(np.where(s == positivo, 1.0, 0.0), index=df.index).where(s.notna())


def mapa_associacoes(df, linhas, desfechos, n_min, excluir=()):
    """Associação de cada variável-linha com cada escala-desfecho.

    linhas: {rótulo: ("binario", coluna, valor_positivo) | ("ordinal", coluna)}
    - binário × escala -> correlação ponto-bisserial de postos (rank-biserial),
      r_rb = 2·U/(n1·n0) − 1, p do Mann-Whitney bilateral. r_rb > 0: o grupo
      'positivo' tende a ter valores MAIORES na escala.
    - ordinal × escala -> ρ de Spearman.
    Ambas vão de −1 a 1 (são correlações de postos). Grupo com n < n_min: não testa.
    `excluir`: pares (rótulo, desfecho) redundantes (mesma pergunta), não calculados.
    Holm sobre todas as células testadas (uma única família exploratória).
    """
    from scipy import stats
    linhas_out = []
    for rot, spec in linhas.items():
        for d in desfechos:
            reg = {"variável": rot, "desfecho": d, "n_pos": np.nan, "n_neg": np.nan,
                   "efeito": np.nan, "medida": "", "p": np.nan, "status": ""}
            if (rot, d) in excluir:
                reg["status"] = "redundante"
                linhas_out.append(reg); continue
            if spec[0] == "binario":
                _, col, pos = spec
                ind = _indicador(df, col, pos)
                sub = pd.DataFrame({"g": ind, "y": df[d]}).dropna()
                a, b = sub.loc[sub.g == 1, "y"], sub.loc[sub.g == 0, "y"]
                reg.update(n_pos=len(a), n_neg=len(b), medida="r_rb")
                if min(len(a), len(b)) < n_min:
                    reg["status"] = "n < N_MIN_GRUPO"
                else:
                    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
                    reg.update(efeito=2 * u / (len(a) * len(b)) - 1, p=p, status="testado")
            else:
                _, col = spec
                x = df[col].cat.codes.where(df[col].cat.codes >= 0) if isinstance(
                    df[col].dtype, pd.CategoricalDtype) else df[col]
                sub = pd.DataFrame({"x": x, "y": df[d]}).dropna()
                reg.update(n_pos=len(sub), medida="ρ")
                if sub.x.nunique() < 2 or sub.x.value_counts().min() < n_min:   # n por categoria
                    reg["status"] = "n < N_MIN_GRUPO"
                else:
                    rho, p = stats.spearmanr(sub.x, sub.y)
                    reg.update(efeito=rho, p=p, status="testado")
            linhas_out.append(reg)
    t = pd.DataFrame(linhas_out)
    # Privacidade: n de grupos não testados (podem ser < N_MIN_CELULA) não é exibido nem salvo.
    t.loc[t["status"] != "testado", ["n_pos", "n_neg"]] = np.nan
    t["p_holm"] = holm(t["p"]).values
    t["sig"] = np.where(t["p_holm"] < 0.05, "*", "")
    return t


def magnitude(v):
    """Rótulo de magnitude (convenção de Cohen para correlações)."""
    if pd.isna(v):
        return ""
    a = abs(v)
    return "desprezível" if a < .1 else "pequena" if a < .3 else "média" if a < .5 else "grande"


def associacoes_binarias(df, linhas, n_min_celula, n_min_grupo, excluir_fontes=None):
    """φ (com sinal) entre todos os pares de variáveis binárias de `linhas`
    (só as do tipo 'binario'), p do teste exato de Fisher, Holm na família.
    Pares com alguma célula 1..n_min_celula-1 são mascarados (o φ e as margens
    permitiriam reconstruir a contagem). Pares da mesma pergunta não são calculados."""
    from scipy import stats
    excluir_fontes = excluir_fontes or {}
    bins = {r: s for r, s in linhas.items() if s[0] == "binario"}
    rots = list(bins)
    regs = []
    for i, a in enumerate(rots):
        for b in rots[i + 1:]:
            reg = {"x": a, "y": b, "phi": np.nan, "p": np.nan, "status": ""}
            fa, fb = excluir_fontes.get(a), excluir_fontes.get(b)
            if fa is not None and fa == fb:
                reg["status"] = "mesma pergunta"
                regs.append(reg); continue
            xa = _indicador(df, bins[a][1], bins[a][2])
            xb = _indicador(df, bins[b][1], bins[b][2])
            sub = pd.DataFrame({"a": xa, "b": xb}).dropna()
            ct = pd.crosstab(sub.a, sub.b).reindex(index=[0, 1], columns=[0, 1], fill_value=0)
            if ct.sum(axis=1).min() < n_min_grupo or ct.sum(axis=0).min() < n_min_grupo:
                reg["status"] = "n < N_MIN_GRUPO"
            elif tem_celula_pequena(ct, n_min_celula):
                reg["status"] = "mascarado (célula < N_MIN_CELULA)"
            else:
                (n00, n01), (n10, n11) = ct.values
                den = np.sqrt(ct.sum(axis=1).prod() * ct.sum(axis=0).prod())
                _, p = stats.fisher_exact(ct)
                reg.update(phi=(n11 * n00 - n10 * n01) / den, p=p, status="testado")
            regs.append(reg)
    t = pd.DataFrame(regs)
    t["p_holm"] = holm(t["p"]).values
    t["sig"] = np.where(t["p_holm"] < 0.05, "*", "")
    return t


def grafico_mapa(longo, linhas_ordem, colunas_ordem, valor, rot_cols=None, arquivo=None,
                 titulo=None, triangular=False):
    """Mapa de calor divergente (−1 a 1) com o valor e '*' (p Holm < 0,05).
    Células não testadas ficam em branco com um traço."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("div", [DIVERGENTE[0], "#f0efec", DIVERGENTE[4]])
    eixo_y, eixo_x = ("y", "x") if triangular else ("variável", "desfecho")
    m = longo.pivot(index=eixo_y, columns=eixo_x, values=valor).reindex(index=linhas_ordem,
                                                                       columns=colunas_ordem)
    s = longo.pivot(index=eixo_y, columns=eixo_x, values="sig").reindex(index=linhas_ordem,
                                                                       columns=colunas_ordem)
    st = longo.pivot(index=eixo_y, columns=eixo_x, values="status").reindex(index=linhas_ordem,
                                                                           columns=colunas_ordem)
    fig, ax = plt.subplots(figsize=(0.95 * len(colunas_ordem) + 4.5, 0.42 * len(linhas_ordem) + 1.8))
    im = ax.imshow(m.values.astype(float), cmap=cmap, vmin=-1, vmax=1, aspect="auto")
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            v, stt = m.values[i, j], st.values[i, j]
            if pd.isna(v):
                if isinstance(stt, str) and stt:
                    ax.text(j, i, "–", ha="center", va="center", fontsize=8, color=MUDO)
                continue
            ax.text(j, i, f"{v:+.2f}{s.values[i, j]}", ha="center", va="center", fontsize=7.5,
                    color="#ffffff" if abs(v) > .55 else TINTA,
                    fontweight="bold" if s.values[i, j] else "normal")
    ax.set_xticks(range(m.shape[1]), rot_cols or [CURTOS.get(c, c) for c in colunas_ordem],
                  rotation=40, ha="right", fontsize=8)
    ax.set_yticks(range(m.shape[0]), linhas_ordem, fontsize=8)
    ax.set_xticks(np.arange(-.5, m.shape[1]), minor=True)
    ax.set_yticks(np.arange(-.5, m.shape[0]), minor=True)
    ax.grid(which="minor", color="#fcfcfb", linewidth=2)
    ax.grid(which="major", visible=False)
    ax.tick_params(which="minor", length=0)
    for e in ax.spines.values():
        e.set_visible(False)
    fig.colorbar(im, ax=ax, shrink=0.6, pad=0.02,
                 label="associação (−1 a +1) · * = p Holm < 0,05 · – = não testado")
    if titulo:
        ax.set_title(titulo, loc="left", fontsize=10)
    fig.tight_layout()
    if arquivo:
        fig.savefig(arquivo)
    return fig


# ===========================================================================
# 05e · Perfis: cada linha do mapa (grupo vs complementar) × escalas, com DP
# ===========================================================================
def slug(s):
    """Nome de arquivo seguro (ascii, minúsculas, _)."""
    import re
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:60]


def grupo_da_linha(df, spec):
    """Série categórica com os grupos de uma linha do mapa.
    binário: [grupo positivo, complementar]; ordinal: as próprias categorias."""
    if spec[0] == "ordinal":
        return df[spec[1]]
    _, col, pos = spec
    if col.startswith(("q19", "q24")):
        rot_pos, rot_neg = "Marcou", "Não marcou"
    else:
        outros = [v for v in df[col].dropna().unique() if v != pos]
        rot_pos, rot_neg = str(pos), (str(outros[0]) if len(outros) == 1 else "Demais")
    ind = _indicador(df, col, pos)
    return pd.Series(pd.Categorical(ind.map({1.0: rot_pos, 0.0: rot_neg}),
                                    categories=[rot_pos, rot_neg]), index=df.index)


def dispersao_por_grupo(df, g, desfechos, n_min_celula, n_min_grupo):
    """Descritiva por grupo (n, mediana, IQR, média, DP) e, por escala, a razão
    DP intragrupo combinado / DP total (< 1: o agrupamento separa as respostas).
    Se algum grupo da linha tem n < n_min_celula (no total ou naquela escala),
    n e estatísticas de TODOS os grupos da linha são mascarados: com o total
    conhecido, a média do complementar revela o n e a soma do grupo pequeno."""
    desc, razao = [], []
    pequeno_linha = g.value_counts().min() < n_min_celula
    for d in desfechos:
        sub = pd.DataFrame({"g": g, "y": df[d]}).dropna()
        ns = sub.groupby("g", observed=False)["y"].size()
        pequeno = pequeno_linha or ns.min() < n_min_celula
        for k, y in sub.groupby("g", observed=False)["y"]:
            ok = not pequeno
            desc.append({"desfecho": d, "grupo": k,
                         "n": np.nan if pequeno else len(y),
                         "mediana": y.median() if ok else np.nan,
                         "IQR": (y.quantile(.75) - y.quantile(.25)) if ok else np.nan,
                         "média": y.mean() if ok else np.nan,
                         "DP": y.std() if ok else np.nan,
                         "n ≥ N_MIN_GRUPO": (not pequeno) and ns.min() >= n_min_grupo})
        if ns.min() >= n_min_grupo:
            k = len(ns)
            sp = np.sqrt(sub.groupby("g", observed=False)["y"]
                         .apply(lambda y: (len(y) - 1) * y.var()).sum() / (len(sub) - k))
            razao.append({"desfecho": d, "DP total": sub.y.std(), "DP intragrupo": sp,
                          "razão": sp / sub.y.std()})
    return pd.DataFrame(desc), pd.DataFrame(razao)


# ===========================================================================
# 05f · Classificação das células do mapa: positiva / negativa / sem associação
# ===========================================================================
def _postos(m):
    """Postos médios por linha (empates recebem a média)."""
    from scipy.stats import rankdata
    return rankdata(m, axis=1)


def bootstrap_mapa(df, linhas, desfechos, n_min, excluir=(), B=5000, semente=0):
    """IC bootstrap (percentil) do efeito de cada célula testável do mapa 05d.
    binário -> r_rb = 2·(posto médio do grupo − posto médio do complementar)/N
    (idêntico a 2U/(n1·n0) − 1); reamostragem estratificada por grupo.
    ordinal -> ρ de Spearman; reamostragem de pares.
    Mesmos critérios de teste do mapa (n < n_min: célula não entra).
    Devolve, por célula: efeito, IC95, IC90 e a distribuição bootstrap (_bs)."""
    from scipy.stats import spearmanr
    rng = np.random.default_rng(semente)
    regs = []
    for rot, spec in linhas.items():
        for d in desfechos:
            if (rot, d) in excluir:
                continue
            if spec[0] == "binario":
                ind = _indicador(df, spec[1], spec[2])
                sub = pd.DataFrame({"g": ind, "y": df[d]}).dropna()
                a, b = sub.y[sub.g == 1].values, sub.y[sub.g == 0].values
                if min(len(a), len(b)) < n_min:
                    continue
                n = len(a) + len(b)
                r = _postos(np.concatenate([a, b])[None, :])[0]
                est = 2 * (r[:len(a)].mean() - r[len(a):].mean()) / n
                ma = a[rng.integers(0, len(a), (B, len(a)))]
                mb = b[rng.integers(0, len(b), (B, len(b)))]
                rr = _postos(np.hstack([ma, mb]))
                bs = 2 * (rr[:, :len(a)].mean(1) - rr[:, len(a):].mean(1)) / n
                medida = "r_rb"
            else:
                codes = df[spec[1]].cat.codes
                sub = pd.DataFrame({"x": codes.where(codes >= 0), "y": df[d]}).dropna()
                if sub.x.nunique() < 2 or sub.x.value_counts().min() < n_min:
                    continue
                x, y = sub.x.values, sub.y.values
                est = spearmanr(x, y)[0]
                idx = rng.integers(0, len(x), (B, len(x)))
                rx, ry = _postos(x[idx]), _postos(y[idx])
                rx -= rx.mean(1, keepdims=True)
                ry -= ry.mean(1, keepdims=True)
                with np.errstate(invalid="ignore", divide="ignore"):
                    bs = (rx * ry).sum(1) / np.sqrt((rx ** 2).sum(1) * (ry ** 2).sum(1))
                medida = "ρ"
            regs.append({"variável": rot, "desfecho": d, "medida": medida, "efeito": est,
                         "ic95_inf": np.nanpercentile(bs, 2.5), "ic95_sup": np.nanpercentile(bs, 97.5),
                         "ic90_inf": np.nanpercentile(bs, 5), "ic90_sup": np.nanpercentile(bs, 95),
                         "_bs": bs})
    return pd.DataFrame(regs)


def classificar_mapa(boot, mapa, delta, alpha=0.05):
    """Junta o bootstrap com o p Holm do mapa e classifica cada célula.

    - positiva/negativa, nível 'holm': p Holm < alpha (família do mapa 05d).
    - positiva/negativa, nível 'indicio': IC95 não contém 0, mas não sobrevive a Holm.
    - sem_associacao, nível 'equivalencia': teste de equivalência (TOST por bootstrap)
      com margem ±delta e p corrigido por Holm < alpha.
    - sem_associacao, nível 'indicio': IC90 inteiro dentro de ±delta (TOST sem correção).
    - inconclusivo: o IC é largo demais para dizer qualquer uma das coisas acima.
    """
    t = boot.merge(mapa[["variável", "desfecho", "p", "p_holm"]], on=["variável", "desfecho"], how="left")
    t["p_equiv"] = [max((b <= -delta).mean(), (b >= delta).mean()) for b in t["_bs"]]
    t["p_equiv_holm"] = holm(t["p_equiv"]).values

    def classe(r):
        if r.p_holm < alpha:
            return ("positiva", "holm") if r.efeito > 0 else ("negativa", "holm")
        if r.ic95_inf > 0:
            return ("positiva", "indicio")
        if r.ic95_sup < 0:
            return ("negativa", "indicio")
        if r.p_equiv_holm < alpha:
            return ("sem_associacao", "equivalencia")
        if r.ic90_inf > -delta and r.ic90_sup < delta:
            return ("sem_associacao", "indicio")
        return ("inconclusivo", "")
    cl = [classe(r) for r in t.itertuples()]
    t["classe"] = [c[0] for c in cl]
    t["nível"] = [c[1] for c in cl]
    return t.drop(columns="_bs")


CORES_CLASSE = {"positiva": "#1c5cab", "negativa": "#b8302f", "sem_associacao": "#1baf7a",
                "inconclusivo": "#a8a7a0"}


# ===========================================================================
# 05a · Hipóteses (ver hipoteses.md)
# ===========================================================================
SINAIS = {"+": "positiva (unilateral)", "-": "negativa (unilateral)",
          "0": "sem associação relevante (equivalência ±Δ)", "±": "alguma associação (bilateral)"}


def _vetor_x(df, x, linhas):
    """x é uma linha do mapa 05d (grupo binário ou ordinal) ou uma coluna numérica.
    Devolve (série, tipo) com tipo 'binario' (0/1) ou 'ordinal' (números)."""
    if x in linhas:
        spec = linhas[x]
        if spec[0] == "binario":
            return _indicador(df, spec[1], spec[2]), "binario"
        codes = df[spec[1]].cat.codes
        return codes.where(codes >= 0).astype(float), "ordinal"
    return pd.to_numeric(df[x], errors="coerce"), "ordinal"


def testar_hipoteses(df, hipoteses, linhas, n_min, delta, B=5000, semente=0):
    """Testa cada hipótese em `df`.

    Cada hipótese: {"id", "x", "y", "sinal", "familia", "texto"}.
      x = rótulo de LINHAS_MAPA (grupo) ou coluna numérica; y = coluna numérica.
      sinal "+"/"-" -> teste unilateral; "±" -> bilateral; "0" -> equivalência (TOST
      por bootstrap, margem ±delta: p = max(P(efeito* ≤ −Δ), P(efeito* ≥ Δ))).
    x binário -> Mann-Whitney U, efeito r_rb; x ordinal/escala -> Spearman ρ.
    Grupo com n < n_min (ou n total < n_min, no Spearman) -> não testado.
    IC95 por bootstrap percentil (estratificado por grupo no caso binário)."""
    from scipy.stats import mannwhitneyu, spearmanr
    rng = np.random.default_rng(semente)
    alt = {"+": "greater", "-": "less", "±": "two-sided", "0": "two-sided"}
    regs = []
    for h in hipoteses:
        xv, tipo = _vetor_x(df, h["x"], linhas)
        sub = pd.DataFrame({"x": xv, "y": pd.to_numeric(df[h["y"]], errors="coerce")}).dropna()
        reg = {"id": h["id"], "família": h["familia"], "hipótese": h["texto"], "sinal": h["sinal"]}
        if tipo == "binario":
            a, b = sub.y[sub.x == 1].values, sub.y[sub.x == 0].values
            reg.update({"medida": "r_rb", "n_grupo": len(a), "n_resto": len(b)})
            testavel = min(len(a), len(b)) >= n_min
        else:
            x, y = sub.x.values, sub.y.values
            reg.update({"medida": "ρ", "n_grupo": len(x), "n_resto": np.nan})
            testavel = len(x) >= n_min and len(np.unique(x)) > 1 and len(np.unique(y)) > 1
        if not testavel:
            regs.append({**reg, "teste": "não testado (n < N_MIN_GRUPO)"})
            continue
        if tipo == "binario":
            n = len(a) + len(b)
            u, p = mannwhitneyu(a, b, alternative=alt[h["sinal"]])
            efeito = 2 * u / (len(a) * len(b)) - 1
            ma = a[rng.integers(0, len(a), (B, len(a)))]
            mb = b[rng.integers(0, len(b), (B, len(b)))]
            rr = _postos(np.hstack([ma, mb]))
            bs = 2 * (rr[:, :len(a)].mean(1) - rr[:, len(a):].mean(1)) / n
            teste = "Mann-Whitney U"
        else:
            efeito, p = spearmanr(x, y, alternative=alt[h["sinal"]])
            idx = rng.integers(0, len(x), (B, len(x)))
            rx, ry = _postos(x[idx]), _postos(y[idx])
            rx -= rx.mean(1, keepdims=True)
            ry -= ry.mean(1, keepdims=True)
            with np.errstate(invalid="ignore", divide="ignore"):
                bs = (rx * ry).sum(1) / np.sqrt((rx ** 2).sum(1) * (ry ** 2).sum(1))
            teste = "Spearman"
        if h["sinal"] == "0":
            p = max(np.nanmean(bs <= -delta), np.nanmean(bs >= delta))
            teste = f"equivalência (TOST bootstrap, ±{delta}) sobre {teste}"
        elif h["sinal"] != "±":
            teste += " unilateral"
        regs.append({**reg, "teste": teste, "efeito": efeito,
                     "ic95_inf": np.nanpercentile(bs, 2.5), "ic95_sup": np.nanpercentile(bs, 97.5), "p": p})
    t = pd.DataFrame(regs)
    for c in ["efeito", "ic95_inf", "ic95_sup", "p"]:
        if c not in t:
            t[c] = np.nan
    t["p_holm"] = np.nan
    for fam, idx in t.groupby("família").groups.items():   # Holm dentro de cada família
        ok = t.loc[idx, "p"].notna()
        if ok.any():
            t.loc[ok[ok].index, "p_holm"] = holm(t.loc[ok[ok].index, "p"]).values
    return t.set_index("id")


# ===========================================================================
# 11 · Resumo expandido: família de 29 associações
# ===========================================================================
NOMES_RESUMO = {
    "TRANSICAO": "Dificuldade da transição EM→superior", "EXPECTATIVA": "Expectativa com a Matemática correspondida",
    "PREREQ": "Dificuldade com pré-requisitos", "AULAS": "Aprendizado atribuído às aulas",
    "CONTEUDO_NOVO": "Conteúdo novo visto", "ABSORCAO": "Quanto sente que absorveu",
    "MONITORIAS": "Quanto as monitorias ajudam", "APOIO": "Nº de disciplinas em que precisou de apoio",
    "IA": "Inclinação ao uso de IA devido ao ritmo do curso",
    "PERMANENCIA": "Pretende terminar o curso (Sim = 1)", "INGRESSO": "Ingresso por ENEM (1) × Medalhas (0)",
    "LEITURA": "Método: leitura e anotação, resumos", "GRUPOS": "Método: grupos de estudos",
    "CRONOGRAMA": "Método: cronograma ou plano de estudos", "PERGUNTAR_IA": "Método: perguntar a uma IA",
    "DES_TEMPO": "Desafio: gerenciar tempo", "DES_ORGANIZACAO": "Desafio: organização de estudos",
    "DES_TAREFAS": "Desafio: tarefas de casa",
}


def codificar_resumo(df):
    """Variáveis da seção 11, com os nomes do roteiro do resumo expandido."""
    d = pd.DataFrame(index=df.index)
    for nome, col in {"TRANSICAO": "q12_transicao", "EXPECTATIVA": "q13_expectativa", "PREREQ": "q14_prereq",
                      "AULAS": "q17_aulas", "CONTEUDO_NOVO": "q25_novo", "ABSORCAO": "q25_absorveu",
                      "MONITORIAS": "q25_monitoria"}.items():
        d[nome] = df[col]
    d["APOIO"] = codificar_ordinal(df["q15_apoio"])   # Não=0 … 4+=4
    d["IA"] = codificar_ordinal(df["q18_ia"])          # Não=0, nunca usei=1, algumas vezes=2, sempre uso=3
    d["PERMANENCIA"] = _indicador(df, "q21_terminar", "Sim")
    d["INGRESSO"] = _indicador(df, "q09_forma_ingresso", "ENEM")
    for nome, col in {"LEITURA": "q24_leitura", "GRUPOS": "q24_grupos", "CRONOGRAMA": "q24_cronograma",
                      "PERGUNTAR_IA": "q24_perguntar_ia", "DES_TEMPO": "q19_tempo",
                      "DES_ORGANIZACAO": "q19_organizacao", "DES_TAREFAS": "q19_tarefas"}.items():
        d[nome] = df[col].astype(float)
    return d


def associacoes_familia(d, familia, n_min, delta=0.2, B=10000, semente=42, alpha=0.05):
    """Uma família de associações, com Holm sobre todas.

    familia: lista de dicts {"id", "bloco", "x", "y"}. x binário (0/1) -> r_rb do grupo x=1
    contra x=0 (= P(1 > 0) − P(1 < 0) = 2U/(n1·n0) − 1), Mann-Whitney bilateral;
    senão -> Spearman ρ (pares completos). IC95/IC90 por bootstrap percentil
    (estratificado por grupo no r_rb). TOST por bootstrap com margem ±delta:
    p = max(P(efeito* ≤ −Δ), P(efeito* ≥ Δ)). Holm sobre os p e, à parte, sobre os p do TOST."""
    from scipy.stats import mannwhitneyu, spearmanr
    rng = np.random.default_rng(semente)
    regs = []
    for a in familia:
        sub = d[[a["x"], a["y"]]].dropna()
        x, y = sub[a["x"]].values, sub[a["y"]].values
        reg = {"id": a["id"], "bloco": a["bloco"], "x": a["x"], "y": a["y"]}
        binario = set(np.unique(x)) <= {0.0, 1.0}
        if binario:
            g1, g0 = y[x == 1], y[x == 0]
            reg.update({"medida": "r_rb", "n_1": len(g1), "n_0": len(g0),
                        "mediana_1": np.median(g1) if len(g1) else np.nan,
                        "mediana_0": np.median(g0) if len(g0) else np.nan})
            if min(len(g1), len(g0)) < n_min:
                regs.append({**reg, "classificação": "grupo insuficiente"})
                continue
            n = len(g1) + len(g0)
            u, p = mannwhitneyu(g1, g0, alternative="two-sided")
            efeito = 2 * u / (len(g1) * len(g0)) - 1
            m1 = g1[rng.integers(0, len(g1), (B, len(g1)))]
            m0 = g0[rng.integers(0, len(g0), (B, len(g0)))]
            rr = _postos(np.hstack([m1, m0]))
            bs = 2 * (rr[:, :len(g1)].mean(1) - rr[:, len(g1):].mean(1)) / n
        else:
            reg.update({"medida": "ρ", "n_1": len(x), "n_0": np.nan})
            if len(x) < n_min:
                regs.append({**reg, "classificação": "grupo insuficiente"})
                continue
            efeito, p = spearmanr(x, y)
            idx = rng.integers(0, len(x), (B, len(x)))
            rx, ry = _postos(x[idx]), _postos(y[idx])
            rx -= rx.mean(1, keepdims=True)
            ry -= ry.mean(1, keepdims=True)
            with np.errstate(invalid="ignore", divide="ignore"):
                bs = (rx * ry).sum(1) / np.sqrt((rx ** 2).sum(1) * (ry ** 2).sum(1))
        regs.append({**reg, "efeito": efeito,
                     "ic95_inf": np.nanpercentile(bs, 2.5), "ic95_sup": np.nanpercentile(bs, 97.5),
                     "ic90_inf": np.nanpercentile(bs, 5), "ic90_sup": np.nanpercentile(bs, 95),
                     "p": p, "p_tost": max(np.nanmean(bs <= -delta), np.nanmean(bs >= delta))})
    t = pd.DataFrame(regs)
    for c in ["efeito", "ic95_inf", "ic95_sup", "ic90_inf", "ic90_sup", "p", "p_tost"]:
        if c not in t:
            t[c] = np.nan
    t["p_holm"] = holm(t["p"]).values
    t["p_tost_holm"] = holm(t["p_tost"]).values

    def classe(r):
        if pd.isna(r.p):
            return r.classificação
        sentido = "positiva" if r.efeito > 0 else "negativa"
        if r.p_holm < alpha:
            return f"Associação {sentido}"
        if r.ic95_inf > 0 or r.ic95_sup < 0:
            return f"Indício de associação {sentido}"
        if r.p_tost_holm < alpha:
            return "Ausência confirmada"
        if r.ic90_inf > -delta and r.ic90_sup < delta:
            return "Indício de ausência"
        return "Inconclusivo"
    if "classificação" not in t:
        t["classificação"] = np.nan
    t["classificação"] = [classe(r) for r in t.itertuples()]
    return t


CURTOS_RESUMO = {"TRANSICAO": "Dificuldade de transição", "EXPECTATIVA": "Expectativa correspondida",
                 "PREREQ": "Dificuldade c/ pré-requisitos", "AULAS": "Aprendizado nas aulas",
                 "CONTEUDO_NOVO": "Conteúdo novo", "ABSORCAO": "Absorção", "MONITORIAS": "Monitorias ajudam",
                 "APOIO": "Nº de disciplinas c/ apoio", "IA": "Inclinação à IA (ritmo)", "PERMANENCIA": "Pretende terminar",
                 "INGRESSO": "ENEM", "LEITURA": "Leitura/anotação", "GRUPOS": "Grupos de estudos",
                 "CRONOGRAMA": "Cronograma", "PERGUNTAR_IA": "Perguntar a uma IA"}


# ===========================================================================
# 05g · Contrastes dois a dois (turmas; tempo até o ingresso × outra graduação)
# ===========================================================================
def contrastes(df, contrastes, desfechos, binarios, n_min_grupo, n_min_celula,
               delta=0.2, B=5000, semente=0, alpha=0.05):
    """Compara dois grupos (A × B) em cada desfecho, para cada contraste.

    contrastes: lista de (rótulo, máscara_A, máscara_B), máscaras booleanas sobre df.
    desfechos: {coluna: rótulo}. Colunas em `binarios` são 0/1; as demais, escalas ou
    códigos ordinais.
    Efeito: r_rb = P(A > B) − P(A < B), positivo quando A tem valores maiores. Num
    desfecho 0/1, r_rb é a diferença de proporções (p_A − p_B). p: Mann-Whitney
    bilateral (escala/ordinal) ou Fisher exato (0/1). IC95/IC90 por bootstrap
    percentil, estratificado por grupo. TOST por bootstrap com margem ±delta.
    Holm sobre todos os testes realizados (uma família por chamada).
    Não testa se algum grupo tem n < n_min_grupo; num desfecho 0/1, mascara (sem
    teste nem %) se alguma das 4 células tiver 1..n_min_celula−1 pessoas.
    Classificação: a mesma do 05f (classe positiva/negativa/sem_associacao/inconclusivo)."""
    from scipy.stats import fisher_exact, mannwhitneyu
    rng = np.random.default_rng(semente)
    regs = []
    for rot_c, ma, mb in contrastes:
        for d, rot_d in desfechos.items():
            a = df.loc[ma, d].dropna().values.astype(float)
            b = df.loc[mb, d].dropna().values.astype(float)
            binario = d in binarios
            reg = {"contraste": rot_c, "desfecho": rot_d, "coluna": d,
                   "tipo": "0/1" if binario else "escala/ordinal", "n_A": len(a), "n_B": len(b),
                   "A": "", "B": "", "efeito": np.nan, "status": ""}
            if binario:
                cel = [int(a.sum()), int(len(a) - a.sum()), int(b.sum()), int(len(b) - b.sum())]
                pequena = any(0 < c < n_min_celula for c in cel)
                if not pequena:
                    reg["A"], reg["B"] = f"{100 * a.mean():.0f}%", f"{100 * b.mean():.0f}%"
            else:
                pequena = False
                for g, v in (("A", a), ("B", b)):
                    if len(v) >= n_min_celula:
                        f2 = lambda x: f"{round(float(x), 2):g}"
                        reg[g] = f"{f2(np.median(v))} [{f2(np.quantile(v, .25))}–{f2(np.quantile(v, .75))}]"
            if min(len(a), len(b)) < n_min_grupo:
                reg["status"] = "n < N_MIN_GRUPO (só descritiva)"
            elif pequena:
                reg["status"] = "mascarado (célula < N_MIN_CELULA)"
            elif len(np.unique(np.concatenate([a, b]))) < 2:
                reg["status"] = "sem variação"
            else:
                n = len(a) + len(b)
                r = _postos(np.concatenate([a, b])[None, :])[0]
                est = 2 * (r[:len(a)].mean() - r[len(a):].mean()) / n
                if binario:
                    p = fisher_exact([[cel[0], cel[1]], [cel[2], cel[3]]])[1]
                else:
                    p = mannwhitneyu(a, b, alternative="two-sided")[1]
                bm = np.hstack([a[rng.integers(0, len(a), (B, len(a)))],
                                b[rng.integers(0, len(b), (B, len(b)))]])
                rr = _postos(bm)
                bs = 2 * (rr[:, :len(a)].mean(1) - rr[:, len(a):].mean(1)) / n
                reg.update(efeito=est, p=p, status="testado",
                           ic95_inf=np.percentile(bs, 2.5), ic95_sup=np.percentile(bs, 97.5),
                           ic90_inf=np.percentile(bs, 5), ic90_sup=np.percentile(bs, 95),
                           p_equiv=max((bs <= -delta).mean(), (bs >= delta).mean()))
            regs.append(reg)
    t = pd.DataFrame(regs)
    for c in ["p", "ic95_inf", "ic95_sup", "ic90_inf", "ic90_sup", "p_equiv"]:
        if c not in t:
            t[c] = np.nan
    t["p_holm"] = holm(t["p"]).values
    t["p_equiv_holm"] = holm(t["p_equiv"]).values
    t["sig"] = np.where(t["p_holm"] < alpha, "*", "")

    return _classificar(t, delta, alpha)


def _classificar(t, delta, alpha=0.05):
    """Classe e nível de cada linha (mesma regra do 05f). Requer as colunas status,
    efeito, p_holm, ic95_inf/sup, ic90_inf/sup e p_equiv_holm."""
    def classe(r):
        if r.status != "testado":
            return ("não testado", "")
        if r.p_holm < alpha:
            return ("positiva" if r.efeito > 0 else "negativa", "holm")
        if r.ic95_inf > 0:
            return ("positiva", "indicio")
        if r.ic95_sup < 0:
            return ("negativa", "indicio")
        if r.p_equiv_holm < alpha:
            return ("sem_associacao", "equivalencia")
        if r.ic90_inf > -delta and r.ic90_sup < delta:
            return ("sem_associacao", "indicio")
        return ("inconclusivo", "")
    cl = [classe(r) for r in t.itertuples()]
    t["classe"], t["nível"] = [c[0] for c in cl], [c[1] for c in cl]
    return t


def placar_contrastes(t):
    """Por contraste: quantos desfechos com A > B e com B > A, por nível de evidência."""
    s = t[t["status"] == "testado"].copy()
    s["lado"] = np.where(s["efeito"] > 0, "A maior", "B maior")
    s["evidência"] = np.select([s["nível"] == "holm", (s["nível"] == "indicio") & s["classe"].isin(["positiva", "negativa"])],
                               ["Holm", "indício"], "inconclusivo / sem diferença")
    return (s.groupby(["contraste", "evidência", "lado"]).size().unstack(fill_value=0)
            .reindex(columns=["A maior", "B maior"], fill_value=0))


# ===========================================================================
# 05h · Agregações
# ===========================================================================
def indice_postos(df, cols):
    """Índice ordinal: média dos postos percentuais (0–1] de cada pessoa nas colunas.
    Usa só a ordem das respostas (não as distâncias entre notas), o que é adequado a
    escalas ordinais. Só é calculado para quem respondeu a todas as colunas.
    Os postos são relativos à amostra: o índice compara pessoas, não é uma nota absoluta."""
    completo = df[cols].notna().all(axis=1)
    r = df.loc[completo, cols].rank(pct=True)
    return r.mean(axis=1).reindex(df.index)


# ===========================================================================
# 05i · Matriz e rede de associações (todas × todas)
# ===========================================================================
def matriz_associacoes(df, variaveis, binarios, n_min_grupo, n_min_celula, excluir=(),
                       delta=0.2, B=5000, semente=0, alpha=0.05):
    """ρ de Spearman entre todos os pares de `variaveis` ({coluna: rótulo}), pares completos.

    Uma medida só para todos os pares, para comparar o nível das relações: ρ entre duas
    variáveis 0/1 é o φ; entre 0/1 e escala é uma correlação de postos. p: Spearman, ou
    Fisher exato quando as duas são 0/1. IC95/IC90 por bootstrap de pares; TOST ±delta;
    Holm sobre todos os pares testados; classificação igual à do 05f.
    Não testa: variável 0/1 com algum lado < n_min_grupo; par 0/1 × 0/1 com alguma
    célula entre 1 e n_min_celula − 1 (mascarado: o φ e as margens revelariam a contagem).
    `excluir`: pares {a, b} derivados um do outro (não calculados)."""
    from scipy.stats import fisher_exact, spearmanr
    rng = np.random.default_rng(semente)
    excluir = {frozenset(p) for p in excluir}
    cols = list(variaveis)
    regs = []
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            reg = {"x": a, "y": b, "rot_x": variaveis[a], "rot_y": variaveis[b], "efeito": np.nan, "status": ""}
            sub = df[[a, b]].astype(float).dropna()
            reg["n"] = len(sub)
            if frozenset((a, b)) in excluir:
                reg["status"] = "derivado (não calculado)"
                regs.append(reg)
                continue
            pequeno = any(c in binarios and min((sub[c] == 1).sum(), (sub[c] == 0).sum()) < n_min_grupo
                          for c in (a, b))
            ct = None
            if a in binarios and b in binarios:
                ct = pd.crosstab(sub[a], sub[b]).reindex(index=[0.0, 1.0], columns=[0.0, 1.0], fill_value=0)
            if pequeno:
                reg["status"] = "n < N_MIN_GRUPO"
            elif ct is not None and tem_celula_pequena(ct, n_min_celula):
                reg["status"] = "mascarado (célula < N_MIN_CELULA)"
            elif sub[a].nunique() < 2 or sub[b].nunique() < 2:
                reg["status"] = "sem variação"
            else:
                x, y = sub[a].values, sub[b].values
                rho, p = spearmanr(x, y)
                if ct is not None:
                    p = fisher_exact(ct.values)[1]
                idx = rng.integers(0, len(x), (B, len(x)))
                rx, ry = _postos(x[idx]), _postos(y[idx])
                rx -= rx.mean(1, keepdims=True)
                ry -= ry.mean(1, keepdims=True)
                with np.errstate(invalid="ignore", divide="ignore"):
                    bs = (rx * ry).sum(1) / np.sqrt((rx ** 2).sum(1) * (ry ** 2).sum(1))
                reg.update(efeito=rho, p=p, status="testado",
                           ic95_inf=np.nanpercentile(bs, 2.5), ic95_sup=np.nanpercentile(bs, 97.5),
                           ic90_inf=np.nanpercentile(bs, 5), ic90_sup=np.nanpercentile(bs, 95),
                           p_equiv=max(np.nanmean(bs <= -delta), np.nanmean(bs >= delta)))
            regs.append(reg)
    t = pd.DataFrame(regs)
    for c in ["p", "ic95_inf", "ic95_sup", "ic90_inf", "ic90_sup", "p_equiv"]:
        if c not in t:
            t[c] = np.nan
    t["p_holm"] = holm(t["p"]).values
    t["p_equiv_holm"] = holm(t["p_equiv"]).values
    return _classificar(t, delta, alpha)


def grafico_matriz(t, ordem, rotulos, temas=None, arquivo=None, titulo=None):
    """Triângulo inferior de ρ. Número em negrito com * = sobrevive a Holm; número escuro =
    indício (IC95 exclui 0); número claro = inconclusivo ou sem associação; – = não calculado.
    `temas` ({coluna: tema}) desenha linhas separando os blocos de temas."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("div", [DIVERGENTE[0], "#f0efec", DIVERGENTE[4]])
    k = len(ordem)
    pos = {c: i for i, c in enumerate(ordem)}
    m = np.full((k, k), np.nan)
    info = {}
    for r in t.itertuples():
        i, j = sorted((pos[r.x], pos[r.y]), reverse=True)   # linha > coluna: triângulo inferior
        m[i, j] = r.efeito if r.status == "testado" else np.nan
        info[(i, j)] = r
    fig, ax = plt.subplots(figsize=(0.42 * k + 4, 0.38 * k + 2.2))
    im = ax.imshow(np.ma.masked_invalid(m), cmap=cmap, vmin=-1, vmax=1)
    for (i, j), r in info.items():
        if r.status != "testado":
            ax.text(j, i, "–", ha="center", va="center", fontsize=6, color=MUDO)
            continue
        forte = r.nível == "holm"
        indicio = r.nível == "indicio" and r.classe in ("positiva", "negativa")
        txt = f"{r.efeito:+.2f}".replace("0.", ".") + ("*" if forte else "")
        cor = ("#ffffff" if abs(r.efeito) > .55 else TINTA) if (forte or indicio) else MUDO
        ax.text(j, i, txt, ha="center", va="center", fontsize=5.6, color=cor,
                fontweight="bold" if forte else "normal")
    ax.set_xticks(range(k), [rotulos[c] for c in ordem], rotation=55, ha="right", fontsize=7)
    ax.set_yticks(range(k), [rotulos[c] for c in ordem], fontsize=7)
    ax.set_xlim(-0.5, k - 1.5)
    ax.set_ylim(k - 0.5, 0.5)
    if temas:
        for i in range(1, k):
            if temas[ordem[i]] != temas[ordem[i - 1]]:
                ax.axhline(i - 0.5, color=TINTA2, lw=0.8)
                ax.axvline(i - 0.5, color=TINTA2, lw=0.8)
    ax.grid(False)
    for e in ax.spines.values():
        e.set_visible(False)
    fig.colorbar(im, ax=ax, shrink=0.5, pad=0.02,
                 label="ρ de Spearman · negrito* = Holm · escuro = indício · claro = inconclusivo")
    if titulo:
        ax.set_title(titulo, loc="left", fontsize=10)
    fig.tight_layout()
    if arquivo:
        fig.savefig(arquivo)
    return fig


def grafico_rede(t, ordem, rotulos, temas, arquivo=None, titulo=None):
    """Rede das associações: nós = variáveis (cor = tema, em círculo, agrupados por tema);
    arestas só para Holm (cheia, grossa) e indício (tracejada); azul = positiva,
    vermelho = negativa; espessura proporcional a |ρ|; tamanho do nó = nº de ligações."""
    import matplotlib.pyplot as plt
    import networkx as nx
    from matplotlib.lines import Line2D
    g = nx.Graph()
    g.add_nodes_from(ordem)
    sel = t[(t["status"] == "testado") & ((t["nível"] == "holm") |
            ((t["nível"] == "indicio") & t["classe"].isin(["positiva", "negativa"])))]
    for r in sel.itertuples():
        g.add_edge(r.x, r.y, rho=r.efeito, forte=r.nível == "holm")
    ang = np.linspace(0, 2 * np.pi, len(ordem), endpoint=False) + np.pi / 2
    pos = {c: (np.cos(a), np.sin(a)) for c, a in zip(ordem, ang)}
    lista_temas = list(dict.fromkeys(temas[c] for c in ordem))
    cor_tema = dict(zip(lista_temas, CATEGORICAS))
    fig, ax = plt.subplots(figsize=(11, 10))
    for forte in (False, True):
        es = [(u, v) for u, v, d in g.edges(data=True) if d["forte"] == forte]
        if not es:
            continue
        nx.draw_networkx_edges(g, pos, edgelist=es, ax=ax,
                               width=[(5 if forte else 2.2) * abs(g[u][v]["rho"]) + 0.4 for u, v in es],
                               edge_color=[DIVERGENTE[4] if g[u][v]["rho"] > 0 else DIVERGENTE[0] for u, v in es],
                               style="solid" if forte else "dashed", alpha=0.9 if forte else 0.55)
    nx.draw_networkx_nodes(g, pos, ax=ax, node_size=[140 + 60 * g.degree(c) for c in ordem],
                           node_color=[cor_tema[temas[c]] for c in ordem], edgecolors="#fcfcfb", linewidths=1.2)
    for c, (px, py) in pos.items():
        ax.text(px * 1.09, py * 1.09, rotulos[c], fontsize=7.5, color=TINTA,
                ha="left" if px > 0.05 else ("right" if px < -0.05 else "center"),
                va="bottom" if py > 0.05 else ("top" if py < -0.05 else "center"))
    hand = [Line2D([], [], color=DIVERGENTE[4], lw=3, label="positiva (Holm)"),
            Line2D([], [], color=DIVERGENTE[0], lw=3, label="negativa (Holm)"),
            Line2D([], [], color=MUDO, lw=1.5, ls="--", label="indício (IC95 exclui 0)")]
    hand += [Line2D([], [], marker="o", ls="none", color=cor_tema[tm], markersize=8, label=tm) for tm in lista_temas]
    ax.legend(handles=hand, loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=8)
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect("equal")
    ax.axis("off")
    if titulo:
        ax.set_title(titulo, loc="left", fontsize=10)
    fig.tight_layout()
    if arquivo:
        fig.savefig(arquivo)
    return fig


# ===========================================================================
# Gráficos de efeito com IC95 e faixa de equivalência (todos no mesmo formato)
# ===========================================================================
# Grupos temáticos: A–E são as seções de hipoteses.md; F e G reúnem o que fica fora delas.
GRUPOS_TEMA = {
    "A": "A. Pré-requisitos, transição e apoio",
    "B": "B. Uso de IA",
    "C": "C. Métodos de estudo",
    "D": "D. Dificuldade de organizar os estudos",
    "E": "E. Trajetória antes do IMPA Tech",
    "F": "F. Permanência (fora das hipóteses H)",
    "G": "G. Aulas e aprendizagem (fora das hipóteses H)",
}
# Ordem de prioridade: uma associação que envolve IA vai para B, mesmo que envolva apoio etc.
_REGRAS_TEMA = [
    ("B", r"\bia\b|q18_ia|perguntar_ia"),
    ("C", r"método|q24_|n_metodos"),
    ("D", r"organiza"),
    ("E", r"enem|ingresso|gradua|outra_grad|escola|privada|após o em|apos1|≥ ?1 ano|idade|turma"),
    ("F", r"risco|terminar|trancou|reprov"),
    ("A", r"transi|pré-req|prereq|apoio|índice|indice|tarefas|tempo|desafio|q12_|q14_|q15_|q19_"),
]


def tema(*textos):
    """Letra do grupo temático (GRUPOS_TEMA) de uma associação, a partir dos nomes ou
    rótulos das variáveis envolvidas."""
    import re
    s = " | ".join(str(x).lower() for x in textos)
    for k, rx in _REGRAS_TEMA:
        if re.search(rx, s):
            return k
    return "G"


def ic_hipoteses(tabs, grupo_de, alpha=0.05):
    """Tabelas de testar_hipoteses ({série: tabela}) -> formato de grafico_ic.
    Associação demonstrada = p Holm < alpha na direção prevista (ou equivalência, sinal "0")."""
    regs = []
    for serie, t in tabs.items():
        for id_, r in t.iterrows():
            if pd.isna(r.get("p")):
                cl = ("não testado", "")
            elif r["p_holm"] < alpha:
                cl = {"+": ("positiva", "holm"), "-": ("negativa", "holm"), "0": ("sem_associacao", "equivalencia")
                      }.get(r["sinal"], ("positiva" if r["efeito"] > 0 else "negativa", "holm"))
            elif r["ic95_inf"] > 0:
                cl = ("positiva", "indicio")
            elif r["ic95_sup"] < 0:
                cl = ("negativa", "indicio")
            else:
                cl = ("inconclusivo", "")
            regs.append({"serie": serie, "grupo": grupo_de[id_], "rotulo": f"{id_}  {r['hipótese']}",
                         "efeito": r.get("efeito"), "ic95_inf": r.get("ic95_inf"), "ic95_sup": r.get("ic95_sup"),
                         "p_holm": r.get("p_holm"), "classe": cl[0], "nível": cl[1]})
    return pd.DataFrame(regs)


_CLASSE_FAMILIA = {"Associação positiva": ("positiva", "holm"), "Associação negativa": ("negativa", "holm"),
                   "Indício de associação positiva": ("positiva", "indicio"),
                   "Indício de associação negativa": ("negativa", "indicio"),
                   "Ausência confirmada": ("sem_associacao", "equivalencia"),
                   "Indício de ausência": ("sem_associacao", "indicio"), "Inconclusivo": ("inconclusivo", "")}


def ic_familia(t):
    """Classe e nível a partir da coluna 'classificação' de associacoes_familia."""
    cl = [_CLASSE_FAMILIA.get(c, ("não testado", "")) for c in t["classificação"]]
    return t.assign(classe=[c[0] for c in cl], nível=[c[1] for c in cl])


def grafico_ic(t, delta, grupos=None, arquivo=None, titulo=None, ordenar=True,
               xlabel="tamanho de efeito (r_rb ou ρ de Spearman) e IC 95% bootstrap"):
    """Efeito e IC95 de cada linha, agrupados por tema, com a faixa ±delta em verde.

    t: colunas grupo, rotulo, efeito, ic95_inf, ic95_sup, p_holm, classe, nível
    (e, opcionalmente, serie). À direita de cada linha: se a associação foi demonstrada
    por Holm (✓, com o p ajustado) ou não. Linha grossa e marcador cheio = Holm;
    marcador vazio = indício ou inconclusivo. ordenar=True ordena cada grupo pelo efeito;
    False mantém a ordem de t (por exemplo, a ordem dos ids das hipóteses)."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    from matplotlib.transforms import blended_transform_factory
    t = t.copy()
    if "serie" not in t:
        t["serie"] = ""
    series = list(dict.fromkeys(t["serie"]))
    presentes = list(dict.fromkeys(t["grupo"]))
    ordem_g = [g for g in (grupos or presentes) if g in presentes] + [g for g in presentes if g not in (grupos or [])]
    linhas = []
    for g in ordem_g:
        sub = t[t["grupo"] == g]
        rots = list(dict.fromkeys(sub["rotulo"]))
        if ordenar:
            ref = sub.drop_duplicates("rotulo", keep="last").set_index("rotulo")["efeito"]
            rots = sorted(rots, key=lambda r: -ref[r] if pd.notna(ref[r]) else 9)
        linhas.append(("g", g))
        linhas += [("r", r) for r in rots]
    n = len(linhas)
    grande = n > 70
    fs = 6 if grande else 7.5
    fig, ax = plt.subplots(figsize=(12, (0.155 if grande else 0.25) * n + 1.9))
    ax.axvspan(-delta, delta, color=CORES_CLASSE["sem_associacao"], alpha=0.13, lw=0)
    ax.axvline(0, color=MUDO, lw=1)
    desl = np.linspace(-0.2, 0.2, len(series)) if len(series) > 1 else [0.0]
    marcas = ["o", "s", "^", "D"]
    direita = blended_transform_factory(ax.transAxes, ax.transData)
    yt, yl = [], []
    for y, (tipo, val) in enumerate(linhas):
        if tipo == "g":
            ax.text(0.0, y, val, transform=direita, fontsize=fs + 1, fontweight="bold", va="center",
                    ha="left", color=TINTA)
            continue
        yt.append(y)
        yl.append(val if len(val) <= 78 else val[:76] + "…")
        notas, alguma_holm = [], False
        for k, (s, d) in enumerate(zip(series, desl)):
            rr = t[(t["rotulo"] == val) & (t["serie"] == s)]
            pref = f"{s}: " if len(series) > 1 else ""
            if rr.empty:
                continue
            r = rr.iloc[0]
            if pd.isna(r["efeito"]):
                notas.append(pref + "não testado")
                continue
            c = CORES_CLASSE.get(r["classe"], MUDO)
            forte = r["nível"] in ("holm", "equivalencia")
            ax.plot([r["ic95_inf"], r["ic95_sup"]], [y + d, y + d], color=c, lw=2.4 if forte else 1.2,
                    solid_capstyle="round")
            ax.plot(r["efeito"], y + d, marcas[k % 4], ms=5.5 if forte else 4.5, color=c,
                    markerfacecolor=c if forte else "#fcfcfb", markeredgewidth=1.1, zorder=3)
            p = r["p_holm"]
            if r["nível"] == "holm":
                notas.append(pref + ("✓ associação (Holm, p < 0.001)" if p < 0.001 else f"✓ associação (Holm, p = {p:.3f})"))
                alguma_holm = True
            elif r["nível"] == "equivalencia":
                notas.append(pref + "✓ ausência (equivalência, Holm)")
                alguma_holm = True
            else:
                notas.append(pref + (f"não demonstrada (p Holm = {p:.3f})" if pd.notna(p) and p < 0.1 else
                                     f"não demonstrada (p Holm = {p:.2f})" if pd.notna(p) else "não demonstrada"))
        ax.text(1.01, y, " · ".join(notas), transform=direita, fontsize=fs, va="center", ha="left",
                color=TINTA if alguma_holm else MUDO, fontweight="bold" if alguma_holm else "normal")
    ax.set_yticks(yt, yl, fontsize=fs)
    ax.set_ylim(n - 0.5, -0.7)
    ax.set_xlim(-1, 1)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.grid(axis="y", visible=False)
    hand = [Line2D([], [], color=DIVERGENTE[4], lw=2.4, marker="o", label="associação demonstrada (Holm)"),
            Line2D([], [], color=DIVERGENTE[4], lw=1.2, marker="o", markerfacecolor="#fcfcfb",
                   label="indício: IC95 exclui 0, sem Holm"),
            Line2D([], [], color=CORES_CLASSE["sem_associacao"], lw=1.2, marker="o", markerfacecolor="#fcfcfb",
                   label="indício de ausência: IC90 dentro da faixa"),
            Line2D([], [], color=CORES_CLASSE["inconclusivo"], lw=1.2, marker="o", markerfacecolor="#fcfcfb",
                   label="inconclusivo"),
            Patch(color=CORES_CLASSE["sem_associacao"], alpha=0.35, label=f"faixa ±{delta}: efeito irrelevante")]
    if len(series) > 1:
        hand += [Line2D([], [], color=MUDO, marker=marcas[k % 4], ls="none", label=s) for k, s in enumerate(series)]
    ax.legend(handles=hand, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3,
              frameon=False, fontsize=7.5)
    if titulo:   # acima da legenda (que fica logo acima do eixo), qualquer que seja a altura da figura
        ax.set_title(titulo, loc="left", fontsize=10.5, pad=38)
    fig.tight_layout()
    if arquivo:
        fig.savefig(arquivo)
    return fig



# ===========================================================================
# 12 · Análise de conteúdo categorial (Bardin) das sugestões (questão 21 do Apêndice A; q22_sugestoes no CSV)
# ===========================================================================
# Tudo que tem texto literal ou id_resposta fica em `pasta` (qualitativa/, fora do git).
COLUNAS_CODIFICACAO = ["id_curto", "trecho", "categoria", "observacao"]
COLUNAS_LIVRO = ["categoria", "definicao", "criterio_inclusao", "criterio_exclusao", "exemplo"]
_NAO_SUGESTAO = (r"^(n[aã]o|sim|s|n|nada|n/?a|n[aã]o sei|n[aã]o tenho|-+|\.+"
                 r"|(nenhum|nenhuma|sem)( sugest[aãoõ]+e?s?)?|n[aã]o tenho sugest[aãoõ]+e?s?)$")


def _normalizar_curto(t):
    """Minúsculas, sem espaços nem pontuação nas pontas (para comparar 'Não.' com 'não')."""
    import re
    return re.sub(r"^[\s.!?,;:]+|[\s.!?,;:]+$", "", str(t).strip().lower())


def nao_e_sugestao(t):
    """True para respostas do tipo 'não', 'sim', 'nada', 'não sei' (não contam como sugestão)."""
    import re
    n = _normalizar_curto(t)
    return n in RESPOSTAS_VAZIAS or bool(re.match(_NAO_SUGESTAO, n))


def _csv_em_branco(arquivo, colunas):
    """Cria o CSV só com o cabeçalho, se ainda não existir. Nunca sobrescreve. Devolve True se criou."""
    import os
    if os.path.exists(arquivo):
        return False
    pd.DataFrame(columns=colunas).to_csv(arquivo, index=False, encoding="utf-8-sig")
    return True


def preparar_codificacao_q21(base, nlp, nomes_extra=(), pasta="qualitativa", coluna="q22_sugestoes", semente=0):
    """Passo 1 da análise de conteúdo das sugestões. Grava em `pasta` (fora do git):

    - chave.csv: id_curto ↔ id_resposta. É o ÚNICO arquivo com id_resposta. Estável entre
      execuções: quem já tem id_curto o mantém; respostas novas recebem os números seguintes,
      em ordem aleatória (semente fixa), para o número não revelar a ordem de envio.
    - textos_q21.csv: id_curto, texto (nomes próprios trocados por [professor]/[pessoa]).
    - q21_excluidas.csv: id_curto (se houver), texto, motivo — para os autores conferirem.
    - q21_exclusao_manual.csv: id_curto, motivo — preenchido pelos autores para excluir
      respostas sem relação com o curso (a regra automática só pega 'não', 'sim' etc.).
    - codificacao_A.csv, codificacao_B.csv (id_curto, trecho, categoria, observacao) e
      livro_de_codigos.csv: criados em branco, nunca sobrescritos.
    Devolve um dicionário só com contagens (nenhum texto, nenhum id)."""
    import os
    os.makedirs(pasta, exist_ok=True)
    s = base[["id_resposta", coluna]].copy()
    s["id_resposta"] = s["id_resposta"].astype(str)
    s["texto"] = s[coluna].fillna("").astype(str).str.strip()
    vazia = s["texto"] == ""
    nao_sug = ~vazia & s["texto"].map(nao_e_sugestao)
    cand = s[~vazia & ~nao_sug].copy()

    arq_chave = f"{pasta}/chave.csv"
    chave = (pd.read_csv(arq_chave, dtype=str) if os.path.exists(arq_chave)
             else pd.DataFrame(columns=["id_curto", "id_resposta"]))
    novos = [i for i in cand["id_resposta"] if i not in set(chave["id_resposta"])]
    if novos:
        novos = list(np.random.default_rng(semente + len(chave)).permutation(novos))
        ini = len(chave) + 1
        chave = pd.concat([chave, pd.DataFrame({"id_curto": [f"Q21-{ini + k:02d}" for k in range(len(novos))],
                                                "id_resposta": novos})], ignore_index=True)
        chave.to_csv(arq_chave, index=False, encoding="utf-8-sig")
    cand["id_curto"] = cand["id_resposta"].map(dict(zip(chave["id_resposta"], chave["id_curto"])))

    arq_man = f"{pasta}/q21_exclusao_manual.csv"
    _csv_em_branco(arq_man, ["id_curto", "motivo"])
    man = ler_planilha(arq_man).dropna(subset=["id_curto"])
    motivo_man = dict(zip(man["id_curto"].str.strip(), man["motivo"].fillna("exclusão manual")))

    cand["texto"], n_subst = anonimizar_textos(cand["texto"], nlp, nomes_extra)
    excl_man = cand["id_curto"].isin(motivo_man)
    incl = cand[~excl_man].sort_values("id_curto")
    incl[["id_curto", "texto"]].to_csv(f"{pasta}/textos_q21.csv", index=False, encoding="utf-8-sig")

    excl = pd.concat([
        s[nao_sug].assign(id_curto="", motivo="não é sugestão (resposta do tipo 'não'/'sim')")[["id_curto", "texto", "motivo"]],
        cand[excl_man].assign(motivo=cand.loc[excl_man, "id_curto"].map(motivo_man))[["id_curto", "texto", "motivo"]],
    ], ignore_index=True)
    excl.to_csv(f"{pasta}/q21_excluidas.csv", index=False, encoding="utf-8-sig")

    criados = [a for a, cols in [(f"{pasta}/codificacao_A.csv", COLUNAS_CODIFICACAO),
                                 (f"{pasta}/codificacao_B.csv", COLUNAS_CODIFICACAO),
                                 (f"{pasta}/livro_de_codigos.csv", COLUNAS_LIVRO)] if _csv_em_branco(a, cols)]
    return {"registros na base": len(s), "sugestões em branco": int(vazia.sum()),
            "excluídas: não é sugestão ('não'/'sim')": int(nao_sug.sum()),
            "excluídas: manual (sem relação com o curso etc.)": int(excl_man.sum()),
            "incluídas para codificação": len(incl), "nomes substituídos": n_subst,
            "_criados": criados}


def ler_planilha(arquivo):
    """CSV preenchido à mão (Excel, LibreOffice…): aceita vírgula ou ponto e vírgula e UTF-8 com ou sem BOM."""
    return pd.read_csv(arquivo, sep=None, engine="python", dtype=str, encoding="utf-8-sig")


def ler_codificacao(arquivo):
    """Planilha de codificação (id_curto, trecho, categoria, observacao) -> linhas com categoria
    preenchida, sem espaços nas pontas. Devolve DataFrame vazio se o arquivo não existir."""
    import os
    if not os.path.exists(arquivo):
        return pd.DataFrame(columns=COLUNAS_CODIFICACAO)
    t = ler_planilha(arquivo)
    for c in COLUNAS_CODIFICACAO:
        if c not in t:
            t[c] = np.nan
    t["id_curto"] = t["id_curto"].str.strip()
    t["categoria"] = t["categoria"].str.strip()
    return t[t["categoria"].notna() & (t["categoria"] != "") & t["id_curto"].notna()].copy()


def _presenca(cod, ids, cats):
    """Matriz resposta × categoria (True = o codificador pôs a resposta na categoria)."""
    m = pd.DataFrame(False, index=list(ids), columns=list(cats))
    for i, c in zip(cod["id_curto"], cod["categoria"]):
        if i in m.index:
            m.loc[i, c] = True
    return m


def _kappa(a, b):
    """Kappa de Cohen entre dois vetores 0/1. NaN se a concordância esperada for 1."""
    a, b = np.asarray(a, bool), np.asarray(b, bool)
    po = (a == b).mean()
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return np.nan if pe >= 1 else (po - pe) / (1 - pe)


def concordancia_codificadores(cod_a, cod_b, ids):
    """Concordância entre A e B por presença/ausência de cada categoria em cada resposta.

    Devolve (geral, por_categoria, divergencias):
    - geral: concordância percentual sobre todas as células resposta × categoria, a
      proporção de respostas com o mesmo conjunto de categorias nos dois, e o kappa.
    - por_categoria: n de respostas marcadas por A e por B, % de concordância, kappa.
    - divergencias: id_curto, categoria, A (0/1), B (0/1) — só onde discordam."""
    cats = sorted(set(cod_a["categoria"]) | set(cod_b["categoria"]))
    A, B = _presenca(cod_a, ids, cats), _presenca(cod_b, ids, cats)
    igual = A == B
    por_cat = pd.DataFrame({"n_respostas_A": A.sum(), "n_respostas_B": B.sum(),
                            "concordância_%": 100 * igual.mean(),
                            "kappa": [_kappa(A[c], B[c]) for c in cats]})
    geral = {"respostas": len(ids), "categorias": len(cats),
             "concordância_%": 100 * igual.values.mean(),
             "respostas com as mesmas categorias (%)": 100 * igual.all(axis=1).mean(),
             "kappa": _kappa(A.values.ravel(), B.values.ravel())}
    div = [(i, c, int(A.loc[i, c]), int(B.loc[i, c])) for i in A.index for c in cats if A.loc[i, c] != B.loc[i, c]]
    return geral, por_cat, pd.DataFrame(div, columns=["id_curto", "categoria", "A", "B"])


def categorias_consenso(consenso, ids, livro, suprimir=True, n_min=5):
    """Nº de respostas distintas por categoria (uma resposta conta uma vez por categoria),
    da mais para a menos frequente, com a definição do livro de códigos. Com suprimir=True,
    contagens entre 1 e n_min − 1 viram '<n_min'."""
    c = consenso[consenso["id_curto"].isin(set(ids))]
    n = c.groupby("categoria")["id_curto"].nunique().sort_values(ascending=False)
    defin = dict(zip(livro["categoria"].astype(str).str.strip(), livro["definicao"])) if len(livro) else {}
    t = pd.DataFrame({"categoria": n.index, "definicao": [defin.get(k, "") for k in n.index], "n_respostas": n.values})
    if suprimir:
        t["n_respostas"] = [f"<{n_min}" if 0 < v < n_min else int(v) for v in t["n_respostas"]]
    return t


def trechos_candidatos(consenso, max_por_categoria=2, max_palavras=30):
    """Até `max_por_categoria` trechos por categoria, com no máximo `max_palavras` palavras
    (os mais curtos primeiro; trecho maior é cortado e marcado). Só para os autores escolherem
    e revisarem à mão: o arquivo fica em qualitativa/, fora do git."""
    regs = []
    c = consenso[consenso["trecho"].notna() & (consenso["trecho"].str.strip() != "")].copy()
    c["n_palavras"] = c["trecho"].str.split().str.len()
    for cat, sub in c.sort_values("n_palavras").groupby("categoria", sort=False):
        for r in sub.drop_duplicates("id_curto").head(max_por_categoria).itertuples():
            pal = r.trecho.split()
            regs.append({"categoria": cat, "id_curto": r.id_curto,
                         "trecho": " ".join(pal[:max_palavras]) + (" […]" if len(pal) > max_palavras else ""),
                         "n_palavras": len(pal), "cortado": len(pal) > max_palavras})
    return pd.DataFrame(regs, columns=["categoria", "id_curto", "trecho", "n_palavras", "cortado"])


# ===========================================================================
# Seção 11 · família de 29 associações
# ===========================================================================
FAMILIA_29 = (
    [{"id": f"A{i}", "bloco": "A", "x": x, "y": y} for i, (x, y) in enumerate([
        ("AULAS", "ABSORCAO"), ("CONTEUDO_NOVO", "ABSORCAO"), ("MONITORIAS", "ABSORCAO"), ("PREREQ", "CONTEUDO_NOVO"),
        ("PREREQ", "APOIO"), ("TRANSICAO", "APOIO"), ("IA", "ABSORCAO"), ("IA", "APOIO")], 1)]
    + [{"id": f"B{i}", "bloco": "B", "x": "PERMANENCIA", "y": y} for i, y in enumerate([
        "EXPECTATIVA", "ABSORCAO", "AULAS", "MONITORIAS", "CONTEUDO_NOVO", "PREREQ", "TRANSICAO", "APOIO", "IA"], 1)]
    + [{"id": f"C{2 * i + j + 1}", "bloco": "C", "x": m, "y": y}
       for i, m in enumerate(["LEITURA", "GRUPOS", "CRONOGRAMA", "PERGUNTAR_IA"])
       for j, y in enumerate(["ABSORCAO", "MONITORIAS"])]
    + [{"id": f"D{i}", "bloco": "D", "x": "INGRESSO", "y": y}
       for i, y in enumerate(["PREREQ", "TRANSICAO", "CONTEUDO_NOVO", "ABSORCAO"], 1)]
)
assert len(FAMILIA_29) == 29
BLOCOS_R = {"A": "A · Percepção das aulas e da aprendizagem", "B": "B · Intenção de concluir o curso (pretende concluir = 1)",
            "C": "C · Métodos de estudo (marcou = 1)", "D": "D · Forma de ingresso (ENEM = 1, Medalhas = 0)"}
