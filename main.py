import streamlit as st 
from src.auth import require_auth

st.set_page_config(page_title="Orion CRM", layout="wide")

if not require_auth():
    st.stop()

user = st.session_state["user"]

st.sidebar.title(f"🙍‍♂️ {user['email']}")
st.sidebar.markdown(f"**Role:** {user['role'].upper()}")
st.sidebar.divider()

st.sidebar.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
st.sidebar.page_link("pages/2_Leads_Manager.py", label="🚀 Leads Manager")
st.sidebar.page_link("pages/3_AI_Assistant.py", label="🤖 AI Architech")

st.title("Orion Enterprise System")
st.write(f"Welcome back, Commander. Connected to Organization: '{user['org_id']}'")
