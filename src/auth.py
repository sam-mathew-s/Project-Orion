import streamlit as st 
import os 

def require_auth():
    if "user" in st.session_state:
        return True 

    st.markdown("## Orion Security Gate")

    email = st.text_input("Enter Corporate Email", key="auth_email_input")
    password = st.text_input("Enter Password", type="password", key="auth_pass_input")

    if st.button("Log In", key="auth_login_btn"):
        if "@" in email and len(password) > 0:
            st.session_state["user"] = {
                "email": email,
                "role": "admin",
                "org_id": "org_default_123"
            }
            st.success("Access Granted.")
            st.rerun()
        else:
            st.error("Invalid Credentials.")
    return False
    