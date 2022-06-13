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
df_death_rate = pd.read_csv("data/pre_df/df_death_rate.csv")
## json
g_p = open("data/countries.geo.edited.json", encoding="utf-8")
gp = open("data/countries.json", encoding="utf-8")
geo_poly = json.load(g_p)
geo_point = pd.json_normalize(json.load(gp))
g_p.close()
gp.close()

## part 1
st.markdown("## 1. 주요 사망 원인별 사망률")
st.markdown("### Data set")
st.dataframe(df_death_rate) # st.table도 사용 가능 -> 일부만 표시시
## 연도별 평균 사망률
st.markdown("#### 연도별 평균 사망률")
with st.echo():
    fig = plt.figure(figsize=(14, 6))
    sns.pointplot(data=df_death_rate, x="연도", y="사망률", hue="국가", estimator=np.mean, ci=None).set_title("연도별 사망률 (연간 평균 사망률)")
    st.pyplot(fig)
## 질병에 따른 사망률
st.markdown("#### 질병에 따른 사망률")
with st.echo():
    fig = plt.figure(figsize=(14, 6))
    sns.pointplot(data=df_death_rate, x="연도", y="사망률", hue="질병명", estimator=np.sum, ci=None).set_title("질병에 따른 사망률")
    st.pyplot(fig)
## 국가별 질병 사망 비율
st.markdown("#### 국가별 질병 사망 비율")
with st.echo():
    st.plotly_chart(px.bar(data_frame=df_death_rate, x="연도", y="사망률", color="질병명", facet_col="국가", facet_col_wrap=5, title="국가별 질병 사망 비율", width=1600, height=800))
## 지역 시각화
st.markdown("#### 종합 지역 시각화")

icon_color = ["red", "blue", "green", "purple", "orange", "lightred", "beige", "darkblue", "darkgreen", "cadetblue", "darkpurple", "white", "pink", "lightblue", "lightgreen", "gray", "black", "lightgray"]
innter_choropleth = geo_poly
    
m = folium.Map(zoom_star=2, tiles="CartoDB dark_matter", dexet_retina=True)

folium.Choropleth(
    geo_data=innter_choropleth,
    name="choropleth",
    key_on="feature.properties.name",
    fill_color="yellow",
    fill_opacity=0.15,
    line_opacity=0.7,
).add_to(m)

mark_cluster = MarkerCluster().add_to(m)

for _ in df_death_rate.index:
    row = df_death_rate.loc[_]  
    folium.Marker([row["위도"], row["경도"]], icon=folium.Icon(icon="glyphicon glyphicon-certificate", color={k : v for k, v in zip(df_death_rate["질병명"].unique(), icon_color)}[row["질병명"]])).add_to(mark_cluster)       
    folium.Circle(
        radius = row["사망률"],
        location = [row["위도"], row["경도"]],
        tooltip = str(row["연도"]) + "년도 " + row["국가"] + " " + row["질병명"] + "로 인한 사망률 " + str(row["사망률"]),
        color = {k : v for k, v in zip(df_death_rate["질병명"].unique(), icon_color)}[row["질병명"]],
        fill = False        
    ).add_to(m)
folium.LayerControl().add_to(m)     
st_folium(m, width=800)
