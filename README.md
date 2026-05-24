# ☕ GeoMarket-SP

Sistema de análise espacial e inteligência comercial para identificação dos melhores distritos da cidade de São Paulo para expansão de cafeterias.

---

# 📌 Sobre o Projeto

O **GeoMarket-SP** é um projeto de geomarketing desenvolvido para transformar dados urbanos em insights estratégicos de expansão comercial. Utilizando técnicas de geoprocessamento, ciência de dados e machine learning, o sistema analisa diferentes indicadores socioeconômicos e espaciais para identificar regiões com maior potencial para instalação de novos negócios.

O projeto foi desenvolvido com foco em cafeterias, mas sua estrutura pode ser facilmente adaptada para outros segmentos comerciais, como restaurantes, farmácias, academias, mercados e franquias.

A aplicação combina análise multicritério, clusterização espacial e visualização geográfica interativa para auxiliar processos de tomada de decisão de maneira visual e inteligente.

---

# 🎯 Objetivos

O projeto busca:

* Identificar distritos com maior potencial comercial;
* Analisar padrões urbanos e socioeconômicos;
* Aplicar técnicas de clusterização espacial;
* Criar um sistema de recomendação de modelos de cafeterias;
* Desenvolver um dashboard interativo para exploração dos dados;
* Demonstrar aplicações reais de geomarketing utilizando Python.

---

# 🧠 Tecnologias Utilizadas

* Python
* Pandas
* GeoPandas
* Folium
* Streamlit
* Plotly
* Scikit-Learn
* K-Means Clustering

---

# 📊 Indicadores Utilizados

O sistema utiliza diferentes variáveis urbanas para cálculo da atratividade comercial:

* Densidade populacional
* Renda média
* Fluxo de pessoas
* Concorrência comercial
* Área territorial dos distritos

Esses indicadores passam por processos de normalização e ponderação para geração do índice final de atratividade.

---

# ⚙️ Funcionalidades

## 📍 Índice de Atratividade

O sistema calcula um índice próprio de atratividade comercial para cada distrito da cidade de São Paulo, permitindo identificar regiões mais estratégicas para expansão.

---

## 🧩 Clusterização com K-Means

Os distritos são agrupados automaticamente em diferentes perfis urbanos utilizando o algoritmo K-Means.

Os clusters representam padrões espaciais e comerciais como:

* Centros comerciais consolidados
* Áreas residenciais densas
* Zonas promissoras de expansão
* Regiões de baixa atratividade comercial

---

## 🗺️ Dashboard Interativo

O dashboard permite:

* Visualização espacial dos distritos;
* Exploração de mapas interativos;
* Comparação entre regiões;
* Filtros dinâmicos;
* Ranking dos distritos;
* Análise visual dos clusters;
* Visualização das recomendações comerciais.

---

# 🗂️ Estrutura do Projeto

```bash
geomarket-sp/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── maps/
│   └── mapa_interativo.html
│
├── notebooks/
│   ├── 01_coleta.py
│   ├── 02_limpeza.py
│   └── 03_analise_espacial.py
│
└── README.md
```

---

# 🚀 Como Executar

## 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/geomarket-sp.git
```

---

## 2. Acesse a pasta

```bash
cd geomarket-sp
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Execute os scripts de processamento

```bash
python notebooks/02_limpeza.py
python notebooks/03_analise_espacial.py
```

---

## 5. Inicie o dashboard

```bash
streamlit run app/dashboard.py
```

---

# 📈 Possíveis Expansões Futuras

* Integração com APIs reais de mobilidade urbana;
* Dados em tempo real;
* Modelos preditivos;
* Análise temporal;
* Sistema de previsão de faturamento;
* Deploy em nuvem;
* Banco de dados geoespacial;
* Integração com Power BI.

---

# 📬 Contato

O GeoMarket-SP foi desenvolvido como uma aplicação prática de análise espacial e inteligência comercial utilizando Python e técnicas de ciência de dados.

Caso queira trocar ideias sobre geoprocessamento, geomarketing ou desenvolvimento do projeto:

* 📧 Email: ckaippertn@gmail.com
* 💼 LinkedIn: www.linkedin.com/in/carolina-kaippert-309257184
