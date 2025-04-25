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
        
        # 데이터 로드 및 모델 학습
        self._load_data()
        self._train_models()
    
    def _load_data(self):
        # 백화점 방문 데이터 로드
        query = """
        SELECT * FROM DEP_STORE_DATA
        WHERE DEP_NAME IN ('롯데백화점_본점', '신세계_강남', '더현대서울')
        """
        self.dep_data = pd.read_sql(query, self.conn)
        
        # 카드 소비 데이터 로드
        query = """
        SELECT * FROM SALES_KOR_LABELING
        WHERE DISTRICT_NAME IN ('여의도동', '소공동', '반포동')
        """
        self.sales_data = pd.read_sql(query, self.conn)
    
    def _train_models(self):
        # 백화점 방문 예측을 위한 특성 추출
        X_store = self._extract_store_features()
        y_store = self.dep_data['DEP_NAME'].map({
            '롯데백화점_본점': '롯데백화점',
            '신세계_강남': '신세계백화점',
            '더현대서울': '현대백화점'
        })
        
        # 지출 예측을 위한 특성 추출
        X_spend = self._extract_spending_features()
        y_spend = self.sales_data['DEPARTMENT_STORE_SALES']
        
        # 모델 학습
        self.store_model.fit(X_store, y_store)
        self.spending_model.fit(X_spend, y_spend)
    
    def _extract_store_features(self):
        # 백화점 방문 예측을 위한 특성 추출
        features = pd.DataFrame()
        
        # 시간대별 방문 빈도
        features['time_slot'] = self.dep_data['TIME_SLOT']
        
        # 요일별 방문 빈도
        features['weekday'] = self.dep_data['WEEKDAY_WEEKEND']
        
        # 성별
        features['gender'] = self.dep_data['GENDER']
        
        # 연령대
        features['age_group'] = self.dep_data['AGE_GROUP']
        
        # 라이프스타일
        features['lifestyle'] = self.dep_data['LIFESTYLE']
        
        return features
    
    def _extract_spending_features(self):
        # 지출 예측을 위한 특성 추출
        features = pd.DataFrame()
        
        # 카드 타입
        features['card_type'] = self.sales_data['CARD_TYPE']
        
        # 요일
        features['weekday'] = self.sales_data['WEEKDAY_WEEKEND']
        
        # 성별
        features['gender'] = self.sales_data['GENDER']
        
        # 연령대
        features['age_group'] = self.sales_data['AGE_GROUP']
        
        # 라이프스타일
        features['lifestyle'] = self.sales_data['LIFESTYLE']
        
        # 시간대
        features['time_slot'] = self.sales_data['TIME_SLOT']
        
        return features
    
    def predict(self, user_input):
        # 입력 데이터 전처리
        features = self._preprocess_input(user_input)
        
        # 백화점 방문 예측
        store_probs = self.store_model.predict_proba([features])[0]
        store_predictions = dict(zip(self.stores, store_probs))
        
        # 지출 예측
        spending = self.spending_model.predict([features])[0]
        
        return {
            "store_predictions": store_predictions,
            "spending": int(spending)
        }
    
    def _preprocess_input(self, user_input):
        # 입력 데이터를 모델이 이해할 수 있는 형태로 변환
        features = []
        
        # 성별 (남성: 0, 여성: 1)
        features.append(1 if user_input["gender"] == "여성" else 0)
        
        # 연령대 (20대: 0, 30대: 1, 40대: 2, 50대 이상: 3)
        age_map = {"20대": 0, "30대": 1, "40대": 2, "50대 이상": 3}
        features.append(age_map[user_input["age"]])
        
        # 거주지 (여의도동: 0, 소공동: 1, 반포동: 2)
        residence_map = {"여의도동": 0, "소공동": 1, "반포동": 2}
        features.append(residence_map[user_input["residence"]])
        
        # 직장 위치 (여의도동: 0, 소공동: 1, 반포동: 2)
        work_map = {"여의도동": 0, "소공동": 1, "반포동": 2}
        features.append(work_map[user_input["work"]])
        
        # 고객 형태 (싱글: 0, 신혼부부: 1, 영유아가족: 2, 청소년가족: 3, 성인자녀가족: 4, 실버: 5)
        type_map = {
            "싱글": 0, "신혼부부": 1, "영유아가족": 2,
            "청소년가족": 3, "성인자녀가족": 4, "실버": 5
        }
        features.append(type_map[user_input["type"]])
        
        return features
