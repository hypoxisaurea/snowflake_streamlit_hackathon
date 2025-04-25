import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def display_prediction_results(ml_prediction, store_score_df, location_based_spending):
    st.title("방문 예측 및 분석 대시보드 🔮")
    st.subheader("🎯 분석 결과 요약")
    
    # --- 백화점 방문 예측 및 선호도 ---
    st.markdown("### 🏢 백화점 방문 분석")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 고객 특성 기반 예측")
        if ml_prediction and 'store_predictions' in ml_prediction:
            store_probs = ml_prediction['store_predictions']
            # 확률 내림차순 정렬
            sorted_store_probs = dict(sorted(store_probs.items(), key=lambda item: item[1], reverse=True))

            fig_ml = go.Figure(data=[
                go.Bar(
                    x=list(sorted_store_probs.keys()),
                    y=list(sorted_store_probs.values()),
                    text=[f"{prob:.1%}" for prob in sorted_store_probs.values()],
                    textposition='auto',
                    marker_color='skyblue'
                )
            ])
            fig_ml.update_layout(
                xaxis_title="백화점",
                yaxis_title="예상 방문 확률",
                yaxis=dict(tickformat=".1%"),
                showlegend=False,
                height=300,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_ml, use_container_width=True)

            best_store_ml = max(store_probs.items(), key=lambda x: x[1])
            st.info(f"**가장 방문 확률 높은 곳:** {best_store_ml[0]} ({best_store_ml[1]:.1%})")
        else:
            st.warning("고객 특성 기반 방문 예측 결과를 불러올 수 없습니다.")

    with col2:
        st.markdown("#### 위치(거주지/직장) 기반 분석")
        if not store_score_df.empty:
            # 점수 내림차순 정렬
            sorted_store_score = store_score_df.sort_values("score", ascending=False)

            fig_loc = go.Figure(data=[
                go.Bar(
                    x=sorted_store_score['DEP_NAME'],
                    y=sorted_store_score['score'],
                    text=[f"{score:.2f}" for score in sorted_store_score['score']],
                    textposition='auto',
                    marker_color='lightgreen'
                )
            ])
            fig_loc.update_layout(
                xaxis_title="백화점",
                yaxis_title="선호도 점수",
                yaxis=dict(range=[0, max(sorted_store_score['score']) * 1.1]),
                showlegend=False,
                height=300,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_loc, use_container_width=True)

            best_store_loc = sorted_store_score.iloc[0]
            st.info(f"**가장 선호도 높은 곳:** {best_store_loc['DEP_NAME']} (점수: {best_store_loc['score']:.2f})")

            # 상세 점수 테이블은 Expander 안에 넣기
            with st.expander("상세 점수 보기 (위치 기반)"):
                st.dataframe(sorted_store_score.rename(columns={'DEP_NAME': '백화점', 'score': '선호도 점수'}).set_index('백화점'), use_container_width=True)
        else:
            st.warning("위치 기반 백화점 선호도 점수를 계산할 수 없습니다.")

    st.divider()

    # --- 지출 예측 및 소비력 비교 ---
    st.markdown("### 💰 예상 소비력 분석")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### 고객 특성 기반 예측")
        if ml_prediction and 'spending' in ml_prediction:
            spending_ml = ml_prediction['spending']
            formatted_spending_ml = f"{spending_ml:,}원"
            st.metric(label="예상 지출 금액", value=formatted_spending_ml)
        else:
             st.metric(label="예상 지출 금액", value="N/A")
             st.warning("고객 특성 기반 지출 예측 결과를 불러올 수 없습니다.")


    with col4:
        st.markdown("#### 거주지 평균 소비력")
        if location_based_spending > 0:
             formatted_spending_loc = f"{location_based_spending:,}원"
             st.metric(label=f"거주지(동) 평균", value=formatted_spending_loc, help="선택하신 거주지의 평균 백화점 소비액입니다.")
        else:
             st.metric(label=f"거주지(동) 평균", value="N/A", help="선택하신 거주지의 평균 백화점 소비액 데이터가 없거나 조회 중 오류가 발생했습니다.")


    # 지출 금액 분포 시각화 (기존 유지 - ML 예측 기반)
    # st.markdown("#### 예상 지출 금액 분포 (ML 예측 기반)")
    # spending_ranges = {
    #     "10만원 미만": 0.2, "10-30만원": 0.4, "30-50만원": 0.3, "50만원 이상": 0.1
    # } # 이 부분은 실제 분포를 반영하도록 수정 필요
    # if ml_prediction and 'spending' in ml_prediction:
    #     # spending 값에 따라 동적으로 분포를 생성하거나, 고정 분포 사용
    #     fig_pie = px.pie(
    #         values=list(spending_ranges.values()), names=list(spending_ranges.keys()), title="참고: 일반적인 지출 분포 예시"
    #     )
    #     st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # 구매력 평가 (기존 유지 - ML 예측 기반)
    st.markdown("### ⭐ 고객 등급 평가 (ML 예측 기반)")
    if ml_prediction and 'spending' in ml_prediction:
        spending = ml_prediction['spending']
        if spending > 500000:
            st.success("💎 프리미엄 고객")
            st.markdown("- VIP 서비스, 프리미엄 쿠폰, 라운지, 개인 쇼핑 지원 등")
        elif spending > 300000:
            st.info("🌟 골드 고객")
            st.markdown("- 특별 할인 쿠폰, 포인트 이벤트, 주차, 멤버십 혜택 등")
        else:
            st.warning("⭐ 일반 고객")
            st.markdown("- 첫 방문 샘플링, 경품 이벤트, 기본 멤버십, 할인 쿠폰 등")
    else:
        st.warning("고객 등급을 평가할 수 없습니다 (ML 예측 결과 필요).")


    st.divider()

    # 추가 정보 (기존 유지)
    st.markdown("### 💡 추가 활용 정보")
    st.markdown("""
    - **마케팅 액션:** 예측된 방문 선호도와 예상 소비력을 바탕으로 맞춤형 프로모션 제안 (예: 타겟 쿠폰 발송)
    - **매장 운영:** 예상 방문 확률이 높은 고객 그룹의 선호 시간대/요일 분석하여 효율적인 인력 배치
    - **MD 전략:** 고객의 라이프스타일과 예상 소비력을 고려한 상품 추천 및 진열
    - **데이터 심층 분석:** 위치 기반 데이터와 고객 특성 데이터를 결합하여 더 정교한 고객 세분화 및 이탈 방지 전략 수립
    """)
