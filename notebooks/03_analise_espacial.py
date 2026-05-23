import geopandas as gpd
import folium
import branca.colormap as cm
from folium.plugins import ( Search, MiniMap ) 

# =========================
# CARREGAR DADOS
# =========================

merged = gpd.read_file(
    "data/processed/geomarket_final.geojson"
)

# remover colunas de data
for col in merged.columns:
    if "dt_" in col:
        merged = merged.drop(columns=[col])

# =========================
# AGRUPAR REGIÕES
# =========================

regioes = merged.dissolve(
    by="nm_regiao_05",
    aggfunc={
        "atratividade": "mean",
        "densidade": "mean",
        "renda": "mean",
        "fluxo": "mean",
        "concorrencia": "mean"
    }
).reset_index()

# =========================
# NORMALIZAR REGIÕES
# =========================

min_reg = regioes["atratividade"].min()
max_reg = regioes["atratividade"].max()

regioes["atratividade_regiao"] = (
    (
        (regioes["atratividade"] - min_reg)
        / (max_reg - min_reg)
    ) * 99 + 1
).round(0)

# =========================
# MAPA BASE
# =========================

m = folium.Map(
    location=[-23.55, -46.63],
    zoom_start=10,
    tiles=None
)

folium.TileLayer(
    tiles="CartoDB positron",
    name="Mapa",
    control=False
).add_to(m)

# =========================
# DISTRITOS
# =========================

# escala de cores distritos
colormap_distritos = cm.LinearColormap(
    colors=["green", "yellow", "red"],
    vmin=merged["atratividade"].min(),
    vmax=merged["atratividade"].max(),
    caption="Atratividade dos Distritos"
)

grupo_distritos = folium.FeatureGroup(
    name="Distritos",
    show=True,
)

folium.GeoJson(
    merged,
    style_function=lambda feature: {
        "fillColor": colormap_distritos(
            feature["properties"]["atratividade"]
        ),
        "color": "black",
        "weight": 0.5,
        "fillOpacity": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=[
            "ranking",
            "nm_distrito_municipal",
            "atratividade",
            "densidade",
            "renda",
            "fluxo",
            "concorrencia"
        ],
        aliases=[
            "Ranking:",
            "Distrito:",
            "Atratividade:",
            "Densidade:",
            "Renda:",
            "Fluxo:",
            "Concorrência:"
        ],
        localize=True
    )
).add_to(grupo_distritos)

MiniMap().add_to(m)

Search(
    layer=grupo_distritos,
    geom_type="Polygon",
    placeholder="Buscar distrito...",
    search_label="nm_distrito_municipal"
).add_to(m)

grupo_distritos.add_to(m)

colormap_distritos.add_to(m)

# =========================
# REGIÕES
# =========================

colormap_regioes = cm.LinearColormap(
    colors=["blue", "purple"],
    vmin=regioes["atratividade_regiao"].min(),
    vmax=regioes["atratividade_regiao"].max(),
    caption="Atratividade das Regiões"
)

grupo_regioes = folium.FeatureGroup(
    name="Regiões",
    show=False,

)

folium.GeoJson(
    regioes,
    style_function=lambda feature: {
        "fillColor": colormap_regioes(
            feature["properties"]["atratividade_regiao"]
        ),
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.5,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=[
            "nm_regiao_05",
            "atratividade_regiao",
            "densidade",
            "renda",
            "fluxo",
            "concorrencia"
        ],
        aliases=[
            "Região:",
            "Índice de Atratividade:",
            "Densidade Média:",
            "Renda Média:",
            "Fluxo Médio:",
            "Concorrência Média:"
        ],
        localize=True
    )
).add_to(grupo_regioes)

grupo_regioes.add_to(m)

colormap_regioes.add_to(m)

# =========================
# CLUSTERS
# =========================

cores_cluster = {
    1: "red",
    2: "blue",
    3: "green",
    4: "purple"
}

grupo_clusters = folium.FeatureGroup(
    name="Clusters",
    show=False
)

folium.GeoJson(
    merged,
    style_function=lambda feature: {
        "fillColor": cores_cluster[
            feature["properties"]["cluster"]
        ],
        "color": "black",
        "weight": 0.5,
        "fillOpacity": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=[
            "nm_distrito_municipal",
            "tipo_cluster",
            "atratividade",
            "renda",
            "fluxo"
        ],
        aliases=[
            "Distrito:",
            "Perfil Comercial:",
            "Atratividade:",
            "Renda:",
            "Fluxo:"
        ]
    )
).add_to(grupo_clusters)

grupo_clusters.add_to(m)

# =========================
# CONTROLE
# =========================

folium.LayerControl().add_to(m)

legenda_clusters = """
<div style="
position: fixed;
bottom: 50px;
left: 50px;
width: 260px;
height: 140px;
background-color: white;
border:2px solid grey;
z-index:9999;
font-size:14px;
padding: 10px;
">

<b>Clusters Comerciais</b><br>

<i style="background:red;
width:10px;
height:10px;
float:left;
margin-right:8px;"></i>
Centro Comercial Consolidado<br>

<i style="background:blue;
width:10px;
height:10px;
float:left;
margin-right:8px;"></i>
Zona Residencial Densa<br>

<i style="background:green;
width:10px;
height:10px;
float:left;
margin-right:8px;"></i>
Área de Expansão Promissora<br>

<i style="background:purple;
width:10px;
height:10px;
float:left;
margin-right:8px;"></i>
Baixa Atratividade Comercial

</div>
"""

m.get_root().html.add_child(
    folium.Element(legenda_clusters)
)


# =========================
# SALVAR
# =========================

m.save("maps/mapa_interativo.html")

print("Mapa interativo gerado com sucesso!")