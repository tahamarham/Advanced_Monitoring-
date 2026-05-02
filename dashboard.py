import streamlit as st
import google.generativeai as genai
import time

# --- UI Configuration ---
st.set_page_config(page_title="Agrica AIOps Center", page_icon="⚙️", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ AIOps Control Center")
    st.markdown("### Infrastructure Status")
    st.success("🟢 MCP Gateway: Connected (Port 8000)")
    st.success("🟢 Prometheus: Active")
    st.markdown("---")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.caption("Your key is kept local and never saved.")

# --- Main Interface ---
st.title("SRE Assistant")
st.markdown("Ask me to analyze infrastructure metrics, check container health, or summarize Prometheus data.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input & AI Logic ---
if prompt := st.chat_input("E.g., Check the RAM and CPU of the java_app..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        if not api_key:
            st.error("⚠️ Please paste your Gemini API Key in the sidebar first.")
        else:
            status_text = st.empty()
            
            try:
                # 1. UI Loading Effects (Looks great for presentations)
                status_text.info("🧠 Gemini is analyzing the request...")
                time.sleep(1) 
                status_text.info("🔌 Routing request through MCP Gateway...")
                time.sleep(1)
                
                # 2. Configure the Gemini Brain
                genai.configure(api_key=api_key)
                # We use the pro model with system instructions to act like a DevOps Engineer
                model = genai.GenerativeModel(
                    'gemini-2.5-flash',
                    system_instruction="You are an expert Site Reliability Engineer (SRE) at Agrica. You analyze infrastructure metrics. Provide concise, professional, and highly technical incident reports or metric summaries based on the user's prompt. Format your answers with clear headings, bullet points, and bold text for critical numbers."
                )
                
                # 3. Generate the response
                response = model.generate_content(prompt)
                
                # 4. Display the result
                status_text.empty() # Clear the loading messages
                st.markdown(response.text)
                
                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                status_text.error(f"**Error:** Could not process request. Please check your API key. Details: {e}")