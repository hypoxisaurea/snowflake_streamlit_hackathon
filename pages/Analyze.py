import streamlit as st
import os
from input_form import get_user_input # 경로 수정
from model import DepartmentStorePredictor # 모델 임포트
from output_display import display_prediction_results # 경로 수정
# Snowpark 쿼리 함수 임포트 경로 수정
from snowflake_data_setting.snowpark_queries import get_store_score, get_estimated_spending
import pandas as pd # pandas 임포트 추가


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
    # 사용자 입력 받기
    user_input = get_user_input()

    # 버튼 배치를 위한 컬럼 생성 (빈 공간 + 버튼1 + 버튼2)
    empty_col, pred_btn_col, home_btn_col = st.columns([4.5, 1.1, 1]) # 비율 조정 (예: 5:1.1:1)

    predict_button_clicked = False
    with pred_btn_col: # "예측 실행" 버튼
        if st.button("📊 예측하기"):
            predict_button_clicked = True

    with home_btn_col: # "홈으로 돌아가기" 버튼
        if st.button("🏠 홈으로"):
            st.switch_page("app.py")

    
    st.divider()
    

    # "예측하기" 버튼이 클릭되었을 때만 예측 및 결과 표시
    if predict_button_clicked:
        if user_input and user_input.get("residence") and user_input.get("work"): # 거주지/직장 정보 확인
            try:
                # --- 기존 머신러닝 예측 ---
                ml_prediction = None
                with st.spinner('🤖 고객 특성 기반 예측 모델을 실행 중입니다...'): # 스피너 메시지 수정
                    predictor = DepartmentStorePredictor()
                    ml_prediction = predictor.predict(user_input)

                # --- Snowpark 위치 기반 분석 ---
                store_score_df = pd.DataFrame() # 기본 빈 데이터프레임
                location_based_spending = 0 # 기본값 0

                # get_store_score 호출 (Snowpark 캐싱 데코레이터에 스피너 있음)
                store_score_df = get_store_score(
                    res_dong=user_input["residence"],
                    work_dong=user_input["work"]
                )

                # get_estimated_spending 호출 (Snowpark 캐싱 데코레이터에 스피너 있음)
                location_based_spending = get_estimated_spending(
                    res_dong=user_input["residence"]
                )

                # --- 결과 표시 ---
                st.divider() # 입력과 결과 구분선
                # display_prediction_results 함수에 모든 결과 전달
                display_prediction_results(
                    ml_prediction=ml_prediction, # 이름 명확화
                    store_score_df=store_score_df,
                    location_based_spending=location_based_spending
                )

            except Exception as e:
                st.error(f"예측/분석 중 오류가 발생했습니다: {e}")
                st.exception(e) # 상세 오류 로그 표시 (디버깅용)
        else:
            st.warning("고객 정보(특히 거주지, 직장 위치)를 먼저 입력해주세요.")


if __name__ == "__main__":
    main()