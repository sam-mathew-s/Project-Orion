from src.knowledge import load_knowledge_base
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
    
    # 1. SELECT TARGET (Common for all tools)
    lead_names = df_leads['name'].tolist()
    selected_lead = st.selectbox("Select Target", lead_names)
    
    # 2. GET DATA & CONTEXT
    target_data = df_leads[df_leads['name'] == selected_lead].iloc[0]
    target_id = target_data['id']
    my_context = load_knowledge_base() # Load your bio from the text file

    # 3. CREATE THE TABS
    tab1, tab2 = st.tabs(["📧 Email Generator", "🧠 AI Lead Scorer"])

    # ==========================
    # TAB 1: THE EMAIL GENERATOR
    # ==========================
    with tab1:
        st.markdown("#### Cold Email Drafter")
        
        # Check for existing saved email
        existing_email = target_data.get('cold_email')

        if st.button("Generate Cold Email", key="btn_email_gen"):
            
            # The Prompt (Using your 'my_info.txt' context)
            prompt = f"""
            You are an AI Assistant writing an email on behalf of:
            {my_context}
            
            TARGET LEAD:
            Name: {target_data['name']}
            Company: {target_data['company']}
            Source: {target_data['source']}
            
            TASK:
            Write a cold email to the Target Lead.
            
            STRICT RULES:
            1. Use the context to mention my skills (Python, Streamlit) and location (Chennai).
            2. Keep it under 150 words.
            3. Do NOT mention "creating files" or errors.
            4. SIGN OFF EXACTLY AS: "Best regards, Sam".
            5. Output ONLY the email body.
            """
            
            with st.spinner("Consulting Knowledge Base..."):
                from agents.llm_engine import get_ai_response
                ai_response = get_ai_response(prompt)
                
                # Save to Database (Immortality)
                supabase.table("leads").update({"cold_email": ai_response}).eq("id", target_id).execute()
                st.success("Draft Saved to Database!")
                st.rerun()

        # Display Saved Email
        if existing_email:
            st.text_area("Current Draft:", value=existing_email, height=300)
            if st.button("🗑️ Clear Draft", key="btn_clear"):
                supabase.table("leads").update({"cold_email": None}).eq("id", target_id).execute()
                st.rerun()

    # ==========================
    # TAB 2: THE LEAD SCORER (NEW!)
    # ==========================
    with tab2:
        st.markdown("#### 🎯 Lead Qualification Engine")
        st.info("This tool analyzes if the company matches your Python/AI skills.")
        
        if st.button("Analyze Lead Potential", key="btn_analyze"):
            
            score_prompt = f"""
            Act as a Career Strategy Expert.
            
            MY PROFILE:
            {my_context}
            
            TARGET LEAD:
            Name: {target_data['name']}
            Company: {target_data['company']}
            Source: {target_data['source']}
            
            TASK:
            Analyze if this lead is a good match for my services.
            1. Assign a Match Score (0-100). Be strict. Deduct points if the company is not Tech Company.
            2. Explain WHY in 1 sentence.
            3. Suggest a specific Technical Angle (e.g., "Pitch an Automation Bot").
            
            OUTPUT FORMAT:
            Score: [Number]/100
            Reason: [Text]
            Strategy: [Text]
            """
            
            with st.spinner("Analyzing Market Fit..."):
                from agents.llm_engine import get_ai_response
                analysis = get_ai_response(score_prompt)
                
                # We use session_state for this one (Temporary View)
                st.session_state[f"analysis_{selected_lead}"] = analysis

        # Show the Analysis if it exists in memory
        if f"analysis_{selected_lead}" in st.session_state:
            st.success("Analysis Complete")
            st.write(st.session_state[f"analysis_{selected_lead}"])

else:
    st.warning("⚠️ No leads found. Add a lead above to unlock AI tools.")