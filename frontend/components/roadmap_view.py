import streamlit as st

def render_roadmap(roadmap_data: dict):
    """
    Renders the generated week-by-week learning roadmap dynamically.
    Expects a dictionary matching the LearningRoadmap Pydantic schema.
    """
    target_role = roadmap_data.get("target_role", "Target Role")
    
    st.markdown(f"### 🗺️ Your Personalized Learning Plan: {target_role}")
    st.write("Based on your assessment, here is your tailored sprint to close your core gaps.")
    
    plan = roadmap_data.get("plan", [])
    
    if not plan:
        st.success("No critical gaps identified! You are highly aligned with the target role.")
        return

    # Iterate through the weeks and create an expandable section for each
    for week_plan in plan:
        week_num = week_plan.get("week", "X")
        focus = week_plan.get("focus", "General Study")
        hours = week_plan.get("hours", 0)
        
        # Keep the first week expanded by default, collapse the rest
        is_first_week = (week_num == 1 or week_num == "1")
        
        with st.expander(f"Week {week_num}: {focus} ⏱️ (~{hours} Hours)", expanded=is_first_week):
            resources = week_plan.get("resources", [])
            
            if not resources:
                st.write("No specific resources assigned for this week. Focus on practical implementation.")
            else:
                for res in resources:
                    title = res.get("title", "Resource")
                    url = res.get("url", "#")
                    res_type = res.get("type", "Material")
                    
                    # Format: * [Course] Title (Hyperlinked)
                    st.markdown(f"* **[{res_type}]** [{title}]({url})")