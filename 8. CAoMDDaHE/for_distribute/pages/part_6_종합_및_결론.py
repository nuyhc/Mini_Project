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
from PIL import Image

st.set_page_config(layout='wide')

country_intersection = ['룩셈부르크',  '네덜란드',  '영국',  '이탈리아',  
        '캐나다',  '오스트레일리아',  '한국',  '일본',  '스페인',  '헝가리',  '독일',  
        '에스토니아',  '그리스',  '슬로바키아',  '핀란드',  '벨기에',  '체코',  
        '슬로베니아',  '프랑스',  '스웨덴',  '노르웨이',  '뉴질랜드',  '라트비아',  
        '덴마크',  '오스트리아',  '포르투갈',  '아일랜드',  '아이슬란드']


## part 6
st.markdown("## 6. 최종")
st.markdown("### Data set")
st.text("앞서 사용한 모든 데이터를 합쳐 하나의 데이터로 생성")
df_death_rate = pd.read_csv("data/pre_df/df_death_rate.csv")
df_corr = pd.read_csv("data/pre_df/df_corr.csv")
df_Nmw = pd.read_csv("data/pre_df/df_Nmw.csv")
df_service = pd.read_csv("data/pre_df/df_service.csv")
df_service_common = pd.read_csv("data/pre_df/df_service_common.csv")
df_medicion = pd.read_csv("data/pre_df/df_medicion.csv")
df_welfare = pd.read_csv("data/pre_df/df_welfare.csv")
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
imgr = Image.open('data/img.png')
st.image(imgr)

st.markdown("##### 4. 국내 사망률 - 보건 서비스 지출 간 관계 분석")
df_temp_corr = df_corr_kr.groupby('연도', as_index = False)[['사망률']].mean()
target_list = ['치료 및 재활 치료', '장기 치료', '예방치료']
df_kr_death_service_common = df_service_common.loc[(df_service_common['국가']=='한국')&(df_service_common['항목구분'].isin(target_list)), ['연도', '서비스비용(백만$)']].groupby('연도', as_index = False).sum().reset_index(drop = True)
df_kr_death_service_common = df_kr_death_service_common.merge(right = df_temp_corr, on = '연도')
with st.echo():
    fig = plt.figure(figsize=(6, 4))
    sns.heatmap(df_kr_death_service_common.corr(), cmap = 'summer_r', annot = True)
    st.pyplot(fig)

