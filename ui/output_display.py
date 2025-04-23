import streamlit as st

def display_prediction_results(prediction):
    st.subheader("🎯 예측 결과")
    
    # 백화점 예측 결과
    st.markdown("### 방문 예상 백화점")
    st.markdown(f"#### {prediction['store']}")
    
    # 지출 예측 결과
    st.markdown("### 예상 지출 금액")
    spending = prediction['spending']
    formatted_spending = f"{spending:,}원"
    st.markdown(f"#### {formatted_spending}")
    
    # 시각화
    st.markdown("### 예측 결과 시각화")
    
    # 백화점 선택 확률 (예시)
    store_probs = {
        "롯데백화점": 0.4,
        "신세계백화점": 0.3,
        "현대백화점": 0.3
    }
    
    # 막대 그래프로 백화점 선택 확률 표시
    st.bar_chart(store_probs)
    
    # 지출 금액 분포 (예시)
    spending_dist = {
        "10만원 미만": 0.2,
        "10-30만원": 0.4,
        "30-50만원": 0.3,
        "50만원 이상": 0.1
    }
    
    # 파이 차트로 지출 금액 분포 표시
    st.pie_chart(spending_dist)
    
    # 추가 정보
    st.markdown("### 💡 추천 정보")
    st.markdown("""
    - 해당 백화점의 최근 프로모션 정보
    - 방문 시간대별 혼잡도
    - 주차장 이용 정보
    - 쇼핑 가이드
    """)
