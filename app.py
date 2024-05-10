import streamlit as st
import pandas as pd
from userfile import run_userfile,save_uploaded_file


def main():
    st.title('사용자가 업로드한 csv 파일을 분석합니다.')
    st.subheader('사용자가 원하는 컬럼끼리의 상관관계, 여러 형태의 차트를 출력합니다.')

    run_userfile()



if __name__=='__main__':
    main()