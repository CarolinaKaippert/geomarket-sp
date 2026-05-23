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

# =========================
# CARREGAR DADOS
# =========================

dados = gpd.read_file(
    "data/processed/geomarket_final.geojson"
)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("Filtros")

regiao = st.sidebar.multiselect(
    "Selecione a região",
    options=dados["nm_regiao_05"].unique(),
    default=dados["nm_regiao_05"].unique()
)

cluster = st.sidebar.multiselect(
    "Selecione o cluster",
    options=dados["tipo_cluster"].unique(),
    default=dados["tipo_cluster"].unique()
)

# aplicar filtros
dados_filtrados = dados[
    (dados["nm_regiao_05"].isin(regiao))
    &
    (dados["tipo_cluster"].isin(cluster))
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
        dados_filtrados["atratividade"].mean(),
        1
    )
)

col3.metric(
    "Renda Média",
    round(
        dados_filtrados["renda"].mean(),
        2
    )
)

# =========================
# TOP 10
# =========================

st.subheader("🏆 Top 10 Distritos")

top10 = dados_filtrados.sort_values(
    "atratividade",
    ascending=False
)[
    [
        "ranking",
        "nm_distrito_municipal",
        "atratividade",
        "tipo_cluster"
    ]
].head(10)

st.dataframe(
    top10,
    use_container_width=True
)

# =========================
# GRÁFICO
# =========================

st.subheader("📊 Atratividade por Distrito")

fig_atratividade = px.bar(
    top10,
    x="nm_distrito_municipal",
    y="atratividade",
    color="tipo_cluster"
)

st.plotly_chart(
    fig_atratividade,
    use_container_width=True
)

st.subheader("📈 Renda vs Fluxo")

fig2 = px.scatter(
    dados_filtrados,
    x="renda",
    y="fluxo",
    size="atratividade",
    color="tipo_cluster",
    hover_name="nm_distrito_municipal"
)



st.plotly_chart(fig2)

# ==========================================
# COMPARAÇÃO DE DISTRITOS
# ==========================================

st.subheader("⚖️ Comparador de Distritos")

st.sidebar.title("Comparação de Distritos")
# Seleção dos distritos
distrito_a = st.sidebar.selectbox(
    "Distrito A",
    options=dados_filtrados["nm_distrito_municipal"].unique()
)

distrito_b = st.sidebar.selectbox(
    "Distrito B",
    options=dados_filtrados["nm_distrito_municipal"].unique()
)

# Filtrar os dois distritos
df_comparacao = dados_filtrados[
    dados_filtrados["nm_distrito_municipal"].isin([distrito_a, distrito_b])
].copy()


# =========================
# PREPARAR DADOS PARA GRÁFICO
# =========================

df_long = df_comparacao.melt(
    id_vars="nm_distrito_municipal",
    value_vars=["renda", "fluxo", "atratividade"],
    var_name="indicador",
    value_name="valor"
)

# =========================
# GRÁFICO
# =========================

fig_comparacao = px.bar(
    df_long,
    x="indicador",
    y="valor",
    color="nm_distrito_municipal",
    barmode="group"
)

st.plotly_chart(fig_comparacao, use_container_width=True)

# ==========================================
# CLUSTERS
# ==========================================

st.subheader("🧠 Distribuição dos Clusters")

fig_cluster = px.pie(
    dados_filtrados,
    names="tipo_cluster"
)

st.plotly_chart(
    fig_cluster,
    use_container_width=True
)

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