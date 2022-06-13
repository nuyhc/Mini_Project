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
    
## Title
st.title("질병 사망자 및 보건 환경 비교 분석")
st.markdown("---")
## Header
st.header("MID Project 2팀")
st.text("팀원: 김재석, 김채현, 김태훈, 박이슬, 손유선")
st.markdown("---")

st.markdown("## 사용 라이브러리")
with st.echo():
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
    

## Data Load
df_death_rate = pd.read_csv("data/pre_df/df_death_rate.csv")
df_Nmw = pd.read_csv("data/pre_df/df_Nmw.csv")
df_service = pd.read_csv("data/pre_df/df_service.csv")
df_service_common = pd.read_csv("data/pre_df/df_service_common.csv")
df_medicion = pd.read_csv("data/pre_df/df_medicion.csv")
df_welfare = pd.read_csv("data/pre_df/df_welfare.csv")
## json
g_p = open("data/countries.geo.edited.json", encoding="utf-8")
gp = open("data/countries.json", encoding="utf-8")
geo_poly = json.load(g_p)
geo_point = pd.json_normalize(json.load(gp))
g_p.close()
gp.close()

## 데이터 분석 범위 설정
st.markdown("## 데이터 분석 범위 설정")
st.markdown("사망률 및 보건 인프라 분석에 사용할 9개 데이터 셋을 선정하며,\n"
            "두 가지 문제점을 발견\n"
            "- 데이터 셋마다 수록 기간이 상이함\n"
            "- Raw Data 출처에 따라, 데이터가 제공하는 나라가 다름\n"
            "   - 일부는 OECD 국가를 대상으로 함\n"
            "   - WHO 데이터를 집계한 경우, 훨씬 광범위한 나라를 다루고 있음\n")
st.markdown("본 프로젝트는 \"질병에 따른 사망률\"과\"다양한 보건 인프라\"간의 관계를\n"
            "분석해보기 위함으로, 공통으로 제공하는 기간과 국가를 대상으로 분석 범위를 설정\n")

with st.echo():
    # 교집합 이용
    # country_intersecion = set(df_1) & set(df_2) & set(df_3) & set(df_4) ..
    # 최종 리스트 선정
    country_intersection = ['룩셈부르크',  '네덜란드',  '영국',  '이탈리아',  
        '캐나다',  '오스트레일리아',  '한국',  '일본',  '스페인',  '헝가리',  '독일',  
        '에스토니아',  '그리스',  '슬로바키아',  '핀란드',  '벨기에',  '체코',  
        '슬로베니아',  '프랑스',  '스웨덴',  '노르웨이',  '뉴질랜드',  '라트비아',  
        '덴마크',  '오스트리아',  '포르투갈',  '아일랜드',  '아이슬란드']