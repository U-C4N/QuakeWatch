import streamlit as st
import pandas as pd
from datetime import datetime

def convert_to_json_safe(data):
    """Convert DataFrame to JSON-safe format with proper datetime handling"""
    json_safe_data = []
    for _, row in data.iterrows():
        row_dict = row.to_dict()
        # Convert datetime to ISO format
        if isinstance(row_dict.get('time'), datetime):
            row_dict['time'] = row_dict['time'].isoformat()
        json_safe_data.append(row_dict)
    return json_safe_data

st.set_page_config(page_title="Earthquake Data JSON View", page_icon="🔍")

st.title("🔍 Earthquake Data JSON View")

# Get data from session state
if 'data' in st.session_state and st.session_state.data is not None:
    data = st.session_state.data
    
    # Add description
    st.markdown("""
    This page displays the complete earthquake dataset in JSON format.
    The data is automatically updated based on the main dashboard's refresh settings.
    """)
    
    # Add formatting options
    st.subheader("Display Options")
    indent_level = st.slider("Indentation Level", min_value=2, max_value=6, value=4)
    
    # Convert data to JSON-safe format
    json_data = convert_to_json_safe(data)
    
    # Display JSON data
    st.subheader("Complete Dataset")
    st.json(json_data, expanded=True)
    
    # Add download button
    st.download_button(
        label="Download JSON",
        data=pd.DataFrame(json_data).to_json(indent=indent_level),
        file_name="earthquake_data.json",
        mime="application/json"
    )
else:
    st.warning("No earthquake data available. Please return to the main dashboard to load data.")
