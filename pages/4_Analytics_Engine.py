import streamlit as st 
import pandas as pd 
import plotly.express as px 
from src.database import fetch_all_leads 

# PAGE CONFIGURATION
st.set_page_config(page_title="Analytics Engine", layout="wide")
st.title("📊 Orion Analytics Command")

# LOAD DATA 
with st.spinner("Crunching Numbers..."):
    df = fetch_all_leads()

# DASHBOARD LOGIC
if not df.empty:
    if "status" not in df.columns:
        df["status"] = "new"

    total_leads = len(df)
    hot_leads = len(df[df["status"] == "hot"])
    converted = len(df[df["status"] == "converted"])
    pipeline_value = total_leads * 5000 

    # --- ROW 1: THE HEAD UP DISPLAY (KPIs) ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Targets", total_leads, delta="Active")
    c2.metric("Hot Leads", hot_leads, delta_color="normal")
    c3.metric("Converted", converted, delta_color="inverse")
    c4.metric("Pipeline Value", f"${pipeline_value:,}","Estimated")

    st.markdown("---")

    # === ROW 2: STRATEGIC CHART ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🎯 Acquistion Channels")
        # PIE CHART: Where are leads coming from?
        fig_source = px.pie(df, names='source', title='Leads by Source', hole=0.4)
        st.plotly_chart(fig_source, use_container_width=True)

    with col_right:
        st.subheader("🏢 Target Density")
        # BAR CHART: Which companies are we targeting?
        company_counts = df['company'].value_counts().reset_index()
        company_counts.columns = ['company', 'count']
        fig_company = px.bar(company_counts, x='company', y='count', title='Leads per Company', color ='count')
        st.plotly_chart(fig_company, use_container_width=True)

    # --- ROW 3: AI INTELLIGENCE ---
    st.markdown("---")
    st.subheader("🧠 AI Opportunity Heatmap")

    import numpy as np 
    display_df = df.copy()
    display_df["ai_score"] = np.random.randint(20, 100, size=len(df))

    fig_scatter = px.scatter(display_df, x="company", y="ai_score", size="ai_score", color="source", title="AI Opportunity vs. Company Size", hover_data=["name", "email"])
    st.plotly_chart(fig_scatter, use_container_width=True)

else:
    st.info("⚠ No Data Detected. Go to Leads Manager and add some targets.")