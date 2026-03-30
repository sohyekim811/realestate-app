import streamlit as st
import pandas as pd

st.title("🏠 APT 리스트 조회")

SHEET_ID = "15XH4DNItLzCFLQgqvY7gr8cD1N1HPAoQlGlSN-05jxw"

url = f"https://docs.google.com/spreadsheets/d/15XH4DNItLzCFLQgqvY7gr8cD1N1HPAoQlGlSN-05jxw/export?format=csv"
df = pd.read_csv(url)

query = st.text_input("검색")

if query:
    df = df[df.astype(str).apply(lambda row: row.str.contains(query, case=False).any(), axis=1)]

st.dataframe(df)

# 🔥 이미지 출력
if "이미지" in df.columns:
    st.subheader("이미지 보기")

    for i, row in df.iterrows():
        if pd.notna(row["이미지"]):
            st.markdown(f"**{row.get('아파트','')}**")
            st.image(row["이미지"], width=300)
