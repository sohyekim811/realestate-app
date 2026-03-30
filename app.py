from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

EXCEL = Path(__file__).resolve().parent / "APT리스트.xlsx"


@st.cache_data(show_spinner=False)
def cached_row_images(cache_key: tuple, data_bytes: bytes, sheet_name: str, hdr: int) -> dict:
    src: Path | bytes = data_bytes if cache_key[0] == "upload" else EXCEL
    return extract_row_images(src, sheet_name, hdr)


def sanitize_sheet_name(name: str) -> str:
    bad = r"[]:*?/\\"
    s = "".join("_" if c in bad else c for c in str(name))[:31]
    return s or "Sheet1"


st.set_page_config(page_title="APT 리스트", layout="wide")
st.title("APT 리스트 조회")
st.sidebar.caption(
    "Cloud: 엑셀 업로드 · 로컬: `APT리스트.xlsx` 자동 · 브라우저: **http://127.0.0.1:8501**"
)

uploaded = st.sidebar.file_uploader(
    "엑셀 (.xlsx) 업로드",
    type=["xlsx"],
    help="배포(Cloud) 시 여기서 파일 선택. PC에 APT리스트.xlsx가 있으면 비워 두어도 됩니다.",
)

if uploaded is not None:
    data_bytes = uploaded.getvalue()
    cache_key: tuple = ("upload", hash(data_bytes))
elif EXCEL.exists():
    data_bytes = EXCEL.read_bytes()
    cache_key = ("local", EXCEL.stat().st_mtime)
else:
    data_bytes = None
    cache_key = ("none", 0)

if data_bytes is None:
    st.error(
        f"엑셀 파일이 필요합니다.\n\n"
        f"- **이 PC:** `{EXCEL.name}` 을 이 앱과 **같은 폴더**에 두거나  \n"
        f"- **어디서나:** 왼쪽 **엑셀 업로드**에서 `.xlsx` 선택"
    )
    st.stop()

xl = pd.ExcelFile(BytesIO(data_bytes))

if st.sidebar.button("데이터 새로고침 (파일 바꾼 뒤)"):
    st.cache_data.clear()
    st.rerun()

sheet = st.sidebar.selectbox("시트 선택", xl.sheet_names, index=min(1, len(xl.sheet_names) - 1))
header_row = st.sidebar.radio(
    "컬럼 제목(헤더) 행",
    ["1행", "2행"],
    index=0,
    horizontal=True,
    help="표가 한 줄 아래로 밀려 있으면 '2행'을 선택하세요.",
)
header = 0 if header_row == "1행" else 1


@st.cache_data(show_spinner=True)
def load(cache_key: tuple, data_bytes: bytes, sheet_name: str, hdr: int) -> pd.DataFrame:
    _ = cache_key
    return pd.read_excel(BytesIO(data_bytes), sheet_name=sheet_name, header=hdr)


df = load(cache_key, data_bytes, sheet, header)

query = st.sidebar.text_input("검색 (입력한 글자가 들어간 셀만)", "")
if query.strip():
    q = query.strip()
    mask = df.astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
    df = df[mask]
    st.caption(f"검색 결과: **{len(df)}**행 (전체에서 필터)")

st.dataframe(df, use_container_width=True, height=min(720, 42 + 35 * (len(df) + 1)))



buf = BytesIO()
out_name = sanitize_sheet_name(sheet)
with pd.ExcelWriter(buf, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name=out_name)
excel_bytes = buf.getvalue()

st.download_button(
    label="현재 화면(필터 적용) 엑셀 다운로드",
    data=excel_bytes,
    file_name="APT_조회결과.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

src_note = "업로드한 파일" if cache_key[0] == "upload" else f"`{EXCEL.name}`"
st.caption(f"원본: {src_note} · 다운로드는 위 표와 동일(검색 시 필터 반영).")
