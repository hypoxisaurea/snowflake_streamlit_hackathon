import streamlit as st
import os
from input_form import get_user_input # 경로 수정
from model import DepartmentStorePredictor # 모델 임포트
from output_display import display_prediction_results # 경로 수정


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

    

    # "예측 실행하기" 버튼이 클릭되었을 때만 예측 및 결과 표시
    if predict_button_clicked:
        if user_input: # 입력값이 있는지 확인
            try:
                # 모델 초기화 및 예측
                with st.spinner('Predicting...'): # 스피너 추가
                    predictor = DepartmentStorePredictor()
                    prediction = predictor.predict(user_input)

                # 결과 표시
                st.divider() # 입력과 결과 구분선
                display_prediction_results(prediction)

            except Exception as e:
                st.error(f"예측 중 오류가 발생했습니다: {e}")
        else:
            st.warning("고객 정보를 먼저 입력해주세요.")


if __name__ == "__main__":
    main()