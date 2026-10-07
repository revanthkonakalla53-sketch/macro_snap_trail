from google import genai
from google.genai import types
import streamlit as st
from prompts import SYSTEM_PROMPT,WELCOME_MESSAGE_TEMPLATE,SUMMARY_REQUEST_PROMPT
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

@st.cache_resource
def get_gemini_client():

    return genai.Client(api_key =st.secrets["GEMINI_API_KEY"])
gemini_client = get_gemini_client()
MODEL_NAME = "gemini-3.8-flash"

#step1 : onboarding (username and phone)
if 'onboarded' not in st.session_state:
    st.title("MacroSnap 🥗")
    st.caption("Snap it .Track it. Text yourself the results.")
    with st.form("onboarding_form"):
        name = st.text_input("Your name")
        whatsapp_number = st.text_input(
            "WhatsApp number (with country code)",
            placeholder="+91XXXXXXXXXX",
            help = "This is the number MacroSnap will text your summary to."
        )
        submitted = st.form_submit_button("Let's go 🚀")
    if submitted:
        if not name.strip() or not whatsapp_number.strip():
            st.warning("Please fill in both your name and WhatsApp number.")
        else:
            st.session_state.name = name.strip()
            st.session_state.whatsapp_number = whatsapp_number.strip()
            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            st.session_state.messages = []
            st.session_state.onboarded = True
            st.rerun()
    st.stop()  


# creating a chat interface
