import streamlit as st
import pandas as pd

st.title("🏠 APT 리스트 조회")

# 👉 네 구글시트 ID
SHEET_ID = "15XH4DNItLzCFLQgqvY7gr8cD1N1HPAoQlGlSN-05jxw"

# 👉 CSV URL
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 👉 데이터 불러오기
df = pd.read_csv(url)

# 👉 검색 기능
query = st.text_input("검색")

if query:
    df = df[df.astype(str).apply(lambda row: row.str.contains(query, case=False).any(), axis=1)]

# 👉 표 출력
st.dataframe(df, use_container_width=True)

# 👉 이미지 컬럼 있으면 출력
if "이미지" in df.columns:
    st.subheader("이미지")

    for i, row in df.iterrows():
        if pd.notna(row["이미지"]):
            st.markdown(f"**{row.get('아파트','')}**")
            st.image(row["이미지"], width=300)

# 👉 다운로드
st.download_button(
    "엑셀 다운로드",
    df.to_csv(index=False).encode('utf-8'),
    "apt.csv",
    "text/csv"
)
