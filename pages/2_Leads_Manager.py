import streamlit as st
import pandas as pd
from src.database import fetch_all_leads, supabase
from agents.llm_engine import get_ai_response

st.set_page_config(page_title="Leads Manager", layout="wide")
st.title("🚀 Orion Leads Manager")

# --- 1. LOAD DATA ---
# We use a spinner so the user knows something is happening
with st.spinner("Accessing Orion Database..."):
    df_leads = fetch_all_leads()

# --- 2. ADD NEW LEAD SECTION ---
with st.expander("➕ Add New Lead", expanded=False):
    with st.form("add_lead_form"):
        c1, c2 = st.columns(2)
        new_name = c1.text_input("Full Name")
        new_company = c2.text_input("Company Name")
        new_email = c1.text_input("Email Address")
        new_source = c2.selectbox("Source", ["manual", "linkedin", "referral", "website"])
        
        if st.form_submit_button("Save to Database"):
            if new_name and new_company:
                new_lead = {
                    "name": new_name, 
                    "company": new_company, 
                    "email": new_email, 
                    "source": new_source, 
                    "status": "new",
                    "org_id": "default"
                }
                try:
                    supabase.table("leads").insert(new_lead).execute()
                    st.success("✅ Lead Secured!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Name & Company required.")

# --- 3. DATA TABLE ---
st.dataframe(df_leads, use_container_width=True)

# --- 4. AI OPERATIONS CENTER (The Brain) ---
st.markdown("---")
st.subheader("🤖 AI Agent Actions")

# Safety Check
if not df_leads.empty and "name" in df_leads.columns:
    
    # Select Target
    lead_names = df_leads['name'].tolist()
    selected_lead = st.selectbox("Select Target", lead_names)

    # Get Data to target
    target_data = df_leads[df_leads['name'] == selected_lead].iloc[0]
    target_id = target_data['id'] 

    # check if already have a saved email in the Database
    existing_email = target_data.get('cold_email')

    col1, col2 = st.columns(2)

    # BUTTON: GENERATE NEW EMAIL
    if col1.button("Generate Cold Email"):

        # Hardcoded Name Logic
        my_name = "Sam"

        prompt = f"""
        Write a sales email to {target_data['name']} at {target_data['company']}.
        FROM: {my_name} (Orion AI Architect).
        GOAL: Schedule a demo.

        STRICT OUTPUT RULES:
        1. Write ONLY the email body.
        2. Do NOT write "Here is the email" "Subject:"
        3. Start directly with "Dear {target_data['name']},".
"""
        with st.spinner("AI is writing to the Database..."):
            from agents.llm_engine import get_ai_response 
            
            # Get text from AI
            ai_response = get_ai_response(prompt)

            # Save to supabse
            supabase.table("leads").update({"cold_email": ai_response}).eq("id", target_id).execute()

            st.success("Email Generated & Saved to Database!")
            st.rerun() # Refresh to show the new data

    if existing_email:
        st.markdown("### 📝 Saved Draft")
        st.text_area("Content", value=existing_email, height=300)

        #CLEAR BUTTON
        if col2.button("Clear Saved Data"):
            supabase.table("leads").update({"cold_email": None}).eq("id", target_id).execute
            st.rerun()
        else:
            st.info("No email saved yet. Click Generate.")

