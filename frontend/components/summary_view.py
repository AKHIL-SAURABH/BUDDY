import streamlit as st

def render_summary():
    st.subheader("📋 Pre-Assessment Analysis")
    
    # Safely retrieve data
    data = st.session_state.get("backend_data", {})
    skill_mapping = data.get("skill_mapping", {})
    
    matched = skill_mapping.get("matched_skills", [])
    missing = skill_mapping.get("missing_skills", [])
    adjacent = skill_mapping.get("adjacent_skills", [])
    
    # Calculate match percentage
    total_skills = len(matched) + len(missing) + len(adjacent)
    if total_skills > 0:
        # Give partial credit for adjacent skills
        score = len(matched) + (len(adjacent) * 0.5)
        match_percentage = int((score / total_skills) * 100)
    else:
        match_percentage = 0

    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("JD Match Strength", f"{match_percentage}%")
    col2.metric("Matched Skills", len(matched))
    col3.metric("Missing Skills", len(missing))
    
    st.divider()
    
    # Display Breakdown
    col_match, col_miss = st.columns(2)
    
    with col_match:
        st.success("✅ Skills Matched")
        if matched:
            for skill in matched:
                st.write(f"- {skill}")
        else:
            st.write("_None detected_")
            
        if adjacent:
            st.info("🔄 Adjacent/Transferable Skills")
            for skill in adjacent:
                st.write(f"- {skill}")
                
    with col_miss:
        st.error("❌ Skills Missing")
        if missing:
            for skill in missing:
                st.write(f"- {skill}")
        else:
            st.write("_None missing! Perfect match._")
            
    st.divider()
    
    # Start Assessment Button
    st.write("Ready to prove your skills? The AI will now conduct a live technical interview based on the requirements.")
    
    if st.button("🚀 Start Assessment", type="primary", use_container_width=True):
        st.session_state.current_stage = "interview"
        st.rerun()
