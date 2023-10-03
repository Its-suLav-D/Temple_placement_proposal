import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Temple Placement Analysis",
    page_icon="🐍",
)

st.title("Temple Placement Analysis")


# Displaying team name in a more visually appealing manner
st.markdown("""
## Team Slytherin 🐍
""")



# Introduction and overview of the project
st.subheader('Project Overview')

st.write("""
Our team is tasked with developing a predictive model to identify potential 
locations for new temples and churches across the US. We leverage high-quality 
data provided by SafeGraph, enriched with census data and real-time weather 
information from the OpenWeather API. Our comprehensive analytics approach 
ensures a precise, data-driven strategy for optimal temple placement, 
maximizing accessibility and convenience for the community.

The predictive model, backed by our robust data analytics pipeline, is designed 
for easy interpretation and use by non-technical stakeholders. Accompanied by 
well-documented guides, we ensure seamless understanding and application of 
the insights derived from the model.
""")

st.subheader('Data Sources and Approach')

st.write("""
- **SafeGraph Data:** Provides rich, spatial, and temporal data on foot traffic at 
various points of interest.
- **Census Data:** Offers demographic, economic, and geographical data for refined 
analysis.
- **OpenWeather API:** Enables real-time weather data integration to factor in 
environmental conditions.

We employ advanced data wrangling techniques, feature creation, and predictive 
modeling powered by Spark, ensuring efficient and scalable processing of large 
data volumes. Our approach is rooted in data-driven insights, accuracy, and 
usability, delivering a robust tool for informed decision-making in temple 
placement.
""")

st.subheader('Project Deliverables')

st.write("""
- A user-friendly predictive model interface accessible by non-technical employees.
- Comprehensive guides on data ingestions, engineering, application development, 
and process implementation.
- Ongoing support and updates to ensure the model’s accuracy and relevance with 
changing data landscapes.
""")

st.markdown('### Team Members and Majors')
st.markdown('---')

# Team members and majors
team_members = pd.DataFrame({
    'Name': ['Sulove Dahal', 'Spencer Howe', 'Kyle Baker', 'Aaron Jones', 'Brandon Lythgoe'],
    'Major': ['SWE / ML', 'Data Science', 'Data Science', 'Computer Science', 'Data Science']
})

# Display team members and majors in a better format
for index, row in team_members.iterrows():
    st.markdown(f"**{row['Name']}** - *{row['Major']}*")
