import streamlit as st 
from agents.llm_engine import get_ai_response 

st.set_page_config(page_title="Orion AI", layout="wide")
st.title("🤖 Orion AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input 
if prompt := st.chat_input("Command the system..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    #get AI response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response = get_ai_response(prompt, system_instruction="You are Orion, the Advanced CRM AI.")
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
