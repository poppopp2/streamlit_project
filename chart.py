# from userfile import run_userfile,save_uploaded_file
# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import seaborn as sb
# import matplotlib.pyplot as plt
# import numpy as np
# from itertools import combinations
# import plotly.express as px
# from userfile import run_userfile



# def run_chart():
#     file1 = st.file_uploader('CSV 파일 선택하세요.', type='CSV', key='file_uploader1')
#     if file1 is not None:
#         df = pd.read_csv(file1)
            
#             # 데이터프레임이 비어 있는지 확인
#         if df.empty:
#             st.warning("파일이 비어 있습니다.")
#         else:
#             current_time = datetime.now()
#             new_filename = current_time.isoformat().replace(':', '_') + '.csv'
#             file1.name = new_filename
#             st.write("Uploaded file:")
#             st.dataframe(df)

#             # 정수로 된 컬럼만 선택
#             num_columns = df.select_dtypes(include=['int','float'])
#             st.dataframe(num_columns)
#             num_columns_list = num_columns.columns
#             st.subheader('d')

#             num_columns = df.select_dtypes(include=['int','float'])
#             string_df = df.select_dtypes(include=['object'])
#             string_columns_list = string_df.columns
#             x_choice = st.selectbox('비교할 숫자 데이터를 선택하세요', num_columns_list)
#             y_choice = st.selectbox('비교할 문자 데이터를 선택하세요', string_columns_list)
    







