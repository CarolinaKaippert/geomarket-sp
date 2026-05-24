import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="GeoMarket-SP",
    layout="wide"
)

st.title("☕ GeoMarket-SP")

st.subheader(
    "Análise Espacial para Expansão Comercial em São Paulo"
)

st.write("""O **GeoMarket-SP** é um projeto de inteligência geográfica e análise espacial desenvolvido com o objetivo de identificar os distritos mais estratégicos da cidade de São Paulo para expansão de cafeterias. A proposta do sistema é transformar dados urbanos em informações úteis para tomada de decisão comercial, utilizando conceitos de geoprocessamento, ciência de dados e machine learning aplicados ao contexto de geomarketing.

O projeto integra diferentes indicadores socioeconômicos e espaciais, como densidade populacional, renda média, fluxo de pessoas, concorrência comercial e área territorial dos distritos. A partir desses dados, foi criado um índice próprio de atratividade comercial, capaz de medir o potencial de cada região para receber novos empreendimentos. Esse índice é calculado através de uma análise multicritério com variáveis normalizadas, permitindo comparar diferentes áreas da cidade de forma padronizada e estratégica.

Além da análise de atratividade, o sistema utiliza o algoritmo K-Means para identificar padrões urbanos e segmentar os distritos em diferentes perfis comerciais. Essa clusterização permite compreender melhor o comportamento espacial da cidade, destacando regiões consolidadas, áreas residenciais densas, zonas promissoras para expansão e locais com baixa atratividade comercial.

Os resultados são apresentados em um dashboard interativo desenvolvido com Streamlit e mapas dinâmicos em Folium, permitindo exploração visual dos dados, comparação entre distritos, filtros espaciais e visualização geográfica das recomendações comerciais. O projeto busca demonstrar como técnicas de análise espacial e ciência de dados podem ser aplicadas para apoiar decisões estratégicas de expansão urbana e comercial de forma inteligente e visual.
""")
st.space(30)

# =========================
# CARREGAR DADOS
# =========================

dados = gpd.read_file(
    "data/processed/geomarket_final.geojson"
)

# =========================
# RENOMEAR VARIÁVEIS
# =========================

dados = dados.rename(
    columns={
        "nm_distrito_municipal": "Distrito",
        "nm_regiao_05": "Região",
        "tipo_cluster": "Cluster",
        "renda": "Renda",
        "fluxo": "Fluxo",
        "densidade": "Densidade",
        "concorrencia": "Concorrência",
        "atratividade": "Atratividade",
        "ranking": "Ranking"
    }
)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("Filtros")

regiao = st.sidebar.multiselect(
    "Selecione a região",
    options=dados["Região"].unique(),
    default=dados["Região"].unique()
)

cluster = st.sidebar.multiselect(
    "Selecione o cluster",
    options=dados["Cluster"].unique(),
    default=dados["Cluster"].unique()
)

# =========================
# FILTROS
# =========================

dados_filtrados = dados[
    (dados["Região"].isin(regiao))
    &
    (dados["Cluster"].isin(cluster))
]

# =========================
# MÉTRICAS
# =========================

st.subheader("📌 Indicadores Gerais")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Distritos",
    len(dados_filtrados)
)

col2.metric(
    "Atratividade Média",
    round(
        dados_filtrados["Atratividade"].mean(),
        1
    )
)

col3.metric(
    "Renda Média",
    round(
        dados_filtrados["Renda"].mean(),
        2
    )
)

st.space(30)

# =========================
# TOP 10
# =========================

st.subheader("🏆 Top 10 Distritos")

top10 = dados_filtrados.sort_values(
    "Atratividade",
    ascending=False
)[
    [
        "Ranking",
        "Distrito",
        "Atratividade",
        "Cluster",
    ]
].head(10)

st.dataframe(
    top10,
    use_container_width=True
)

st.space(30)

# =========================
# GRÁFICO
# =========================

st.subheader("📊 Atratividade por Distrito")

fig_atratividade = px.bar(
    top10,
    x="Distrito",
    y="Atratividade",
    color="Cluster",
    text="Atratividade"
)

fig_atratividade.update_layout(
    xaxis_title="Distrito",
    yaxis_title="Índice de Atratividade",
    height=500
)

st.plotly_chart(
    fig_atratividade,
    use_container_width=True
)

st.space(30)

