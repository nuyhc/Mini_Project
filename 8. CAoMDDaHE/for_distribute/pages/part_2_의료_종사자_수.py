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
df_Nmw = pd.read_csv("data/pre_df/df_Nmw.csv")

## json
g_p = open("data/countries.geo.edited.json", encoding="utf-8")
gp = open("data/countries.json", encoding="utf-8")
geo_poly = json.load(g_p)
geo_point = pd.json_normalize(json.load(gp))
g_p.close()
gp.close()

## part2
st.markdown("## 2. 의료 종사자 수")
st.markdown("### Data set")
st.dataframe(df_Nmw)
## 연도별 의료 인력
st.markdown("#### 연도별 의료 인력 수")
with st.echo():
    fig = plt.figure(figsize=(14, 6))
    sns.pointplot(data=df_Nmw, x="연도", y="수", hue="직업", estimator=np.mean, ci=None).set_title("연도별 의료 인력 수")
    st.pyplot(fig)

with st.echo():
    st.plotly_chart(px.line(data_frame=df_Nmw, x="연도", y="수", facet_col="직업", color="국가", title="직업군별 추이"))

## 국가별 의료 인력
st.markdown("#### 국가별 의료 인력")
with st.echo():
    fig = plt.figure(figsize=(18, 12))
    sns.pointplot(data=df_Nmw, x="연도", y="수", hue="국가", ci=None).set_title("국가별 - 연도별 의료 인력 수 (상세)")
    st.pyplot(fig)
    
temp = []
group_yc = df_Nmw.groupby("연도", as_index=False)["국가"].value_counts()
for _ in range(len(group_yc["연도"].unique())):
    temp.append(set(group_yc[group_yc["연도"]==group_yc["연도"].unique()[_]]["국가"].values))
always = set(temp[0])
for _ in range(1, len(temp)):
    always = always & temp[_]

df_Nmw_always = df_Nmw[df_Nmw["국가"].isin(always)]
df_Nmw_always = df_Nmw_always.reset_index(drop=True).copy()

## 직업군별 추이
st.markdown("#### 직업군별 추이")
with st.echo():
    st.plotly_chart(px.line(data_frame=df_Nmw_always, x="연도", y="수", facet_col="직업", color="국가", title="직업군별 추이"))

## 지역 시각화
st.markdown("#### 종합 지역 시각화")
innter_choropleth = geo_poly
m = folium.Map(zoom_star=2, tiles="CartoDB dark_matter")

folium.Choropleth(
    geo_data=innter_choropleth,
    name="choropleth",
    key_on="feature.properties.name",
    fill_color="yellow",
    fill_opacity=0.15,
    line_opacity=0.7,
).add_to(m)

mark_cluster = MarkerCluster().add_to(m)

for _ in df_Nmw.index:
    row = df_Nmw.loc[_]    
    folium.Marker([row["위도"], row["경도"]], icon=folium.Icon(icon="glyphicon glyphicon-plus",color={"의사":"red", "간호사":"lightgray", "약사":"blue", "치과의사":"purple"}[row["직업"]])).add_to(mark_cluster)    
    folium.Circle(
        radius = row["수"],
        location = [row["위도"], row["경도"]],
        tooltip = str(row["연도"]) + "년도 " + row["국가"] + " " + {"의사":"의사", "간호사":"간호사", "약사":"약사", "치과의사":"치과의사"}[row["직업"]] + " : " + str(row["수"]),
        color = {"의사":"crimson", "간호사":"lightgray", "약사":"blue", "치과의사":"purple"}[row["직업"]],
        fill = False        
    ).add_to(m)
folium.LayerControl().add_to(m)
st_folium(m, width=800)  
