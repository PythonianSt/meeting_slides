from pathlib import Path

import streamlit as st
from PIL import Image


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="สไลด์การประชุม",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------
SLIDE_FOLDER = Path("slides")
TOTAL_SLIDES = 8


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        /* ลดระยะว่างด้านบน */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }

        /* หัวข้อ */
        .meeting-title {
            text-align: center;
            font-size: 1.55rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .meeting-subtitle {
            text-align: center;
            color: #666666;
            font-size: 0.95rem;
            margin-bottom: 0.8rem;
        }

        /* แสดงหมายเลขหน้า */
        .slide-number {
            text-align: center;
            font-size: 1.1rem;
            font-weight: 700;
            padding: 0.35rem;
            margin-bottom: 0.4rem;
        }

        /* ปุ่มให้เหมาะกับมือถือ */
        div.stButton > button {
            width: 100%;
            min-height: 3rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 12px;
        }

        /* Slider */
        div[data-testid="stSlider"] {
            padding-left: 0.3rem;
            padding-right: 0.3rem;
        }

        /* ซ่อนเมนูบางส่วน */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "slide_number" not in st.session_state:
    st.session_state.slide_number = 1


def previous_slide():
    """เลื่อนไปยังสไลด์ก่อนหน้า"""
    if st.session_state.slide_number > 1:
        st.session_state.slide_number -= 1


def next_slide():
    """เลื่อนไปยังสไลด์ถัดไป"""
    if st.session_state.slide_number < TOTAL_SLIDES:
        st.session_state.slide_number += 1


def update_from_slider():
    """อัปเดตหมายเลขสไลด์จาก Slider"""
    st.session_state.slide_number = st.session_state.slide_slider


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    '<div class="meeting-title">📱 สไลด์การประชุม</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="meeting-subtitle">'
    'เลื่อนหมายเลขให้ตรงกับหน้าที่กำลังอภิปราย'
    "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SLIDER
# ---------------------------------------------------------
st.slider(
    "เลือกหมายเลขสไลด์",
    min_value=1,
    max_value=TOTAL_SLIDES,
    value=st.session_state.slide_number,
    step=1,
    key="slide_slider",
    on_change=update_from_slider,
)


# ---------------------------------------------------------
# PREVIOUS / CURRENT / NEXT BUTTONS
# ---------------------------------------------------------
previous_col, current_col, next_col = st.columns([1, 1.2, 1])

with previous_col:
    st.button(
        "◀ ก่อนหน้า",
        on_click=previous_slide,
        disabled=st.session_state.slide_number <= 1,
        use_container_width=True,
    )

with current_col:
    st.markdown(
        f'<div class="slide-number">'
        f'หน้า {st.session_state.slide_number} / {TOTAL_SLIDES}'
        f"</div>",
        unsafe_allow_html=True,
    )

with next_col:
    st.button(
        "ถัดไป ▶",
        on_click=next_slide,
        disabled=st.session_state.slide_number >= TOTAL_SLIDES,
        use_container_width=True,
    )


# ---------------------------------------------------------
# DISPLAY CURRENT SLIDE
# ---------------------------------------------------------
slide_filename = f"slide{st.session_state.slide_number:02d}.png"
slide_path = SLIDE_FOLDER / slide_filename

if slide_path.exists():
    try:
        slide_image = Image.open(slide_path)

        st.image(
            slide_image,
            caption=f"สไลด์ที่ {st.session_state.slide_number}",
            use_container_width=True,
        )

    except Exception as error:
        st.error(f"ไม่สามารถเปิดไฟล์ {slide_filename} ได้")
        st.code(str(error))

else:
    st.warning(
        f"ไม่พบไฟล์ `{slide_path}`\n\n"
        f"โปรดตรวจสอบว่ามีไฟล์ชื่อ `{slide_filename}` "
        "อยู่ในโฟลเดอร์ `slides`"
    )


# ---------------------------------------------------------
# LOWER NAVIGATION
# ช่วยให้ผู้ใช้ไม่ต้องเลื่อนกลับไปด้านบนเมื่อดูสไลด์ยาว
# ---------------------------------------------------------
st.divider()

lower_previous_col, lower_home_col, lower_next_col = st.columns(3)

with lower_previous_col:
    st.button(
        "◀ หน้าก่อน",
        key="lower_previous",
        on_click=previous_slide,
        disabled=st.session_state.slide_number <= 1,
        use_container_width=True,
    )

with lower_home_col:
    if st.button(
        "หน้าแรก",
        key="go_to_first",
        use_container_width=True,
    ):
        st.session_state.slide_number = 1
        st.rerun()

with lower_next_col:
    st.button(
        "หน้าถัดไป ▶",
        key="lower_next",
        on_click=next_slide,
        disabled=st.session_state.slide_number >= TOTAL_SLIDES,
        use_container_width=True,
    )


# ---------------------------------------------------------
# INSTRUCTIONS
# ---------------------------------------------------------
with st.expander("วิธีใช้งาน"):
    st.markdown(
        """
1. สแกน QR code เพื่อเปิดหน้าเว็บนี้
2. ฟังหมายเลขสไลด์จากผู้นำเสนอ
3. เลื่อน Slider ไปยังหมายเลขเดียวกัน
4. สามารถกด **ก่อนหน้า** หรือ **ถัดไป** เพื่อทบทวนได้
5. ผู้เข้าประชุมแต่ละคนสามารถควบคุมหน้าสไลด์ของตนเอง
        """
    )
