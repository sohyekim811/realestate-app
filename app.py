import streamlit as st
import pandas as pd

st.title("🏠 APT 리스트 조회")

# 👉 여기에 네 시트 ID 넣기
SHEET_ID = "여기에_ID붙여넣기"

url = f"https://docs.google.com/spreadsheets/d/15XH4DNItLzCFLQgqvY7gr8cD1N1HPAoQlGlSN-05jxw/export?format=csv"

df = pd.read_csv(url)

query = st.text_input("검색")

if query:
    df = df[df.astype(str).apply(lambda row: row.str.contains(query, case=False).any(), axis=1)]

st.dataframe(df)

st.download_button(
    "엑셀 다운로드",
    df.to_csv(index=False).encode('utf-8'),
    "apt.csv",
    "text/csv"
)
