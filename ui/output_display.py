import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def display_prediction_results(prediction):
    st.subheader("🎯 예측 결과")
    
    # 백화점 방문 예측 결과
    st.markdown("### 방문 예상 백화점")
    
    # 백화점 선택 확률을 막대 그래프로 표시
    store_probs = prediction['store_predictions']
    fig = go.Figure(data=[
        go.Bar(
            x=list(store_probs.keys()),
            y=list(store_probs.values()),
            text=[f"{prob:.1%}" for prob in store_probs.values()],
            textposition='auto',
        )
    ])
    fig.update_layout(
        title="백화점 방문 확률",
        xaxis_title="백화점",
        yaxis_title="방문 확률",
        yaxis=dict(tickformat=".1%"),
        showlegend=False
    )
    st.plotly_chart(fig)
    
    # 가장 높은 확률의 백화점 강조
    best_store = max(store_probs.items(), key=lambda x: x[1])
    st.markdown(f"#### 가장 방문 가능성이 높은 백화점: {best_store[0]} ({best_store[1]:.1%})")
    
    # 지출 예측 결과
    st.markdown("### 예상 지출 금액")
    spending = prediction['spending']
    formatted_spending = f"{spending:,}원"
    st.markdown(f"#### {formatted_spending}")
    
    # 지출 금액 분포 시각화
    spending_ranges = {
        "10만원 미만": 0.2,
        "10-30만원": 0.4,
        "30-50만원": 0.3,
        "50만원 이상": 0.1
    }
    
    fig = px.pie(
        values=list(spending_ranges.values()),
        names=list(spending_ranges.keys()),
        title="예상 지출 금액 분포"
    )
    st.plotly_chart(fig)
    
    # 구매력 평가
    st.markdown("### 💰 구매력 평가")
    if spending > 500000:
        st.success("💎 프리미엄 고객")
        st.markdown("""
        - VIP 서비스 제공
        - 프리미엄 할인 쿠폰
        - 전용 라운지 이용
        - 개인 쇼핑 어시스턴트 서비스
        """)
    elif spending > 300000:
        st.info("🌟 골드 고객")
        st.markdown("""
        - 특별 할인 쿠폰
        - 포인트 적립 이벤트
        - 주차 서비스
        - 멤버십 혜택
        """)
    else:
        st.warning("⭐ 일반 고객")
        st.markdown("""
        - 첫 방문 유도용 샘플링
        - 경품 이벤트
        - 기본 멤버십 혜택
        - 할인 쿠폰
        """)
    
    # 추가 정보
    st.markdown("### 💡 추천 정보")
    st.markdown("""
    - 해당 백화점의 최근 프로모션 정보
    - 방문 시간대별 혼잡도
    - 주차장 이용 정보
    - 쇼핑 가이드
    """)
