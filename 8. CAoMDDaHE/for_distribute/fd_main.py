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
st_folium(m, width=800)

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
st_folium(m, width=800)  



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

df_sale = pd.read_csv("../data/pre_df/df_sale.csv", encoding="cp949")
df_consume = pd.read_csv("../data/pre_df/df_consume.csv", encoding="cp949")
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



## part 6
st.markdown("## 6. 최종")
st.markdown("### Data set")
st.text("앞서 사용한 모든 데이터를 합쳐 하나의 데이터로 생성")
df_corr = pd.read_csv("../data/pre_df/df_corr.csv")
df_corr_pre = df_corr[["국가", "연도", "평균 사망률", "평균 의료 인력 수", "1인당 보건지출", "평균 소비량", "평균 판매량", "평균 치료비", "평균 복지 비용(G$)"]]
st.dataframe(df_corr_pre)
## 결측치 확인
st.markdown("#### 결측치 확인")
with st.echo():
    fig = plt.figure(figsize=(6, 4))
    sns.heatmap(data=df_corr_pre.isnull())
    st.pyplot(fig)

st.code(df_corr_pre.isnull().mean()*100)
st.write("9개의 데이터 셋을 공통 항목 (국가, 연도)로 가져오다보니 결측치가 있습니다.")
st.write("특정 항목에서 약 23.4% 정도의 결측치 입니다.")

## 사망률과 의료 인프라
st.markdown("#### 사망률과 의료 인프라")

temp = df_welfare[df_welfare["국가"].isin(country_intersection)][["대륙", "국가"]].drop_duplicates().reset_index(drop=True)
temp = pd.merge(left=temp, right=df_corr, on="국가", how="outer")
temp = temp[["국가", "대륙"]].drop_duplicates()

asia = temp[(temp["대륙"]=="아시아") | (temp["대륙"]=="오세아니아")]["국가"].to_list()
europe = temp[temp["대륙"]=="유럽"]["국가"].to_list()
america = temp[temp["대륙"]=="북아메리카"]["국가"].to_list()

asia.extend(["터키", "이스라엘"])
europe.extend(["라투아니아", "스위스", "폴란드"])
america.extend(["칠레", "멕시코", "미국"])

st.markdown("##### 아시아/오세아니아")
st.plotly_chart(px.bar(data_frame=df_corr[df_corr["국가"].isin(asia)], x="연도", y=["평균 사망률", "평균 의료 인력 수", "1인당 보건지출", "평균 소비량", "평균 판매량", "평균 치료비", "평균 복지 비용(G$)"],\
    facet_col="국가", barmode="overlay", title="데이터 종합 (아시아 / 오세아니아)"))

st.markdown("##### 아메리카")
st.plotly_chart(px.bar(data_frame=df_corr[df_corr["국가"].isin(america)], x="연도", y=["평균 사망률", "평균 의료 인력 수", "1인당 보건지출", "평균 소비량", "평균 판매량", "평균 치료비", "평균 복지 비용(G$)"],\
    facet_col="국가", barmode="overlay", title="데이터 종합 (북미 / 남미)"))

st.write("유럽은 국가가 많아 나눠 그렸습니다.")
st.markdown("##### 유럽")
st.plotly_chart(px.bar(data_frame=df_corr[df_corr["국가"].isin(europe[:10])], x="연도", y=["평균 사망률", "평균 의료 인력 수", "1인당 보건지출", "평균 소비량", "평균 판매량", "평균 치료비", "평균 복지 비용(G$)"],\
    facet_col="국가", facet_col_wrap=5, barmode="overlay", title="데이터 종합 (유럽)"))
st.plotly_chart(px.bar(data_frame=df_corr[df_corr["국가"].isin(europe[10:20])], x="연도", y=["평균 사망률", "평균 의료 인력 수", "1인당 보건지출", "평균 소비량", "평균 판매량", "평균 치료비", "평균 복지 비용(G$)"],\
    facet_col="국가", facet_col_wrap=5, barmode="overlay", title="데이터 종합 (유럽)"))
st.plotly_chart(px.bar(data_frame=df_corr[df_corr["국가"].isin(europe[20:])], x="연도", y=["평균 사망률", "평균 의료 인력 수", "1인당 보건지출", "평균 소비량", "평균 판매량", "평균 치료비", "평균 복지 비용(G$)"],\
    facet_col="국가", facet_col_wrap=3, barmode="overlay", title="데이터 종합 (유럽)"))

