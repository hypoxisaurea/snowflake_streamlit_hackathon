import streamlit as st
import joblib
import pandas as pd
import numpy as np
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


# 모델 로드
# visit_model = joblib.load('visit_predictor.pkl')
# spend_model = joblib.load('spending_predictor.pkl')

st.title("방문 예측 대시보드 🔮")

# visit_probs = visit_model.predict_proba(input_df)[0]
# top3_indices = np.argsort(visit_probs)[::-1][:3]
# top3_departments = visit_model.classes_[top3_indices]
# top3_probs = visit_probs[top3_indices]

# expected_spending = spend_model.predict(input_df)[0]

st.subheader("📍 방문 가능성 높은 백화점 Top 3")
# for i in range(3):
#     st.write(f"{top3_departments[i]}: {round(top3_probs[i]*100, 2)}%")

st.subheader("💰 예상 소비 금액")
# st.write(f"{int(expected_spending):,} 원")

# if expected_spending > 200000:
#     st.success("💡 프리미엄 할인 쿠폰, VIP 서비스 홍보 전략 추천!")
# elif expected_spending > 80000:
#     st.info("💡 식음료 쿠폰, 포인트 적립 이벤트 홍보 추천!")
# else:
#     st.warning("💡 첫 방문 유도용 샘플링, 경품 추천!")

# 분석 시작 버튼
if st.button("다시 해보기"):
    switch_page("analyze")