import streamlit as st
from components.sidebar import render_sidebar
from components.chat_interface import render_chat
from components.visualizations import render_results
from components.summary_view import render_summary

st.set_page_config(page_title="Catalyst | AI Assessment", page_icon="🚀", layout="wide")

# --- Initialize Session State ---
# This is crucial so Streamlit remembers where the user is when the page reloads
if "current_stage" not in st.session_state:
    st.session_state.current_stage = "upload"  # Stages: upload, summary, interview, results
if "backend_data" not in st.session_state:
    st.session_state.backend_data = None
if "current_skill_testing" not in st.session_state:
    st.session_state.current_skill_testing = None

st.title("🚀 Catalyst: AI Skill Verification")
st.markdown("Move beyond the resume. Prove what you know.")

# --- Application Routing ---
if st.session_state.current_stage == "upload":
    st.info("👈 Please upload your Job Description and Resume in the sidebar to begin.")
    
    # Render the upload sidebar
    render_sidebar()

elif st.session_state.current_stage == "summary":
    render_summary()

elif st.session_state.current_stage == "interview":
    st.subheader(f"🧠 Live Assessment: {st.session_state.current_skill_testing}")
    render_chat()

elif st.session_state.current_stage == "results":
    st.subheader("📊 Your Skill Gap Analysis & Roadmap")
    render_results()