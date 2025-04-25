import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import snowflake.connector
import os
from dotenv import load_dotenv
import streamlit as st # Streamlit 임포트 추가

class DepartmentStorePredictor:
    def __init__(self):
        # Snowflake 연결 설정
        load_dotenv()
        self.conn = None # conn 초기화
        self.is_initialized = False # 초기화 플래그 추가 (기본 False)

        try:
            self.conn = snowflake.connector.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                account=os.getenv("DB_ACCOUNT"),
                warehouse=os.getenv("DB_WAREHOUSE"),
                database=os.getenv("DB_DATABASE"),
                schema=os.getenv("DB_SCHEMA"),
                role=os.getenv("DB_ROLE"),
            )
        except Exception as e:
            print(f"Snowflake connection failed: {e}")
            st.error(f"ML 모델용 Snowflake 연결 실패: {e}")
            # 연결 실패 시 더 이상 진행하지 않음 (또는 기본 모델 로드 등의 로직 추가)
            return # __init__ 종료

        # 백화점 목록
        self.stores = ["롯데백화점", "신세계백화점", "현대백화점"]

        # 모델 초기화
        self.store_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.spending_model = RandomForestRegressor(n_estimators=100, random_state=42)

        # 데이터 로드 및 모델 학습
        try:
            self._load_data()
            self._train_models()
            if self.dep_data.empty or self.sales_data.empty: # _train_models 내부 검사 후 재확인
                 st.warning("데이터 로딩 후 확인 결과, 학습 데이터가 부족하여 ML 모델이 초기화되지 않았습니다.")
                 # self.is_initialized는 False 유지됨
            else:
                 self.is_initialized = True # 성공적으로 학습 완료 시 True로 설정
                 print("DepartmentStorePredictor initialized successfully.") # 성공 로그 추가
        except Exception as e:
            print(f"Error during model initialization: {e}")
            st.error(f"ML 모델 초기화 중 오류 발생: {e}")
            # self.is_initialized는 False 유지됨
        finally:
             if self.conn:
                 self.conn.close() # 데이터 로드/학습 후 연결 종료 보장
                 print("Snowflake connection for ML model closed.")


    def _load_data(self):
        # 데이터 로드 전에 연결 상태 확인
        if not self.conn:
             print("Error: Snowflake connection not established. Cannot load data.")
             st.error("ML 모델 데이터 로딩 실패: Snowflake 연결 없음.")
             self.dep_data = pd.DataFrame() # 빈 데이터프레임 할당
             self.sales_data = pd.DataFrame()
             return

        print("Loading data for ML model...") # 로딩 시작 로그
        # 백화점 방문 데이터 로드
        query_dep = """
        SELECT AGE_GROUP, GENDER, TIME_SLOT, WEEKDAY_WEEKEND, LIFESTYLE, DEP_NAME
        FROM DEP_STORE_DATA
        WHERE DEP_NAME IN ('롯데백화점_본점', '신세계_강남', '더현대서울')
        """
        try:
            self.dep_data = pd.read_sql(query_dep, self.conn)
            print(f"Loaded {len(self.dep_data)} rows from DEP_STORE_DATA.") # 로드된 행 수 로그
        except Exception as e:
             print(f"Error loading DEP_STORE_DATA: {e}")
             st.error(f"백화점 방문 데이터 로딩 실패: {e}")
             self.dep_data = pd.DataFrame()

        # 카드 소비 데이터 로드
        query_sales = """
        SELECT AGE_GROUP, GENDER, TIME_SLOT, WEEKDAY_WEEKEND, LIFESTYLE, CARD_TYPE, DEPARTMENT_STORE_SALES
        FROM SALES_KOR_LABELING
        WHERE DISTRICT_NAME IN ('여의도동', '소공동', '반포동')
        """
        try:
            self.sales_data = pd.read_sql(query_sales, self.conn)
            print(f"Loaded {len(self.sales_data)} rows from SALES_KOR_LABELING.") # 로드된 행 수 로그
        except Exception as e:
            print(f"Error loading SALES_KOR_LABELING: {e}")
            st.error(f"카드 소비 데이터 로딩 실패: {e}")
            self.sales_data = pd.DataFrame()

        # 데이터 로드 후 연결 종료는 __init__의 finally 블록으로 이동
        # self.conn.close()

    def _train_models(self):
        # 데이터 유효성 검사
        if self.dep_data.empty or self.sales_data.empty:
            print("Error: Data loading failed or returned empty dataframes. Cannot train models.")
            # st.warning 메시지는 __init__ 에서 출력하므로 여기선 print만 유지
            return # 여기서 함수 종료 시 is_initialized = False 유지됨

        print("Training ML models...") # 학습 시작 로그
        # 백화점 방문 예측 모델 학습
        # 범주형 변수 인코딩 (LabelEncoder 사용)
        store_features = self.dep_data[['AGE_GROUP', 'GENDER', 'TIME_SLOT', 'WEEKDAY_WEEKEND', 'LIFESTYLE']].copy()
        encoders = {}
        for col in store_features.columns:
            le = LabelEncoder()
            store_features[col] = le.fit_transform(store_features[col])
            encoders[col] = le # 나중에 예측 시 사용하기 위해 인코더 저장
        self.store_encoders = encoders

        y_store = self.dep_data['DEP_NAME'].map({
            '롯데백화점_본점': '롯데백화점',
            '신세계_강남': '신세계백화점',
            '더현대서울': '현대백화점'
        })
        self.store_model.fit(store_features, y_store)

        # 지출 예측 모델 학습
        spending_features = self.sales_data[['AGE_GROUP', 'GENDER', 'TIME_SLOT', 'WEEKDAY_WEEKEND', 'LIFESTYLE', 'CARD_TYPE']].copy()
        encoders = {}
        for col in spending_features.columns:
            le = LabelEncoder()
            spending_features[col] = le.fit_transform(spending_features[col])
            encoders[col] = le
        self.spending_encoders = encoders

        y_spend = self.sales_data['DEPARTMENT_STORE_SALES']
        # NaN 또는 무한대 값 처리 (예: 0으로 대체)
        y_spend = y_spend.fillna(0).replace([np.inf, -np.inf], 0)
        self.spending_model.fit(spending_features, y_spend)

        print("ML models trained successfully.") # 학습 완료 로그

    def predict(self, user_input):
        # 예측 전 초기화 상태 확인
        if not self.is_initialized:
            st.error("ML 모델이 초기화되지 않아 예측을 수행할 수 없습니다. Snowflake 연결 또는 데이터 로딩/학습 과정을 확인하세요.")
            return {"store_predictions": {}, "spending": 0} # 기본값 반환

        # 입력 데이터 전처리
        processed_input_store, processed_input_spending = self._preprocess_input(user_input)

        # 백화점 방문 예측
        store_probs = self.store_model.predict_proba([processed_input_store])[0]
        store_predictions = dict(zip(self.store_model.classes_, store_probs))

        # 지출 예측
        spending = self.spending_model.predict([processed_input_spending])[0]

        return {
            "store_predictions": store_predictions,
            "spending": max(0, int(spending)) # 음수 값 방지
        }

    def _preprocess_input(self, user_input):
        # 예측 전 초기화 상태 재확인 (이론상 predict에서 걸러지지만 안전 장치)
        if not self.is_initialized:
            raise AttributeError("Model is not initialized, cannot preprocess input.")

        # 입력 데이터를 모델이 이해할 수 있는 형태로 변환
        # 순서는 _train_models 에서 사용된 특성 순서와 일치해야 함

        # 백화점 방문 예측용 특성
        store_feature_values = [
            user_input["age"],
            user_input["gender"],
            "00~06", # 임시값 또는 사용자 입력 추가 필요 (TIME_SLOT)
            "주중",   # 임시값 또는 사용자 입력 추가 필요 (WEEKDAY_WEEKEND)
            user_input["type"] # 고객 형태를 라이프스타일로 사용 (가정)
        ]
        processed_store = []
        store_cols = ['AGE_GROUP', 'GENDER', 'TIME_SLOT', 'WEEKDAY_WEEKEND', 'LIFESTYLE']
        for i, col in enumerate(store_cols):
            try:
                # 학습 시 사용된 인코더로 변환
                processed_store.append(self.store_encoders[col].transform([store_feature_values[i]])[0])
            except ValueError:
                # 모르는 값(새로운 카테고리) 처리: 예를 들어 0 또는 다른 대표값 할당
                # 또는 에러 발생시키기: st.error(f"Unknown value '{store_feature_values[i]}' for feature '{col}'")
                print(f"Warning: Unknown value '{store_feature_values[i]}' for store feature '{col}'. Using 0.")
                processed_store.append(0)
            except KeyError:
                # 인코더 자체가 없는 경우 (학습 실패 시 발생 가능)
                print(f"Error: Encoder for store feature '{col}' not found. Check model training.")
                st.error(f"ML 모델 오류: '{col}' 특징에 대한 인코더를 찾을 수 없습니다.")
                # 이 경우 예측 중단 또는 기본값 사용
                processed_store.append(0) # 예시: 기본값 사용

        # 지출 예측용 특성
        spending_feature_values = [
            user_input["age"],
            user_input["gender"],
            "00~06", # 임시값
            "주중",   # 임시값
            user_input["type"], # 고객 형태를 라이프스타일로 사용 (가정)
            1        # 임시값 또는 사용자 입력 추가 필요 (CARD_TYPE, 예: 개인=1)
        ]
        processed_spending = []
        spending_cols = ['AGE_GROUP', 'GENDER', 'TIME_SLOT', 'WEEKDAY_WEEKEND', 'LIFESTYLE', 'CARD_TYPE']
        for i, col in enumerate(spending_cols):
            try:
                processed_spending.append(self.spending_encoders[col].transform([spending_feature_values[i]])[0])
            except ValueError:
                print(f"Warning: Unknown value '{spending_feature_values[i]}' for spending feature '{col}'. Using 0.")
                processed_spending.append(0)
            except KeyError:
                print(f"Error: Encoder for spending feature '{col}' not found. Check model training.")
                st.error(f"ML 모델 오류: '{col}' 특징에 대한 인코더를 찾을 수 없습니다.")
                processed_spending.append(0)

        return processed_store, processed_spending 