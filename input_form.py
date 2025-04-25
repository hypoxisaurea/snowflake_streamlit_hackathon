import streamlit as st
from snowflake.snowpark import Session

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
        /* 라디오 버튼 내부 요소 수직 중앙 정렬 (필요 시 유지) */
        .stRadio > div {
            align-items: center;
        }
        /* .vcenter-label 클래스는 더 이상 사용 안 함 */
    </style>
""", unsafe_allow_html=True)


def get_user_input():
    st.header("🧩  타겟 고객 정보")
    st.markdown("<br>", unsafe_allow_html=True)

    # 성별 입력: st.markdown 레이블 사용, 위젯 레이블 숨김
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**성별**") # 별도 markdown 라벨 사용
        gender = st.radio(label="성별", options=["남성", "여성"], horizontal=True, label_visibility="collapsed") # 위젯 라벨 숨김

    st.markdown("<br>", unsafe_allow_html=True)

    # 거주지/직장 위치: 이전 방식 유지 (st.markdown + label_visibility)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**거주지**")
        residence = st.selectbox(label="🏠 거주지", options=["여의도동", "소공동", "반포동"], label_visibility="collapsed")
    with col4:
        st.markdown("**직장 위치**")
        work = st.selectbox(label="💼 직장 위치", options=["여의도동", "소공동", "반포동"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # 연령대/고객 형태: 이전 방식 유지
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("**연령대**")
        age = st.selectbox(label="연령대", options=["20대", "30대", "40대", "50대 이상"], label_visibility="collapsed")
    with col6:
        st.markdown("**고객 형태**")
        type = st.selectbox(label="고객 형태", options=["싱글", '신혼부부',"영유아가족", "청소년가족", "성인자녀가족", '실버'], label_visibility="collapsed")


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    return {
        "gender": gender,
        "age": age,
        "residence": residence,
        "work": work,
        "type": type
    }