## 1인당 보건지출 - 복지비용 비율
st.markdown("#### 1인당 보건 지출 - 복지 비용 비율")
st.plotly_chart(px.area(data_frame=df_corr, x="연도", y="보건지출-복지비용 비율", color="국가", title="1인당 보건지출-복지비용 비율"))
## 1인당 보건지출 - 치료비 비율
st.markdown("#### 1인당 보건 지출 - 치료비 비율")
st.plotly_chart(px.area(data_frame=df_corr, x="연도", y="보건지출-치료비 비율", color="국가", title="1인당 보건지출-치료비 비율"))
## 보건 지출 대비 의약품 소비량
st.markdown("#### 1인당 보건 지출 - 의약품 소비량 비율")
st.plotly_chart(px.area(data_frame=df_corr, x="연도", y="보건지출-의약품 소비량 비율", color="국가", title="보건지출-의약품 소비량 비율"))
## 의약품 판매액 대비 의약품 소비량
st.markdown("#### 의약품 판매액 대비 의약품 소비량")
st.plotly_chart(px.area(data_frame=df_corr, x="연도", y="의약품 판매량-의약품 소비량 비율", color="국가", title="의약품 판매량-의약품 소비량 비율"))
## 의료 인력 수 대비 평균 치료비
st.markdown("#### 의료 인력 수 대비 평균 치료비")
st.plotly_chart(px.area(data_frame=df_corr, x="연도", y="의료 인력-평균 치료비 비율", color="국가", title="의료 인력-평균 치료비 비율"))

## 상관 계수 분석
st.markdown("### 상관 계수 분석")
st.markdown("#### 전체 국가")
with st.echo():
    df = df_corr[['국가', '연도', '평균 사망률', '평균 의료 인력 수', '1인당 보건지출', '평균 소비량', '평균 판매량', '평균 치료비', '평균 복지 비용(G$)']]
    corr = df.corr()
    fig = plt.figure(figsize=(8,6))
    sns.heatmap(data=corr, annot=True, cmap="coolwarm", mask=np.triu(np.ones_like(corr)))
    st.pyplot(fig)

st.write("주요 원인별 사망률과 의료 인프라 간의 상관계수는 음의 상관을 띄고 있습니다.")
st.write("즉, 의료 인프라와 관련된 변수의 값이 증가하면, 사망률은 감소한다는 사실을 확인할 수 있습니다.")

st.markdown("#### 한국 (2008 ~ 2019)")
st.markdown("##### 1. 의약품 소비량이 증가하면 해당 질병에 기인한 사망률이 감소하는 경향을 보임")
df_corr_kr = df_death_rate.loc[(df_death_rate['국가'] == '한국'), ['국가', '질병명', '연도', '성별', '사망률']].reset_index(drop = True)
# 한국표준질병사인분류 코드에 따라, 데이터 셋 질병명 대분류 정리
# medicine : 호흡계통 데이터 없음 - 그 외로 분류
dict_disease_cat = {'특정감염성 및 기생충성질환': '그 외',
                    ' 호흡기결핵': '그 외',
                    '악성신생물(암)': '그 외',
                    ' 위': '소화계통',
                    ' 간 및 간내 쓸개관': '소화계통',
                    ' 기관·기관지 및 폐': '순환계통',
                    ' 유방': '그 외',
                    '당뇨병': '내분비/대사질환',
                    '순환기계통의 질환': '순환계통',
                    ' 고혈압성질환': '순환계통',
                    ' 허혈성심질환': '순환계통',
                    ' 뇌혈관질환': '순환계통',
                    '호흡기계통의 질환': '그 외',
                    '소화기계통의 질환': '소화계통',
                    ' 간질환': '소화계통',
                    '사망의 외부요인': '그 외',
                    ' 운수사고': '그 외',
                    ' 고의적 자해(자살)': '정신 및 행동장애'}
# dict_disease_cat 기준 > 질병명 분류 컬럼 생성
for i in range(len(df_corr)):
    temp_name = df_corr_kr.iloc[i, 1]
    df_corr_kr.loc[i, '질병명_분류'] = dict_disease_cat[temp_name]
