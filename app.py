import streamlit as st
import os


st.set_page_config(page_title="백화점 방문 예측", layout="centered")

# 사이드바 관련 모든 요소 숨기기 강화
st.markdown("""
    <style>
        /* 기본 사이드바 숨기기 */
        [data-testid="stSidebar"] { display: none !important; }
        /* 사이드바 네비게이션 숨기기 */
        [data-testid="stSidebarNav"] { display: none !important; }
        /* 확장/축소 버튼 숨기기 */
        [data-testid="collapsedControl"] { display: none !important; }

        /* 헤더의 햄버거 메뉴 (사이드바 열기 버튼) 숨기기 시도 */
        button[data-testid="stMainMenu"] {
            display: none !important;
        }
        /* 가끔 사이드바 컨트롤을 감싸는 추가 div 숨기기 시도 */
        div[data-testid="stAppViewBlockContainer"] > div:first-child > div:first-child > div:first-child {
             /* 이 선택자는 Streamlit 버전에 따라 매우 불안정할 수 있음 */
             /* display: none !important; */ /* 주의해서 사용 */
        }

        /* 기타 요소 숨기기 */
        footer { visibility: hidden; }
        header { visibility: hidden; }
        .main {
            padding: 2rem;
        }
        h1 {
            color: #1E88E5;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        h3 {
            color: #424242;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .stButton>button {
            background-color: #E53935;
            color: white;
            font-size: 1.2rem;
            padding: 0.5rem 2rem;
            border-radius: 0.5rem;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #C62828;
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)

def main():
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


    st.title("TargetIQ 🎯")
    st.markdown("#### 백화점 방문 예측 및 마케팅 전략 추천 서비스")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        이 서비스는 고객의 방문 예측과 맞춤형 마케팅 전략을 제시합니다.  
        페르소나를 확인하고, 분석을 시작해보세요!
    """)


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1.45])

    with col5:
        if st.button("🔍 분석 시작하기"):
            st.write("분석 시작하기 버튼 클릭됨, 페이지 전환 시도...")
            st.switch_page("pages/Analyze.py")

if __name__ == "__main__":
    main()
