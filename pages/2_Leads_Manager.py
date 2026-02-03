import streamlit as st 
from src.database import fetch_all_leads

st.set_page_config(page_title="Leads Manager", layout="wide")

st.title("🚀 Orion Leads Manager")

# Fetch data
with st.spinner("Talking to the database..."):
    df_leads = fetch_all_leads()

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Leads", len(df_leads))
col2.metric("New Leads", len(df_leads[df_leads['status']=='new']))
col3.metric("Qualified", len(df_leads[df_leads['status']=='qualified']))

# Show the table
st.markdown("### Database Records")
st.dataframe(df_leads, use_container_width=True)


