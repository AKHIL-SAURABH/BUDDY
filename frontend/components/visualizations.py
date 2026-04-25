import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from components.roadmap_view import render_roadmap

def render_results():
    st.success("Here is your personalized skill breakdown and learning roadmap.")
    
    data = st.session_state.get("backend_data", {})
    skill_mapping = data.get("skill_mapping", {})
    
    # 1. Score & Graph
    scores = st.session_state.get("assessment_scores", [])
    if scores:
        avg_score = sum(scores) / len(scores)
        st.markdown(f"### 🏆 Overall Assessment Score: **{avg_score:.1f}/100**")
        
        # Simple graph mapping scores to question numbers or the skill
        # Since MVP only assesses one skill, we graph the trajectory over questions
        df = pd.DataFrame({
            "Question": [f"Q{i+1}" for i in range(len(scores))],
            "Score": scores
        })
        fig = px.bar(df, x="Question", y="Score", title=f"Performance Trajectory on {st.session_state.current_skill_testing}", range_y=[0, 100])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No score data recorded (assessment ended early or no valid answers).")
    
    # 2. Render the Gap Analysis "Heatmap"
    st.markdown("### 🔍 Skill Gap Analysis")
    col1, col2, col3, col4 = st.columns(4)
    
    matched = skill_mapping.get("matched_skills", [])
    adjacent = skill_mapping.get("adjacent_skills", [])
    missing = skill_mapping.get("missing_skills", [])
    
    with col1:
        st.info("🟢 Strong\n\n(No action needed)")
        for s in matched:
            st.write(f"- {s}")
    with col2:
        st.warning("🟡 Moderate\n\n(Needs review)")
        for s in adjacent:
            st.write(f"- {s}")
    with col3:
        st.error("🟠 Weak\n\n(Significant gaps)")
        # For MVP, assume the skill they were just tested on is weak if score < 70
        if scores and avg_score < 70:
            st.write(f"- {st.session_state.current_skill_testing}")
        else:
            st.write("_None identified_")
    with col4:
        st.error("🔴 Missing\n\n(Completely absent)")
        for s in missing:
            st.write(f"- {s}")
            
    st.divider()

    # 3. Generate and Render Roadmap
    if "final_roadmap" not in st.session_state:
        with st.spinner("Generating your highly personalized roadmap..."):
            target_role = data.get("job_requirements", {}).get("role", "Software Engineer")
            
            # Determine weak skills
            weak_skills = [st.session_state.current_skill_testing] if scores and avg_score < 70 else []
            
            payload = {
                "strong": matched,
                "moderate": adjacent,
                "weak": weak_skills,
                "missing": missing
            }
            
            try:
                response = requests.post(f"http://localhost:8000/api/v1/dashboard/generate-roadmap?target_role={target_role}", json=payload)
                if response.status_code == 200:
                    st.session_state.final_roadmap = response.json()["data"]
                else:
                    st.error(f"Failed to generate roadmap: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

    if "final_roadmap" in st.session_state and st.session_state.final_roadmap:
        render_roadmap(st.session_state.final_roadmap)
        
    if st.button("Start New Assessment", type="primary"):
        st.session_state.clear()
        st.rerun()