# =========================
# RENDA VS FLUXO
# =========================

st.subheader("📈 Renda vs Fluxo")

fig2 = px.scatter(
    dados_filtrados,
    x="Renda",
    y="Fluxo",
    size="Atratividade",
    color="Cluster",
    hover_name="Distrito",
    labels={
        "Renda": "Renda Média",
        "Fluxo": "Fluxo de Pessoas"
    }
)

fig2.update_layout(
    height=600
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.space(30)

# ==========================================
# COMPARAÇÃO DE DISTRITOS
# ==========================================

st.subheader("⚖️ Comparador de Distritos")

col_sel1, col_sel2 = st.columns(2)

with col_sel1:

    distrito_a = st.selectbox(
        "Distrito A",
        options=sorted(
            dados_filtrados["Distrito"].unique()
        )
    )

with col_sel2:

    distrito_b = st.selectbox(
        "Distrito B",
        options=sorted(
            dados_filtrados["Distrito"].unique()
        ),
        index=1
    )

# ==========================================
# FILTRAR DISTRITOS
# ==========================================

df_comparacao = dados_filtrados[
    dados_filtrados["Distrito"].isin(
        [distrito_a, distrito_b]
    )
].copy()

# ==========================================
# NORMALIZAÇÃO 0-100
# ==========================================

colunas_normalizar = [
    "Renda",
    "Fluxo",
    "Atratividade",
    "Densidade",
    "Concorrência"
]

for col in colunas_normalizar:

    min_val = dados_filtrados[col].min()
    max_val = dados_filtrados[col].max()

    if max_val != min_val:

        df_comparacao[f"{col}_norm"] = (
            (
                df_comparacao[col] - min_val
            ) / (
                max_val - min_val
            )
        ) * 100

    else:

        df_comparacao[f"{col}_norm"] = 0

st.space(30)

# ==========================================
# TABELA COMPARATIVA
# ==========================================

st.subheader("📋 Comparação dos Distritos")

st.dataframe(
    df_comparacao[
        [
            "Distrito",
            "Cluster",
            "Renda",
            "Fluxo",
            "Densidade",
            "Concorrência",
            "Atratividade"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ==========================================
# DADOS DO GRÁFICO
# ==========================================

df_long = df_comparacao.melt(
    id_vars=["Distrito"],
    value_vars=[
        "Renda_norm",
        "Fluxo_norm",
        "Densidade_norm",
        "Concorrência_norm",
        "Atratividade_norm"
    ],
    var_name="Indicador",
    value_name="Valor"
)

df_long["Indicador"] = (
    df_long["Indicador"]
    .str.replace("_norm", "")
)

# ==========================================
# GRÁFICO DE COMPARAÇÃO
# ==========================================

fig_comparacao = px.bar(
    df_long,
    x="Indicador",
    y="Valor",
    color="Distrito",
    barmode="group",
    text="Valor"
)

fig_comparacao.update_layout(
    xaxis_title="Indicadores",
    yaxis_title="Escala Normalizada (0-100)",
    height=550
)

fig_comparacao.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig_comparacao,
    use_container_width=True
)

st.space(30)

# ==========================================
# INSIGHTS AUTOMÁTICOS
# ==========================================

st.subheader("🧠 Insights Automáticos")

melhor = df_comparacao.sort_values(
    "Atratividade",
    ascending=False
).iloc[0]

pior = df_comparacao.sort_values(
    "Atratividade",
    ascending=True
).iloc[0]

st.success(
    f"""
    ✅ O distrito mais atrativo é
    {melhor['Distrito']}
    com índice {melhor['Atratividade']}.
    """
)

st.warning(
    f"""
    ⚠️ O distrito menos atrativo é
    {pior['Distrito']}
    com índice {pior['Atratividade']}.
    """
)

st.space(30)

# ==========================================
# CLUSTERS
# ==========================================

st.subheader("📍​ Distribuição dos Clusters")

fig_cluster = px.pie(
    dados_filtrados,
    names="Cluster"
)

st.plotly_chart(
    fig_cluster,
    use_container_width=True
)

st.space(30)

# =========================
# MAPA HTML
# =========================

st.subheader("🗺️ Mapa Interativo")

with open(
    "maps/mapa_interativo.html",
    "r",
    encoding="utf-8"
) as f:

    mapa_html = f.read()

st.components.v1.html(
    mapa_html,
    height=700
)