# 한국에 대해서 - 2008년 이후부터 분석 (데이터가 그 때부터 생성되었음)
# 연도 별 
df_kr_death_med = pd.DataFrame(df_corr_kr[df_corr_kr['연도']>=2008].groupby(by = ['연도', '질병명_분류'], as_index = False)['사망률'].mean()).sort_values('사망률',  ascending = False).reset_index(drop = True)
# 한국표준질병사인분류 코드에 따라, 데이터 셋 질병명 대분류 정리
# medicine : 호흡계통 데이터 없음 - 사망률 데이터에서도 '그 외'로 분류
dict_medicine_cat = {'소화관 및 신진대사': '소화계통',
                    '제산제': '소화계통',
                    '소화성궤양 및 위장용 약물': '소화계통',
                    '당뇨 약물': '내분비/대사질환',
                    '심장 배당체': '순환계통',
                    '항 부정맥제': '순환계통',
                    '이뇨제': '순환계통',
                    '향균제': '그 외',
                    '진통제': '그 외',
                    '수면제 및 진정제':'정신 및 행동장애' ,
                    '항우울제': '정신 및 행동장애'}
# dict_medicine_cat 기준 > 질병명 분류 컬럼 생성
for i in range(len(df_medicion)):
    temp_name = df_medicion.iloc[i, 2]
    df_medicion.loc[i, '질병명_분류'] = dict_medicine_cat[temp_name]
# 한국에 대해서 - 2008년 이후부터 분석 (데이터가 그 때부터 생성되었음)
# 연도 별 
df_temp = pd.DataFrame(df_medicion[df_medicion['국가']=='한국'].groupby(by = ['연도', '질병명_분류'], as_index = False)[['의약품소비량']].sum()).sort_values('의약품소비량',  ascending = False)
# merge 위한 key값 생성 후, null값 생성될 여지 없는지 여집합 이용해 확인
df_temp['key'] = df_temp['연도'].astype(str)+df_temp['질병명_분류']
df_kr_death_med['key'] = df_kr_death_med['연도'].astype(str)+df_kr_death_med['질병명_분류']
len(set(df_kr_death_med['key'].unique())-set(df_temp['key'].unique())), len(set(df_temp['key'].unique())-set(df_kr_death_med['key'].unique()))
# 상관관계 분석 위한 dataframe 생성
df_kr_death_med = df_kr_death_med.merge(right = df_temp, on = 'key').drop(columns = ['key','연도_y','질병명_분류_y'], axis = 1)
df_kr_death_med.columns = ['연도','질병명_분류','사망률','의약품소비량']

with st.echo():
    fig = plt.figure(figsize=(6, 4))
    sns.heatmap(df_kr_death_med.corr(), cmap = 'summer_r', annot = True, fmt = '.2f')
    st.pyplot(fig)

    
st.markdown("##### 2. 국내 사망률 - 의료 종사자 수 간 관계 분석")
# 의약품 데이터가 아니므로, 굳이 2008년부터 볼 이유가 없다 : 전체 연도에 대해서 진행함
df_kr_death_workers = df_Nmw.loc[(df_Nmw['국가']=='한국') & (df_Nmw['직업'].isin(['의사','간호사'])),"연도":"수"].groupby(by = ['직업', '연도'], as_index = False)['수'].sum()
df_kr_death_workers.columns = ['직업', '연도', '종사자 수']
df_kr_death_workers = df_kr_death_workers.merge(right = df_corr_kr.groupby('연도', as_index = False)['사망률'].mean(), on = '연도')
with st.echo():
    fig = plt.figure(figsize=(6, 4))
    sns.heatmap(df_kr_death_workers.corr(), cmap = 'summer_r', annot = True, fmt = '.2f')
    st.pyplot(fig)
    
st.markdown("##### 3. 보건 관련 지출 간 관계 분석")
st.markdown("![img](..\data\보건 관련 지출 간 관계 분석.png)")

st.markdown("##### 4. 국내 사망률 - 보건 서비스 지출 간 관계 분석")
df_temp_corr = df_corr_kr.groupby('연도', as_index = False)[['사망률']].mean()
target_list = ['치료 및 재활 치료', '장기 치료', '예방치료']
df_kr_death_service_common = df_service_common.loc[(df_service_common['국가']=='한국')&(df_service_common['항목구분'].isin(target_list)), ['연도', '서비스비용(백만$)']].groupby('연도', as_index = False).sum().reset_index(drop = True)
df_kr_death_service_common = df_kr_death_service_common.merge(right = df_temp_corr, on = '연도')
with st.echo():
    fig = plt.figure(figsize=(6, 4))
    sns.heatmap(df_kr_death_service_common.corr(), cmap = 'summer_r', annot = True)
    st.pyplot(fig)

