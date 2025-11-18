import streamlit as st
import requests

st.set_page_config(page_title="Debug Mode", page_icon="🛠️")
st.title("🛠️ Connection Debugger")

# 1. INPUTS
api_key = st.text_input("Paste New API Key", type="password")
test_input = st.button("Test Connection")

# 2. THE RAW TEST
if test_input and api_key:
    st.info("Attempting to connect to Google...")
    
    # We use the most standard URL possible
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": "Hello, are you there?"}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        # 3. DIAGNOSTIC OUPUT
        st.write(f"**HTTP Status Code:** {response.status_code}")
        
        if response.status_code == 200:
            st.success("✅ SUCCESS! The key works.")
            st.json(response.json())
        else:
            st.error("❌ FAILURE. Here is the exact error from Google:")
            st.code(response.text, language="json")
            
    except Exception as e:
        st.error(f"Python Error: {e}")
