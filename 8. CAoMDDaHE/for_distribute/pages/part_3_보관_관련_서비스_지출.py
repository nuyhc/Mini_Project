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
df_service = pd.read_csv("data/pre_df/df_service.csv")

## json
g_p = open("data/countries.geo.edited.json", encoding="utf-8")
gp = open("data/countries.json", encoding="utf-8")
geo_poly = json.load(g_p)
geo_point = pd.json_normalize(json.load(gp))
g_p.close()
gp.close()

## part 3
st.markdown("## 3. 보건 관련 지출비")
st.markdown("### Data set")
st.dataframe(df_service)
## 세계 1인당 보건지출(US$) 연도별
st.markdown("#### 세계 1인당 보건 지출 (US$)")
with st.echo():
    df_service = df_service[df_service["항목"]=="1인당 보건지출(US$)"].reset_index(drop=True)
    w_pivot = pd.pivot_table(data=df_service,index='연도', columns='국가영문', values="데이터값")
    st.plotly_chart(px.line(w_pivot))
