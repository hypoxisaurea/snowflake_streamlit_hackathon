import streamlit as st

# 사이드바 제거
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        div[data-baseweb="select"] input {
            caret-color: transparent;
        }
    </style>
""", unsafe_allow_html=True)


def get_user_input():
    st.subheader("👤 고객 정보 입력")

    col1, col2 = st.columns(2)
    with col1:
        gender = st.radio("성별", ["남성", "여성"], horizontal=True)
    with col2:
        age = st.selectbox("연령대", ["20대", "30대", "40대", "50대 이상"])

    col3, col4 = st.columns(2)
    with col3:
        residence = st.selectbox("🏠 거주지", ["여의도동", "소공동", "반포동"])
    with col4:
        work = st.selectbox("💼 직장 위치", ["여의도동", "소공동", "반포동"])

    st.divider()


    st.subheader("🌤️ 환경 조건")

    col5, col6 = st.columns(2)
    with col5:
        weather = st.selectbox("날씨", ["맑음", "흐림", "비", "눈"])
    with col6:
        season = st.slider("계절 (월)", 1, 12, 4)

    return {
        "gender": gender,
        "age": age,
        "residence": residence,
        "work": work,
        "weather": weather,
        "season": season
    }