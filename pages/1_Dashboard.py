import streamlit as st 
import plotly.express as px 
from src.database import fetch_all_leads 

st.set_page_config(page_title="Orion Dashboard", layout="wide")

st.title("📊 Orion Command Center")

df = fetch_all_leads()

if not df.empty:
    # KPI CARDS 
    total_leads = len(df)
    new_leads = len(df[df['status'] == 'new'])
    conversion_rate = round((len(df[df['status'] == 'qualified']) / total_leads) * 100, 1) if total_leads > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Leads", total_leads, "+2 today")
    col2.metric("New Opportunities", new_leads, "Active")
    col3.metric("Conversion Rate", f"{conversion_rate}%", "On Target")
    col4.metric("Revenue Pipeline", "$12,500", "+$2k")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Leads by Status")
        # Beautiful Donut Chart
        fig_status = px.pie(df, names='status', hole=0.4,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_status, use_container_width=True)

    with col_right:
        st.subheader("Lead Sources")
        if 'source' in df.columns:
            source_counts = df['source'].value_counts().reset_index()
            source_counts.columns = ['source', 'count']
            fig_source = px.bar(source_counts, x='source', y='count', color='source')
            st.plotly_chart(fig_source, use_container_width=True)
        else:
            st.warning("Source data missing.")

else: 
    st.info("System Standby.No data detected in the Orion Mainframe.")
