import streamlit as st

# ✅ MUST BE FIRST
st.set_page_config(
    page_title="Student Performance System",
    layout="wide"
)

from auth import login
import marksheet
import attendance

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False


# ---------------- DARK MODE STYLE ----------------
def apply_theme():
    if st.session_state["dark_mode"]:
        st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        section[data-testid="stSidebar"] {
            background-color: #161A23;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #F5F7FA;
        }
        </style>
        """, unsafe_allow_html=True)


# ---------------- LOGIN ----------------
if not st.session_state["logged_in"]:
    login()

# ---------------- MAIN APP ----------------
else:
    apply_theme()

    # SIDEBAR
    with st.sidebar:
        st.markdown("## 🎓 Dashboard")
        st.write(f"👤 **{st.session_state['staff_id']}**")

        st.session_state["dark_mode"] = st.toggle(
            "🌙 Dark Mode",
            value=st.session_state["dark_mode"]
        )

        st.markdown("---")

        menu = st.radio("Select Module", [
            "Marksheet",
            "Attendance"
        ])

    # MAIN HEADER
    st.markdown("""
        <h1 style='text-align: center; color: #4A90E2;'>
        📊 Student Performance System
        </h1>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # MODULE NAVIGATION
    if menu == "Marksheet":
        marksheet.run()

    elif menu == "Attendance":
        attendance.run()