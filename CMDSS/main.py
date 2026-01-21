import streamlit as st
from utils.db_handler import verify_owner

st.set_page_config(page_title="Smart Canteen AI", layout="centered")

def login():
    st.title("🍽 Smart Canteen Management System")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if verify_owner(username, password):
            st.session_state["owner_id"] = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

def main():
    if "owner_id" not in st.session_state:
        login()
    else:
        st.sidebar.success(f"Logged in as {st.session_state['owner_id']}")
        st.sidebar.info("Use sidebar to navigate")

if __name__ == "__main__":
    main()
