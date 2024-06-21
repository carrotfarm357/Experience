import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO

def get_exchange_rate_data(currency_code, last_page_num):
    #base_url = "https://finance.naver.com/marketindex/exchangeDailyQuote.naver"
    df = pd.DataFrame()
    
    for page_num in range(1, last_page_num+1):
        url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_USDKRW&page=3"
        
        dfs = pd.read_html(url, header=1,encoding='cp949')
        
        # 통화 코드가 잘못 지정됐거나 마지막 페이지의 경우 for 문을 빠져나옴
        if dfs[0].empty:
            if (page_num==1):
                print(f"통화 코드({currency_code})가 잘못 지정됐습니다.")
            else:
                print(f"{page_num}가 마지막 페이지입니다.")
            break
            
        # page별로 가져온 DataFrame 데이터 연결
        df = pd.concat([df, dfs[0]], ignore_index=True)
        time.sleep(0.1) # 0.1초간 멈춤
        
    return df

# -----------------------------------------------------------------------------
# df_exchange = get_exchange_rate_data('USD', 10)
# print(df_get_exchange)

st.subheader("환율 정보를 가져오는 웹 앱")

# 딕셔너리로 통화 정보
currency_name_dict={'미국 달러': 'USD', '유럽연합 유로': 'EUR', '일본 엔': 'JPY'}

# 콤보상자 작성
currency_name = st.selectbox('통화 선택', currency_name_dict.keys())
clicked = st.button("환율 데이터 가져오기")

# 환율 코드 크롤링
select_currency_code = currency_name_dict[currency_name]
last_page = 10

# 환율 데이터 표시
df_exchange = get_exchange_rate_data(select_currency_code, last_page)
st.dataframe