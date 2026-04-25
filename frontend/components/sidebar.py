import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1/ingest/upload"

def render_sidebar():
    with st.sidebar:
        st.header("📄 Ingestion Setup")
        
        with st.form("upload_form"):
            jd_text = st.text_area("Paste Job Description", height=200, placeholder="e.g., We are looking for a Machine Learning Engineer...")
            resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
            
            submitted = st.form_submit_button("Analyze & Start Interview", use_container_width=True)
            
            if submitted:
                if not jd_text or not resume_file:
                    st.error("⚠️ Both Job Description and Resume are required.")
                else:
                    with st.spinner("Agents are analyzing documents..."):
                        # Prepare the payload for FastAPI
                        files = {"resume": (resume_file.name, resume_file, "application/pdf")}
                        data = {"jd_text": jd_text}
                        
                        try:
                            # Send POST request to your backend
                            response = requests.post(API_URL, data=data, files=files)
                            
                            if response.status_code == 200:
                                result = response.json()
                                # Save the data to session state
                                st.session_state.backend_data = result["data"]
                                
                                # Pick the first skill to start testing
                                missing_skills = result["data"]["skill_mapping"]["missing_skills"]
                                if missing_skills:
                                    st.session_state.current_skill_testing = missing_skills[0]
                                
                                # Move the user to the summary stage!
                                st.session_state.current_stage = "summary"
                                st.rerun()
                            else:
                                st.error(f"Backend Error: {response.text}")
                        except requests.exceptions.ConnectionError:
                            st.error("🚨 Cannot connect to the backend. Is FastAPI running?")