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
from googletrans import Translator
import time

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
    from googletrans import Translator
    import time
    
## 한글폰트 설정
from IPython.display import set_matplotlib_formats

def get_font_family():
    import platform
    system_name = platform.system()

    if system_name == "Darwin" :
        font_family = "AppleGothic"
    elif system_name == "Windows":
        font_family = "Malgun Gothic"
    else:
        import matplotlib as mpl
        mpl.font_manager._rebuild()
        findfont = mpl.font_manager.fontManager.findfont
        mpl.font_manager.findfont = findfont
        mpl.backends.backend_agg.findfont = findfont
        
        font_family = "NanumBarunGothic"
    return font_family

get_font_family()

plt.style.use("ggplot")

font_family = get_font_family()
plt.rc("font", family=font_family)
plt.rc("axes", unicode_minus=False)

set_matplotlib_formats("retina")

## Data Load
df_death_rate = pd.read_csv("../data/pre_df/df_death_rate.csv")
df_Nmw = pd.read_csv("../data/pre_df/df_Nmw.csv")
df_service = pd.read_csv("../data/pre_df/df_service.csv")
df_service_common = pd.read_csv("../data/pre_df/df_service_common.csv")
df_medicion = pd.read_csv("../data/pre_df/df_medicion.csv")
df_welfare = pd.read_csv("../data/pre_df/df_welfare.csv")
## json
g_p = open("../data/countries.geo.edited.json", encoding="utf-8")
gp = open("../data/countries.json", encoding="utf-8")
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

## 국가 영문명 추가
st.markdown("## 영문 국가명 추가")
st.markdown("데이터를 전처리하는 과정에서 영문 국가명을 추가해줬습니다.\n"
            "Google Trans API를 이용했습니다\n")
with st.echo():
    translator = Translator()
    
    def kor2eng(list_of_country):
        temp = []
        for _ in list_of_country:
            temp.append(translator.translate(_).text.lower())
            time.sleep(0.5)
        return temp

    dict_kor2eng = {}
    list_kor2eng = kor2eng(df_Nmw["국가"].unique())

    for kor, eng in zip(df_Nmw["국가"].unique(), list_kor2eng):
        dict_kor2eng[kor] = eng


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
    
st_folium(m, width=1000)

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
    
st_folium(m, width=1000)  



## part 3
st.markdown("## 3. 보건 관련 지출비")
st.markdown("### Data set")
st.dataframe(df_service)

## part 4
st.markdown("## 4. 의약품 판매 / 소비")
st.markdown("### Data set")
st.dataframe(df_medicion)

## part 5
st.markdown("## 5. 공공사회 복지 지출")
st.markdown("### Data set")
st.markdown("#### 보건 서비스 지출")
st.dataframe(df_service)
st.markdown("#### 공공사회 복지 지출")
st.dataframe(df_welfare)


## part 6
st.markdown("## 6. 최종")
st.markdown("### Data set")
st.text("앞서 사용한 모든 데이터를 합쳐 하나의 데이터로 생성")
df_corr = pd.read_csv("../data/pre_df/df_corr.csv")
st.dataframe(df_corr)