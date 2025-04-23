import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from ui.output_display import display_prediction_results
from model import DepartmentStorePredictor


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




# 모델 로드
# visit_model = joblib.load('visit_predictor.pkl')
# spend_model = joblib.load('spending_predictor.pkl')



# visit_probs = visit_model.predict_proba(input_df)[0]
# top3_indices = np.argsort(visit_probs)[::-1][:3]
# top3_departments = visit_model.classes_[top3_indices]
# top3_probs = visit_probs[top3_indices]

# expected_spending = spend_model.predict(input_df)[0]


# for i in range(3):
#     st.write(f"{top3_departments[i]}: {round(top3_probs[i]*100, 2)}%")


# st.write(f"{int(expected_spending):,} 원")

# if expected_spending > 200000:
#     st.success("💡 프리미엄 할인 쿠폰, VIP 서비스 홍보 전략 추천!")
# elif expected_spending > 80000:
#     st.info("💡 식음료 쿠폰, 포인트 적립 이벤트 홍보 추천!")
# else:
#     st.warning("💡 첫 방문 유도용 샘플링, 경품 추천!")

# 분석 시작 버튼




def main():
    st.title("방문 예측 대시보드 🔮")
    
    # 세션 상태에서 사용자 입력 가져오기
    if 'user_input' not in st.session_state:
        st.error("입력 데이터가 없습니다. 분석 페이지로 돌아가주세요.")
        if st.button("분석 페이지로 돌아가기"):
            switch_page("analyze")
        return
    
    # 모델 초기화 및 예측
    predictor = DepartmentStorePredictor()
    prediction = predictor.predict(st.session_state['user_input'])

    st.subheader("📍 방문 가능성 높은 백화점 Top 3")
    # 결과 표시
    display_prediction_results(prediction)
    st.subheader("💰 예상 소비 금액")
    # 홈으로 돌아가기 버튼
    if st.button("🏠 홈으로 돌아가기"):
        switch_page("app")
    if st.button("다시 해보기"):
        switch_page("analyze")


if __name__ == "__main__":
    main()