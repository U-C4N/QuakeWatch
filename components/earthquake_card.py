import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def display_earthquake_card(earthquake_data):
    """Display detailed information card for a selected earthquake"""
    if earthquake_data is None:
        return
    
    # Create card container with custom styling
    with st.container():
        st.markdown("""
            <style>
            .earthquake-card {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin: 10px 0;
            }
            </style>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="earthquake-card">', unsafe_allow_html=True)
        
        # Header with magnitude and location
        magnitude_color = get_magnitude_color(earthquake_data['magnitude'])
        st.markdown(
            f"""
            <h2 style='margin-bottom: 0px;'>
                <span style='color: {magnitude_color}'>M {earthquake_data['magnitude']:.1f}</span>
                Earthquake
            </h2>
            <h3 style='margin-top: 5px; color: #666;'>{earthquake_data['place']}</h3>
            """,
            unsafe_allow_html=True
        )
        
        # Create three columns for key information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Depth", f"{earthquake_data['depth']:.1f} km")
        
        with col2:
            st.metric("Latitude", f"{earthquake_data['latitude']:.3f}°")
        
        with col3:
            st.metric("Longitude", f"{earthquake_data['longitude']:.3f}°")
        
        # Time information
        st.markdown("### Time Information")
        event_time = earthquake_data['time']
        st.write(f"Event Time (UTC): {event_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Create a gauge chart for magnitude visualization
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = earthquake_data['magnitude'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 10], 'tickwidth': 1},
                'bar': {'color': magnitude_color},
                'steps': [
                    {'range': [0, 2], 'color': '#a8e6cf'},
                    {'range': [2, 4], 'color': '#ffd3b6'},
                    {'range': [4, 6], 'color': '#ffaaa5'},
                    {'range': [6, 10], 'color': '#ff8b94'}
                ],
            },
            title = {'text': "Magnitude Scale"}
        ))
        
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def get_magnitude_color(magnitude):
    """Return color code based on earthquake magnitude"""
    if magnitude < 2.0:
        return '#1b7340'  # Dark green
    elif magnitude < 4.0:
        return '#b35900'  # Dark orange
    elif magnitude < 6.0:
        return '#cc2900'  # Dark red
    else:
        return '#800000'  # Very dark red