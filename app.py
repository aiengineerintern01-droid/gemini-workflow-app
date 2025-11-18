import streamlit as st
import google.generative_ai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Gemini 3.0 Workflow Architect",
    page_icon="🤖",
    layout="centered"
)

# --- HEADER & INTRODUCTION ---
st.title("🤖 AI Workflow Architect")
st.caption("Powered by Gemini 3.0 Logic | Automate the Boring Stuff")

st.markdown("""
**How this works:**
1. Paste examples of messy emails or notifications you handle manually (leads, orders, support).
2. The AI detects the pattern and architects an automated workflow.
""")

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("Configuration")
    # OPTION 1: User enters their key (Safe for public demos)
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get one at aistudio.google.com")
    
    st.info("ℹ️ **Privacy Note:** Your API key is not stored. It is used only for this session.")
    st.markdown("---")
    st.markdown("Built for the **Gemini 3.0** workflow experiment.")

# --- MAIN LOGIC ---
user_emails = st.text_area(
    "Paste your email/notification examples here:",
    height=200,
    placeholder="Subject: New Lead \nBody: We have a new inquiry from John Doe...\n\nSubject: Order #1234 \nBody: Order confirmed for $50..."
)

# The "Gemini 3" System Prompt
SYSTEM_PROMPT = """
You are an AI Automation Assistant.

The user will paste 1–5 example emails or notifications they often handle manually
(e.g., lead emails, order confirmations, support requests).

Your tasks:

1) Pattern
- In 1–2 sentences, explain what these messages are about and when they usually arrive.

2) What can be automated
- List 3–5 things that are currently done manually
(for example: copy data to a sheet, reply with a template, create a task).

3) Automation ideas
- Suggest 2–3 concrete automations that would save time.
- For each idea, mention which tools could be used (like n8n, Zapier, Make, Google Sheets,
Gmail, Slack, Notion, a CRM).

4) Example workflow outline
- Pick ONE of the ideas and give an 'n8n workflow outline' with 4–8 steps in this format:

1. Trigger: …
2. Node: …
3. Node: …
4. Node: …
5. Node: …

Use simple English. Keep the whole answer under 250 words.
"""

if st.button("🚀 Architect Workflow", type="primary"):
    if not api_key:
        st.error("Please enter an API Key in the sidebar to activate the agent.")
    elif not user_emails:
        st.warning("Please paste some email examples first.")
    else:
        try:
            genai.configure(api_key=api_key)
            # Using the latest stable model to execute the logic
            model = genai.GenerativeModel(
                model_name="gemini-2.5-pro", 
                system_instruction=SYSTEM_PROMPT
            )
            
            with st.spinner("Analyzing patterns and designing workflow..."):
                response = model.generate_content(user_emails)
                
                st.markdown("### ⚡ Workflow Blueprint")
                st.markdown("---")
                st.markdown(response.text)
                st.success("Analysis Complete.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- FOOTER ---
st.markdown("---")
st.markdown("Create your own workflows with Google Gemini.")
