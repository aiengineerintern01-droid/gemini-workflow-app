import streamlit as st
import requests
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Gemini Workflow Architect", page_icon="🤖", layout="centered")

st.title("🤖 AI Workflow Architect")
st.caption("Powered by Gemini (Multi-Model Fallback System)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("System Status: Ready")

# --- MAIN INPUT ---
user_emails = st.text_area(
    "Paste your manual tasks or email examples here:", 
    height=200,
    placeholder="Example: I get emails about invoices, I download them, rename them, and upload to Drive..."
)

# --- THE ROBUST LOGIC ---
def call_gemini_robust(prompt, key):
    # LIST OF MODELS TO TRY (If one fails, it tries the next)
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash-latest",
        "gemini-pro"
    ]
    
    last_error = ""

    for model_name in models_to_try:
        try:
            # Construct the URL for this specific model
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
            headers = {"Content-Type": "application/json"}
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            
            # Make the request
            response = requests.post(url, headers=headers, json=data)
            
            # If successful (Code 200), return the text immediately
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                # If failed, log error and continue to next model in list
                last_error = f"Model {model_name} failed ({response.status_code}). Switching..."
                continue
                
        except Exception as e:
            last_error = str(e)
            continue
            
    # If loop finishes and nothing worked:
    return f"All models failed. Please check your API Key. Last error: {last_error}"

# --- THE SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are an expert AI Automation Consultant.
Your goal: Convert the user's messy description of manual work into a structured automation workflow.

Response Structure:
1. THE PAIN: Summarize what they are doing manually in 1 sentence.
2. THE FIX: List 3 steps to automate this.
3. THE BLUEPRINT: Create a technical workflow (Trigger -> Action -> Action) for tools like n8n or Zapier.

USER INPUT TO ANALYZE:
"""

# --- EXECUTION ---
if st.button("🚀 Architect Workflow", type="primary"):
    if not api_key:
        st.error("Please enter your API Key in the sidebar.")
    elif not user_emails:
        st.warning("Please paste some text to analyze.")
    else:
        with st.spinner("Analyzing workflow patterns..."):
            # Combine instructions with user input
            full_prompt = SYSTEM_PROMPT + "\n" + user_emails
            
            # Run the robust function
            result = call_gemini_robust(full_prompt, api_key)
            
            # Display results
            st.markdown("---")
            if "All models failed" in result:
                st.error(result)
            else:
                st.success("Blueprint Generated Successfully")
                st.markdown(result)
