import os
import streamlit as st
import snowflake.connector
from dotenv import load_dotenv

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    account=os.getenv("DB_ACCOUNT"),
    warehouse=os.getenv("DB_WAREHOUSE"),
    database=os.getenv("DB_DATABASE"),
    schema=os.getenv("DB_SCHEMA"),
    role=os.getenv("DB_ROLE"),
)

# # data loading
# query = "SELECT * FROM DEP_STORE_DATA;"
# department_store_df = pd.read_sql(query, conn)

# # data preprocessing
# department_store_df['DEP_NAME'] = department_store_df['DEP_NAME'].replace({
#     '더현대서울': 'HYUNDAI',
#     '신세계_강남': 'SSG',
#     '롯데백화점_본점': 'LOTTE',
# })
# department_store_df['DATE_KST'] = pd.to_datetime(department_store_df['DATE_KST'])
# department_store_grouped = department_store_df.groupby(['DATE_KST', 'DEP_NAME'])['COUNT'].sum().reset_index()
# department_store_df = department_store_grouped.pivot(index='DATE_KST', columns='DEP_NAME', values='COUNT').reset_index()


# # data loading
# query = "SELECT * FROM SEOUL_WEATHER_DATA;"
# weather_df = pd.read_sql(query, conn)

# # data preprocessing
# weather_df = weather_df.drop(columns=['CITY'])
# weather_df['DATE_KST'] = pd.to_datetime(weather_df['DATE_KST'])

# data loading
query = "SELECT * FROM CARD_REGION_DATA;"
card_df = pd.read_sql(query, conn)

# data merging
# merge_df = pd.merge(department_store_df, weather_df, on='DATE_KST', how='inner')
# merge_df['TOTAL_COUNT'] = department_store_df.drop(columns=['DATE_KST']).sum(axis=1)

# merge_df['seasons'] = merge_df['DATE_KST'].dt.month.apply(
#     lambda x: 'WINTER' if x in [12, 1, 2] else
#         'SPRING' if x in [3, 4, 5] else
#         'SUMMER' if x in [6, 7, 8] else
#         'AUTUMN'
# )

# merge_df['weekday'] = merge_df['DATE_KST'].dt.dayofweek  # 0:월 ~ 6:일



# correlation analysis
# season_dummies = pd.get_dummies(merge_df['seasons'])
# numeric_df = pd.concat([merge_df.select_dtypes(include='number'), season_dummies], axis=1)
# correlation_matrix = numeric_df.corr()

# st.subheader("백화점 방문 수와 날씨의 상관관계 히트맵")
# fig, ax = plt.subplots(figsize=(10, 8))
# sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
# st.pyplot(fig)


# # data visualization
# st.dataframe(merge_df.set_index('DATE_KST'))
st.dataframe(card_df)
