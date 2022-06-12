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
import Stramlit as st

## Title
st.title("주요 질병 사망자 및 보건 환경 비교 분석")

## Header
st.header("멋쟁이 사자처럼 AI School 6기 MID Project 2팀")
st.text("팀원: 김재석, 김채현, 김태훈, 박이슬, 손유선")

## 사용 라이브러리
st.markdown("## 사용 라이브러리\n"
            "```python"
            "import numpy as np"
            "import pandas as pd"
            "import seaborn as sns"
            "import plotly.express as px"
            "import matplotlib.pyplot as plt"
            "import cufflinks as cf"
            "import chart_studio"
            "import folium"
            "from folium.plugins import MarkerCluster"
            "import json"
            "import Stramlit as st"
            )

## Data Load
df_death_rate = pd.read_csv("data/pre_df/df_death_rate.csv")
df_Nmw = pd.read_csv("data/pre_df/df_Nmw.csv")
df_service = pd.read_csv("data/pre_df/df_service.csv")
df_service_common = pd.read_csv("data/pre_df/df_service_common.csv")
df_medicion = pd.read_csv("data/pre_df/df_medicion.csv")
df_welfare = pd.read_csv("data/pre_df/df_welfare.csv")

## part 1
st.markdown("## 1. 주요 사망 원인별 사망률")
st.markdown("### Data set")
st.dataframe(df_death_rate) # st.table도 사용 가능 -> 일부만 표시시

## part2
st.markdown("## 2. 의료 종사자 수")
st.markdown("### Data set")
st.dataframe(df_Nmw)

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
st.mrkdown("#### 공공사회 복지 지출")
st.dataframe(df_welfare)


## part 6
st.markdown("## 6. 최종")
st.markdown("### Data set")
st.text("앞서 사용한 모든 데이터를 합쳐 하나의 데이터로 생성")
df_corr = pd.read_csv("data/pre_df/df_corr.csv")
st.dataframe(df_corr)