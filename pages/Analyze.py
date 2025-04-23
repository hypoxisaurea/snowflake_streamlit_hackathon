import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from ui.input_form import get_user_input


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


def main():
    st.header("🛍️ 고객 맞춤형 백화점 방문 & 소비 예측")
    
    user_input = get_user_input()
    st.session_state['user_input'] = user_input

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.1])
    with col3:
        if st.button("🔍 분석 시작하기"):
            switch_page("result")
    with col4:
        if st.button("🏠 홈으로 돌아가기"):
            switch_page("app")

if __name__ == "__main__":
    main()