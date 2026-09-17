import streamlit as st

# ✅ Hardcoded users
users = {
    "admin": "1234",
    "teacher1": "pass123",
    "staff1": "abc123"
}

def login():

    st.markdown("<h1 style='text-align: center;'>🔐 Staff Login</h1>", unsafe_allow_html=True)

    # 👇 Create center column
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:  # ✅ center column

        staff_id = st.text_input("👤 Staff ID")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login", use_container_width=True):

            if staff_id in users:
                if users[staff_id] == password:

                    st.success("✅ Login Successful")

                    st.session_state["logged_in"] = True
                    st.session_state["staff_id"] = staff_id

                    st.rerun()

                else:
                    st.error("❌ Wrong Password")
            else:
                st.error("❌ Staff ID not found")