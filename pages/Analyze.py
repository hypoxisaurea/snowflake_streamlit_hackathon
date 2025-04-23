import streamlit as st
from ui.input_form import get_user_input
from streamlit_extras.switch_page_button import switch_page

# 사이드바 제거
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

st.header("🛍️ 고객 맞춤형 백화점 방문 & 소비 예측")

user_inputs = get_user_input()

# 5개의 column을 만들고 오른쪽 2개만 사용
col1, col2, col3, col4 = st.columns([1, 1, 1, 1.1])

with col3:
    if st.button("🔍 분석 시작하기"):
        switch_page("result")
with col4:
    if st.button("🏠 홈으로 돌아가기"):
        switch_page("app")