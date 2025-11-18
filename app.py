import streamlit as st
import requests
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Gemini Workflow Architect", page_icon="🤖")

st.title("🤖 AI Workflow Architect")
st.caption("Powered by Gemini 3.0 Logic (Direct API)")

# --- SIDEBAR ---
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Using Direct API Mode (No SDK)")

# --- MAIN INPUT ---
user_emails = st.text_area("Paste your manual tasks/emails here:", height=200)

# --- THE LOGIC (Direct API Call) ---
def call_gemini_direct(prompt, key):
    # FIX: This URL line is now indented correctly (4 spaces)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except KeyError:
            return "Error: Unexpected response format from Google."
    else:
        return f"Error: {response.text}"

SYSTEM_PROMPT = """
You are an AI Automation Assistant. Analyze the user's input and output a workflow plan.
1. Summary of patterns.
2. Manual tasks list.
3. Automation ideas (n8n/Zapier).
4. Detailed Step-by-step workflow.
User Input:
"""

if st.button("🚀 Architect Workflow", type="primary"):
    if not api_key:
        st.error("Please enter API Key.")
    elif not user_emails:
        st.warning("Please enter text.")
    else:
        with st.spinner("Architecting..."):
            try:
                # Combine prompt and input
                full_prompt = SYSTEM_PROMPT + user_emails
                result = call_gemini_direct(full_prompt, api_key)
                st.markdown("---")
                st.markdown(result)
            except Exception as e:
                st.error(f"Connection error: {e}")
