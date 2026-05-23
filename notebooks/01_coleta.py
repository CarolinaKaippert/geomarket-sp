import pandas as pd
import geopandas as gpd

print("Projeto GeoMarket SP iniciado")

mapa = gpd.read_file("data/raw/distritos_sp.geojson")

dados = pd.read_csv("data/raw/indicadores_sp.csv")

print(mapa.columns)
print(dados.head())