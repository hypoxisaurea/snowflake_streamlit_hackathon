import streamlit as st
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(page_title="백화점 방문 예측", layout="centered")

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
    st.title("TargetIQ 🎯")
    st.markdown("### 백화점 방문 예측 및 마케팅 전략 추천 서비스")
    st.markdown("""
        이 서비스는 고객의 방문 예측과 맞춤형 마케팅 전략을 제시합니다.  
        페르소나를 확인하고, 분석을 시작해보세요!
    """)

    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1.5])

    with col5:
        if st.button("🔍 분석 시작하기"):
            switch_page("analyze")

if __name__ == "__main__":
    main()
