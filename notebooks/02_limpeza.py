import geopandas as gpd
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =========================
# CARREGAR DADOS
# =========================

mapa = gpd.read_file(
    "data/raw/distritos_sp.geojson"
)

dados = pd.read_csv(
    "data/raw/indicadores_sp.csv",
    sep=";",
    encoding="latin1"
)

# =========================
# MERGE DOS DADOS
# =========================

merged = mapa.merge(
    dados,
    on="nm_distrito_municipal"
)

# =========================
# DENSIDADE DEMOGRÁFICA
# =========================

merged["densidade"] = (
    merged["populacao"]
    / merged["qt_area_quilometro"]
)

# =========================
# NORMALIZAÇÃO DAS VARIÁVEIS
# =========================

merged["densidade_norm"] = (
    (merged["densidade"] - merged["densidade"].min())
    / (
        merged["densidade"].max()
        - merged["densidade"].min()
    )
)

merged["renda_norm"] = (
    (merged["renda"] - merged["renda"].min())
    / (
        merged["renda"].max()
        - merged["renda"].min()
    )
)

merged["fluxo_norm"] = (
    (merged["fluxo"] - merged["fluxo"].min())
    / (
        merged["fluxo"].max()
        - merged["fluxo"].min()
    )
)

merged["concorrencia_norm"] = (
    (merged["concorrencia"] - merged["concorrencia"].min())
    / (
        merged["concorrencia"].max()
        - merged["concorrencia"].min()
    )
)

# =========================
# ÍNDICE DE ATRATIVIDADE
# =========================

merged["atratividade_raw"] = (
    merged["densidade_norm"] * 0.30
    + merged["renda_norm"] * 0.25
    + merged["fluxo_norm"] * 0.35
    - merged["concorrencia_norm"] * 0.20
)

# =========================
# ESCALA 1-100
# =========================

minimo = merged["atratividade_raw"].min()
maximo = merged["atratividade_raw"].max()

merged["atratividade"] = (
    (
        (merged["atratividade_raw"] - minimo)
        / (maximo - minimo)
    ) * 99 + 1
).round(0)

# =========================
# RANKING
# =========================

merged["ranking"] = merged[
    "atratividade"
].rank(
    ascending=False,
    method="dense"
).astype(int)

# =========================
# TOP 10 DISTRITOS
# =========================

top10 = merged.sort_values(
    "atratividade",
    ascending=False
)[
    [
        "ranking",
        "nm_distrito_municipal",
        "atratividade",
        "densidade",
        "renda",
        "fluxo",
        "concorrencia"
    ]
].head(10)

top10.to_csv(
    "data/processed/top10_distritos.csv",
    index=False
)

# =========================
# ANÁLISE POR REGIÃO
# =========================

analise_regiao = merged.groupby(
    "nm_regiao_05"
)[
    [
        "atratividade",
        "densidade",
        "renda",
        "fluxo",
        "concorrencia"
    ]
].mean().round(2)

analise_regiao.to_csv(
    "data/processed/analise_regiao.csv"
)

# =========================
# CLUSTERIZAÇÃO KMEANS
# =========================

variaveis_cluster = merged[
    [
        "densidade",
        "renda",
        "fluxo",
        "concorrencia",
        "atratividade"
    ]
]

# padronizar dados
scaler = StandardScaler()

dados_padronizados = scaler.fit_transform(
    variaveis_cluster
)

# criar modelo
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

# gerar clusters
merged["cluster"] = kmeans.fit_predict(
    dados_padronizados
)

# converter para 1-4
merged["cluster"] = merged["cluster"] + 1

# =========================
# NOMES DOS CLUSTERS
# =========================

nomes_clusters = {
    1: "Centro Comercial Consolidado",
    2: "Zona Residencial Densa",
    3: "Área de Expansão Promissora",
    4: "Baixa Atratividade Comercial"
}

merged["tipo_cluster"] = merged["cluster"].map(
    nomes_clusters
)

# analisar médias dos clusters
analise_clusters = merged.groupby("cluster")[
    [
        "densidade",
        "renda",
        "fluxo",
        "concorrencia",
        "atratividade"
    ]
].mean().round(2)

# =========================
# EXPORTAR GEOJSON FINAL
# =========================

merged.to_file(
    "data/processed/geomarket_final.geojson",
    driver="GeoJSON"
)

# =========================
# STATUS
# =========================

print("Dados processados com sucesso!")
print(f"{len(merged)} distritos processados.")
