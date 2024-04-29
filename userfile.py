import streamlit as st
import pandas as pd
from datetime import datetime
import os
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
import plotly.graph_objects as go
import plotly.express as px
import random




def save_uploaded_file(directory, file, max_size):
    # 파일 크기 체크
    if file.size > max_size:
        st.error("파일 크기가 너무 큽니다. 5MB 이하의 파일만 업로드할 수 있습니다. 파일이 손상되어 출렵됩니다.")
        return

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(os.path.join(directory, file.name), 'wb') as f:
        f.write(file.getbuffer())
    
    st.success(f"{file.name}이 {directory}에 저장되었습니다.")

# 메인 코드
def run_userfile():
    file = st.file_uploader("파일을 업로드하세요.", type=["csv", "txt"])
    if file is not None:
        save_uploaded_file(".", file, max_size=5*1024*1024)  # 최대 파일
    if file is not None:
        # 파일에서 데이터프레임으로 읽어오기
        df = pd.read_csv(file)
        
        # 데이터프레임이 비어 있는지 확인
        if df.empty:
            st.warning("파일이 비어 있습니다.")
        else:
            current_time = datetime.now()
            new_filename = current_time.isoformat().replace(':', '_') + '.csv'
            file.name = new_filename
            st.write("Uploaded file:")
            st.dataframe(df)

        # 정수로 된 컬럼만 선택
        num_columns = df.select_dtypes(include=['int','float'])
        st.dataframe(num_columns)
        num_columns_list = num_columns.columns

        columns_list = st.multiselect('컬럼을 선택 하세요.', num_columns_list)

        st.text('선택하신 컬럼의, 각 컬럼별 최대/최소 데이터를 보여드립니다.')
        numbers_list = []

        for column in columns_list:
            columns_list_index = []
            columns_list_index.append(df.loc[df[column] == df[column].max()].index[0])
            columns_list_index.append(df.loc[df[column] == df[column].min()].index[0])
            numbers_list.append(columns_list_index)

        for i in numbers_list:
            st.text(f'선택하신 컬럼 {columns_list}의 최대, 최소값이 포함된 행입니다.')
            st.dataframe(df.iloc[i, :])




    if len(columns_list) >= 1:
        #1. 페어플롯을 그린다.
        #tobo : 1. pairplot 을 다른 라이브러리 이용해서 하는 방법
        # pairplot 말고, 반복문으로 두 컬럼씩 관계를 차트로 그리는 방법
        pair_plot = sb.pairplot(data=df, vars=columns_list)
        pair_plot.fig.suptitle("corr",y=1.02)
        st.pyplot(pair_plot)

    

        #.상관계수 보여준다.
        st.dataframe(df[columns_list].corr())

        combinations_list = list(combinations(columns_list, 2))
        for pair in combinations_list:
            pair_plot = sb.pairplot(data=df, vars=pair)
            st.pyplot(pair_plot)


        else:
            st.text('컬럼은 2개이상 선택해야 합니다.')

        pair_plot = sb.pairplot(data=df[columns_list])

        # pairplot에 제목 추가
        pair_plot.fig.suptitle("Pair Plot", y=1.02)

        # Streamlit에 pairplot 표시
        st.pyplot(pair_plot)

    string_df = df.select_dtypes(include=['object'])
    string_columns_list = string_df.columns



    y_choice = st.selectbox('비교할 숫자 데이터를 선택하세요', num_columns_list)
    x_choice = st.selectbox('비교할 문자 데이터를 선택하세요', string_columns_list)
    chart_user=[x_choice,y_choice]
    st.dataframe(df[[x_choice,y_choice]])
    data_limit=st.radio('데이터가 많아 차트 보기가 어렵다면 데이터의 갯수를 정해주세요',['그대로 보기','정렬해서 보기'], index=0)


    
    if data_limit == '정렬해서 보기':
        sort_order = st.radio('정렬 순서를 선택하세요', ['오름차순', '내림차순','랜덤'])
        if sort_order == '오름차순':
            # 오름차순 정렬을 선택한 경우의 동작
            st.write('오름차순으로 데이터를 정렬합니다. 데이터의 갯수를 입력해 주세요.')
            user_count = st.number_input('데이터의 갯수를 입력해 주세요.', min_value=0, max_value=len(df.index))
            sorted_df = df[[y_choice,x_choice]].sort_index(ascending=True).head(user_count)
            st.dataframe(sorted_df)
        elif sort_order == '내림차순':
            # 내림차순 정렬을 선택한 경우의 동작
            st.write('내림차순으로 데이터를 정렬합니다. 데이터의 갯수를 입력해 주세요.')
            user_count = st.number_input('데이터의 갯수를 입력해 주세요.', min_value=0, max_value=len(df.index))
            sorted_df = df[[y_choice,x_choice]].sort_index(ascending=False).head(user_count)
            st.dataframe(sorted_df)
        elif sort_order == '랜덤':
            random_button_clicked = st.button('새로운 랜덤값 생성')
            st.write('랜덤으로 데이터를추출하여 데이터를 정렬합니다. 데이터의 갯수를 입력해 주세요.')
            user_count = st.number_input('데이터의 갯수를 입력해 주세요.', min_value=0, max_value=len(df.index))

            random_seed = random.randint(1, 1000)
            sorted_df = df[[y_choice, x_choice]].sample(n=100, random_state=random_seed).head(user_count)
            st.dataframe(sorted_df)


    else:
        st.write('현재는 정렬하지 않고 데이터를 그대로 보여줍니다.')
    chart = st.checkbox("차트 확인하기")
    if chart:
        if data_limit == '그대로 보기':
            sort_order = st.radio('정렬 순서를 선택하세요', ['오름차순', '내림차순',])
            
            if sort_order == '오름차순':
                sorted_df = df.sort_values(by=y_choice, ascending=True)
                fig = go.Figure(go.Bar(x=sorted_df[x_choice], y=sorted_df[y_choice], orientation='v'))  
                st.plotly_chart(fig) 

                fig1 = px.pie(df, values=y_choice, names=x_choice)
                st.plotly_chart(fig1)
            elif sort_order == '내림차순':
                sorted_df = df.sort_values(by=y_choice, ascending=False)
                fig = go.Figure(go.Bar(x=sorted_df[x_choice], y=sorted_df[y_choice], orientation='v'))
                st.plotly_chart(fig)

                fig1 = px.pie(df, values=y_choice, names=x_choice)
                st.plotly_chart(fig1)
        elif data_limit == '정렬해서 보기':
            if sorted_df is not None:  # sorted_df가 None이 아닌 경우에만 사용합니다.
                fig = go.Figure(go.Bar(x=sorted_df[x_choice], y=sorted_df[y_choice], orientation='v'))  # x와 y를 각각 설정
                st.plotly_chart(fig)

                fig1 = px.pie(sorted_df, values=y_choice, names=x_choice)
                st.plotly_chart(fig1)


