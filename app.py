import streamlit as st
import pandas as pd
from userfile import run_userfile,save_uploaded_file


def main():
    st.title('사용자가 업로드한 csv 파일을 분석합니다.')

    run_userfile()



if __name__=='__main__':
    main()