import streamlit as st
import pandas as pd

st.title("🏠 부동산 정리")

name = st.text_input("아파트명")
price = st.text_input("가격")
addr = st.text_input("주소")

if "data" not in st.session_state:
    st.session_state.data = []

if st.button("추가"):
    st.session_state.data.append({
        "아파트": name,
        "가격": price,
        "주소": addr
    })

df = pd.DataFrame(st.session_state.data)
st.dataframe(df)

if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("엑셀 다운로드", csv, "realestate.csv", "text/csv")
