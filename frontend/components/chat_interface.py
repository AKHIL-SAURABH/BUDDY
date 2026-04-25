import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_URL = f"{BACKEND_URL}/api/v1/assessment/chat-turn"

def render_chat():
    skill = st.session_state.current_skill_testing
    
    # Initialize chat history and score tracking
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.assessment_scores = []
        # Trigger the first question automatically
        with st.spinner("Agent is preparing the first question..."):
            payload = {"skill": skill, "current_difficulty": "Medium"}
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()["data"]
                st.session_state.messages.append({"role": "assistant", "content": data["next_question"]})
                st.session_state.last_agent_data = data
            
    # Render existing messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle new user input
    if user_answer := st.chat_input("Type your answer here..."):
        # Display the user's answer immediately
        st.chat_message("user").markdown(user_answer)
        st.session_state.messages.append({"role": "user", "content": user_answer})
        
        with st.spinner("Evaluating your answer..."):
            last_data = st.session_state.last_agent_data
            payload = {
                "skill": skill,
                "previous_question": st.session_state.messages[-2]["content"], # The question they are answering
                "candidate_answer": user_answer,
                "current_difficulty": last_data.get("next_difficulty", "Medium")
            }
            
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()["data"]
                st.session_state.last_agent_data = result
                
                # Track the score if evaluated
                if "evaluation_score" in result and result["evaluation_score"] is not None:
                    st.session_state.assessment_scores.append(result["evaluation_score"])
                
                # Check if the agent is done assessing this skill
                if result.get("is_completed"):
                    st.success("✅ Assessment complete! Generating your results...")
                    st.session_state.current_stage = "results"
                    st.rerun()
                else:
                    # Display the next question
                    next_q = result["next_question"]
                    st.chat_message("assistant").markdown(next_q)
                    st.session_state.messages.append({"role": "assistant", "content": next_q})
            else:
                st.error("Backend Error: Could not reach the assessment agent.")
                
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🛑 End Assessment", use_container_width=True):
            st.session_state.current_stage = "results"
            st.rerun()