import streamlit as st
import pandas as pd

st.title("🏠 APT 리스트 조회")

SHEET_ID = "15XH4DNItLzCFLQgqvY7gr8cD1N1HPAoQlGlSN-05jxw"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

df = pd.read_csv(url)

# 🔍 검색
query = st.text_input("🔍 검색")

if query:
    df = df[df.astype(str).apply(lambda row: row.str.contains(query, case=False).any(), axis=1)]

# 📊 표 (이미지 컬럼 제외)
hide_cols = ["네이버부동산", "네이버지도"]
show_df = df.drop(columns=[col for col in hide_cols if col in df.columns])

st.dataframe(show_df, use_container_width=True)

# 🔗 네이버 링크
if "네이버부동산 링크" in df.columns:
    st.subheader("🔗 네이버 바로가기")

    for _, row in df.iterrows():
        if pd.notna(row["네이버부동산 링크"]):
            st.markdown(f"[{row.get('아파트명','아파트')} 보러가기]({row['네이버부동산 링크']})")

# 📥 다운로드
st.download_button(
    "📥 엑셀 다운로드",
    df.to_csv(index=False).encode('utf-8'),
    "apt.csv",
    "text/csv"
)
