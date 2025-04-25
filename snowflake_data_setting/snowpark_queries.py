from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

# 🔌 세션 연결: SiS 우선, 실패 시 로컬 설정 시도
session = None
try:
    # 1. Streamlit in Snowflake 환경 시도
    session = get_active_session()
    st.success("❄️ Streamlit in Snowflake 환경에서 활성 Snowpark 세션을 가져왔습니다.")
except Exception:
    # 2. SiS 실패 시 로컬 환경 설정 시도
    st.warning("Streamlit in Snowflake 활성 세션을 찾을 수 없습니다. 로컬 설정으로 세션 생성을 시도합니다...")
    try:
        load_dotenv()
        connection_parameters = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "account": os.getenv("DB_ACCOUNT"),
            "warehouse": os.getenv("DB_WAREHOUSE"),
            "database": os.getenv("DB_DATABASE"),
            "schema": os.getenv("DB_SCHEMA"),
            "role": os.getenv("DB_ROLE"),
        }
        if not all(connection_parameters.values()):
            missing = [k for k, v in connection_parameters.items() if not v]
            st.error(f".env 파일 또는 환경 변수에 다음 Snowflake 연결 정보가 누락되었습니다: {', '.join(missing)}")
            st.stop()

        session = Session.builder.configs(connection_parameters).create()
        st.success("✅ 로컬 설정(.env)으로 Snowpark 세션을 성공적으로 생성했습니다.")
    except Exception as e:
        st.error(f"로컬 설정으로 Snowpark 세션 생성에 실패했습니다: {e}")
        st.exception(e)
        st.stop()

# 세션 최종 확인
if not session:
    st.error("Snowpark 세션을 초기화할 수 없습니다. 앱을 중지합니다.")
    st.stop()

# 🧠 데이터 처리 함수 (캐싱)
@st.cache_data(show_spinner="🌀 [위치 기반] 백화점 선호도 점수를 계산 중입니다...")
def get_store_score(res_dong: str, work_dong: str) -> pd.DataFrame:
    """
    거주지와 직장지 정보를 바탕으로 백화점별 선호도 점수를 계산합니다.
    LOC_TYPE: 1=거주지 기준, 2=직장지 기준
    점수 = 거주지 비율 * 0.6 + 직장지 비율 * 0.4
    """
    if not session:
        st.error("Snowpark 세션이 활성화되지 않았습니다.")
        return pd.DataFrame({'DEP_NAME': [], 'score': []})

    # 주거지 기준 쿼리
    query_home = f"""
    SELECT DEP_NAME, RATIO
    FROM SNOWFLAKE_STREAMLIT_HACKATHON_LOPLAT_HOME_OFFICE_RATIO
    WHERE ADDR_LV3 = '{res_dong}' AND LOC_TYPE = 1
    """
    try:
        home_df = session.sql(query_home).to_pandas()
    except Exception as e:
        st.error(f"거주지 기반 데이터 조회 중 오류 발생: {e}")
        home_df = pd.DataFrame({'DEP_NAME': [], 'RATIO': []})

    # 직장지 기준 쿼리
    query_work = f"""
    SELECT DEP_NAME, RATIO
    FROM SNOWFLAKE_STREAMLIT_HACKATHON_LOPLAT_HOME_OFFICE_RATIO
    WHERE ADDR_LV3 = '{work_dong}' AND LOC_TYPE = 2
    """
    try:
        work_df = session.sql(query_work).to_pandas()
    except Exception as e:
        st.error(f"직장지 기반 데이터 조회 중 오류 발생: {e}")
        work_df = pd.DataFrame({'DEP_NAME': [], 'RATIO': []})

    # 점수 결합 계산
    if home_df.empty and work_df.empty:
        return pd.DataFrame({'DEP_NAME': [], 'score': []})
    elif home_df.empty:
        merged = work_df.rename(columns={'RATIO': 'RATIO_work'})
        merged['RATIO_home'] = 0
    elif work_df.empty:
        merged = home_df.rename(columns={'RATIO': 'RATIO_home'})
        merged['RATIO_work'] = 0
    else:
        merged = pd.merge(home_df, work_df, on="DEP_NAME", how="outer", suffixes=("_home", "_work")).fillna(0)

    # 점수 계산 (RATIO_home 또는 RATIO_work가 없을 경우 대비)
    merged["score"] = merged.get("RATIO_home", 0) * 0.6 + merged.get("RATIO_work", 0) * 0.4
    merged = merged.sort_values("score", ascending=False)

    # 백화점 이름 매핑
    store_name_map = {
        '롯데백화점_본점': '롯데백화점',
        '신세계_강남': '신세계백화점',
        '더현대서울': '현대백화점'
    }
    if 'DEP_NAME' in merged.columns:
        merged['DEP_NAME'] = merged['DEP_NAME'].replace(store_name_map)
    else:
        st.warning("결과에 DEP_NAME 컬럼이 없어 백화점 이름을 변환할 수 없습니다.")
        return pd.DataFrame({'DEP_NAME': [], 'score': []})

    return merged[['DEP_NAME', 'score']]

# 🧠 소비력 추정 함수 (캐싱)
@st.cache_data(show_spinner="💳 [위치 기반] 평균 소비력을 추정 중입니다...")
def get_estimated_spending(res_dong: str) -> int:
    """
    거주지 동(dong)을 기준으로 'dong_features' 테이블에서
    평균 백화점 소비액(AVG_DEPARTMENT_STORE_SALES)을 조회합니다.
    """
    if not session:
        st.error("Snowpark 세션이 활성화되지 않았습니다.")
        return 0

    query = f"""
    SELECT AVG_DEPARTMENT_STORE_SALES
    FROM dong_features
    WHERE DONG = '{res_dong}'
    """
    try:
        df = session.sql(query).to_pandas()
        if df.empty or pd.isna(df.iloc[0, 0]):
            st.warning(f"'{res_dong}'에 대한 소비력 데이터가 없습니다.")
            return 0
        avg_sales = df.iloc[0, 0]
        if isinstance(avg_sales, (int, float)):
            return int(avg_sales)
        else:
            st.warning(f"'{res_dong}'의 소비력 데이터 형식이 올바르지 않습니다: {avg_sales}")
            return 0
    except Exception as e:
        st.error(f"소비력 데이터 조회 중 오류 발생: {e}")
        return 0 