import streamlit as st

def apply_styles():
    """Apply custom styles to the Streamlit app"""
    st.markdown("""
        <style>
        .main {
            padding: 1rem;
        }
        .stTable {
            width: 100%;
        }
        .st-emotion-cache-1wf13uc {
            max-width: 100%;
        }
        .magnitude {
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

def get_magnitude_color(magnitude):
    """Return background color based on magnitude"""
    if magnitude < 2.0:
        return 'background-color: #a8e6cf'  # Light green
    elif magnitude < 4.0:
        return 'background-color: #ffd3b6'  # Light orange
    elif magnitude < 6.0:
        return 'background-color: #ffaaa5'  # Salmon
    else:
        return 'background-color: #ff8b94'  # Red
