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
df_service_common = pd.read_csv("data/pre_df/df_service_common.csv")

df_welfare = pd.read_csv("data/pre_df/df_welfare.csv")
## json
g_p = open("data/countries.geo.edited.json", encoding="utf-8")
gp = open("data/countries.json", encoding="utf-8")
geo_poly = json.load(g_p)
geo_point = pd.json_normalize(json.load(gp))
g_p.close()
gp.close()

## part 5
st.markdown("## 5. 공공사회 복지 지출")
st.markdown("### Data set")
st.markdown("#### 보건 서비스 지출")
st.dataframe(df_service)
## 복지 서비스 지출 증감
st.markdown("#### 복지 서비스 지출 분석")
with st.echo():
    px_cont = df_service_common.groupby(by = ['연도','대륙'], as_index = False )['서비스비용(백만$)'].sum()
    st.plotly_chart(px.bar(data_frame = px_cont, x= '연도', y = '서비스비용(백만$)',  color = '대륙', title = '국가 별 사회복지서비스 비용(백만$)'))
    
with st.echo():
    st.plotly_chart(px.line(data_frame = df_welfare, x = '연도', y = '복지비용(10억$)', color = '국가', title = '연도 별 공공사회복지비용 - 국가별'))

st.markdown("#### 공공사회 복지 지출")
st.dataframe(df_welfare)
## 공공 사회 복지 지출
st.markdown("#### 공공사회 복지 지출")
with st.echo():
    fig = plt.figure(figsize=(14, 6))
    sns.lineplot(data = df_welfare, x = '연도', y = '복지비용(10억$)', estimator = np.sum, ci = None)
    st.pyplot(fig)
