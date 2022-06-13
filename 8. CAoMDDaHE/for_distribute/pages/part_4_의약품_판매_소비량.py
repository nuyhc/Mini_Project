import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import cufflinks as cf
import chart_studio
import folium
from folium.plugins import MarkerCluster
import json
import streamlit as st
from streamlit_folium import st_folium
import time
import koreanize_matplotlib

st.set_page_config(layout='wide')

country_intersection = ['룩셈부르크',  '네덜란드',  '영국',  '이탈리아',  
        '캐나다',  '오스트레일리아',  '한국',  '일본',  '스페인',  '헝가리',  '독일',  
        '에스토니아',  '그리스',  '슬로바키아',  '핀란드',  '벨기에',  '체코',  
        '슬로베니아',  '프랑스',  '스웨덴',  '노르웨이',  '뉴질랜드',  '라트비아',  
        '덴마크',  '오스트리아',  '포르투갈',  '아일랜드',  '아이슬란드']

## Data Load

df_medicion = pd.read_csv("data/pre_df/df_medicion.csv")

## json
g_p = open("data/countries.geo.edited.json", encoding="utf-8")
gp = open("data/countries.json", encoding="utf-8")
geo_poly = json.load(g_p)
geo_point = pd.json_normalize(json.load(gp))
g_p.close()
gp.close()

## part 4
st.markdown("## 4. 의약품 판매 / 소비")
st.markdown("### Data set")
st.dataframe(df_medicion)
## 연간 의약품 판매액/소비량
st.markdown("#### 연간 의약품 판매액")
with st.echo():
    fig = plt.figure(figsize=(15, 4))
    sns.pointplot(data=df_medicion, x='연도', y='의약품판매량', ci=None, estimator=np.sum).set_ylabel("의약품 판매량 (100만 $)", fontsize=11)
    st.pyplot(fig)
st.markdown("#### 연간 의약품 소비량")
with st.echo():
    fig = plt.figure(figsize=(15,4))
    sns.pointplot(data=df_medicion, x='연도', y='의약품소비량', ci=None, estimator=np.sum)
    st.pyplot(fig)
## 의약품별 연간 의약품 소비량
st.markdown("#### 의약품별 연간 의약품 소비량")
with st.echo():
    fig = plt.figure(figsize=(15,10))
    sns.pointplot(data=df_medicion, x='연도', y='의약품소비량', hue='의약품', ci=None, estimator=np.sum)
    st.pyplot(fig)

df_sale = pd.read_csv("data/pre_df/df_sale.csv", encoding="cp949")
df_consume = pd.read_csv("data/pre_df/df_consume.csv", encoding="cp949")
df_consume = df_consume.rename(columns={'시점':'연도'})
df_consume = df_consume.rename(columns={'데이터':'의약품소비량'})
df_sale = df_sale.rename(columns={'시점' : '연도'})
df_sale = df_sale.rename(columns={'데이터' : '의약품판매량'})

## 연간 국가별 의약품 판매량 df_sale
st.markdown("#### 연간 국가별 의약품 판매량")
with st.echo():
    fig = plt.figure(figsize=(25,15))
    sns.pointplot(data=df_sale, x='연도', y='의약품판매량', hue='국가', ci=None)
    st.pyplot(fig)
## 연간 국가별 의약품 소비량 df_consume
with st.echo():
    fig = plt.figure(figsize=(25,15))
    sns.pointplot(data=df_medicion, x='연도', y='의약품소비량', hue='국가', ci=None)
    st.pyplot(fig)
