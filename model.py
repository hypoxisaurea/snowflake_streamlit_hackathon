import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

class DepartmentStorePredictor:
    def __init__(self):
        # 백화점 목록
        self.stores = ["롯데백화점", "신세계백화점", "현대백화점"]
        
        # 모델 초기화
        self.store_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.spending_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # 간단한 학습 데이터 생성 (실제로는 더 복잡한 데이터셋 사용 필요)
        self._train_models()
    
    def _train_models(self):
        # 예시 데이터 생성
        X = np.random.rand(1000, 6)  # 6개 특성
        store_y = np.random.choice(self.stores, 1000)
        spending_y = np.random.uniform(10000, 1000000, 1000)
        
        # 모델 학습
        self.store_model.fit(X, store_y)
        self.spending_model.fit(X, spending_y)
    
    def predict(self, user_input):
        # 입력 데이터 전처리
        features = self._preprocess_input(user_input)
        
        # 예측
        predicted_store = self.store_model.predict([features])[0]
        predicted_spending = self.spending_model.predict([features])[0]
        
        return {
            "store": predicted_store,
            "spending": int(predicted_spending)
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
        
        # 날씨 (맑음: 0, 흐림: 1, 비: 2, 눈: 3)
        weather_map = {"맑음": 0, "흐림": 1, "비": 2, "눈": 3}
        features.append(weather_map[user_input["weather"]])
        
        # 계절 (1-12월)
        features.append(user_input["season"] / 12)  # 정규화
        
        return features
