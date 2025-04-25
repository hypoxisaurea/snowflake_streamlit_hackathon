import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import snowflake.connector
import os
from dotenv import load_dotenv

class DepartmentStorePredictor:
    def __init__(self):
        # Snowflake 연결 설정
        load_dotenv()
        self.conn = snowflake.connector.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            account=os.getenv("DB_ACCOUNT"),
            warehouse=os.getenv("DB_WAREHOUSE"),
            database=os.getenv("DB_DATABASE"),
            schema=os.getenv("DB_SCHEMA"),
            role=os.getenv("DB_ROLE"),
        )

        # 백화점 목록
        self.stores = ["롯데백화점", "신세계백화점", "현대백화점"]

        # 모델 초기화
        self.store_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.spending_model = RandomForestRegressor(n_estimators=100, random_state=42)

        # 데이터 로드 및 모델 학습 (오류 발생 시 예외 처리 추가)
        try:
            self._load_data()
            self._train_models()
        except Exception as e:
            print(f"Error during model initialization: {e}")
            # 필요한 경우, 여기서 기본 모델을 로드하거나 오류 상태를 설정할 수 있습니다.
            # 예: self.initialized_successfully = False

    def _load_data(self):
        # 백화점 방문 데이터 로드
        query = """
        SELECT AGE_GROUP, GENDER, TIME_SLOT, WEEKDAY_WEEKEND, LIFESTYLE, DEP_NAME
        FROM DEP_STORE_DATA
        WHERE DEP_NAME IN ('롯데백화점_본점', '신세계_강남', '더현대서울')
        """
        self.dep_data = pd.read_sql(query, self.conn)

        # 카드 소비 데이터 로드
        query = """
        SELECT AGE_GROUP, GENDER, TIME_SLOT, WEEKDAY_WEEKEND, LIFESTYLE, CARD_TYPE, DEPARTMENT_STORE_SALES
        FROM SALES_KOR_LABELING
        WHERE DISTRICT_NAME IN ('여의도동', '소공동', '반포동')
        """
        self.sales_data = pd.read_sql(query, self.conn)
        self.conn.close() # 데이터 로드 후 연결 종료

    def _train_models(self):
        # 데이터 유효성 검사
        if self.dep_data.empty or self.sales_data.empty:
            print("Error: Data loading failed or returned empty dataframes. Cannot train models.")
            return

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


    def predict(self, user_input):
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
                # 학습 시 사용된 인코더로 변환, 모르는 값은 0 등으로 처리
                processed_store.append(self.store_encoders[col].transform([store_feature_values[i]])[0])
            except ValueError:
                 processed_store.append(0) # 또는 다른 기본값

        # 지출 예측용 특성
        spending_feature_values = [
            user_input["age"],
            user_input["gender"],
            "00~06", # 임시값 또는 사용자 입력 추가 필요 (TIME_SLOT)
            "주중",   # 임시값 또는 사용자 입력 추가 필요 (WEEKDAY_WEEKEND)
            user_input["type"], # 고객 형태를 라이프스타일로 사용 (가정)
            1        # 임시값 또는 사용자 입력 추가 필요 (CARD_TYPE, 예: 개인=1)
        ]
        processed_spending = []
        spending_cols = ['AGE_GROUP', 'GENDER', 'TIME_SLOT', 'WEEKDAY_WEEKEND', 'LIFESTYLE', 'CARD_TYPE']
        for i, col in enumerate(spending_cols):
             try:
                processed_spending.append(self.spending_encoders[col].transform([spending_feature_values[i]])[0])
             except ValueError:
                 processed_spending.append(0)

        return processed_store, processed_spending 