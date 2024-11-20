import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
from streamlit_folium import st_folium
import plotly.express as px

from utils.data_fetcher import EarthquakeDataFetcher
from utils.map_helper import create_earthquake_map
from styles.styles import apply_styles, get_magnitude_color
from components.earthquake_card import display_earthquake_card

# Page configuration
st.set_page_config(
    page_title="Real-Time Earthquake Monitor",
    page_icon="🌍",
    layout="wide"
)

# Apply custom styles
apply_styles()

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = None
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'earthquake_fetcher' not in st.session_state:
    st.session_state.earthquake_fetcher = EarthquakeDataFetcher()
if 'selected_earthquake' not in st.session_state:
    st.session_state.selected_earthquake = None

def load_data():
    """Fetch and process earthquake data"""
    data = st.session_state.earthquake_fetcher.fetch_data()
    st.session_state.data = data
    st.session_state.last_update = datetime.now()
    
    # Check for major earthquakes
    new_major_quakes = st.session_state.earthquake_fetcher.get_new_major_earthquakes(data)
    for quake in new_major_quakes:
        st.toast(f"⚠️ Major Earthquake Alert!\nMagnitude {quake['magnitude']:.1f} earthquake detected near {quake['place']}")
    
    return data

# Header
st.title("🌍 Real-Time Earthquake Monitor")

# Alert Section
st.sidebar.markdown("""
    <div style='background-color: #ff4b4b22; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>
        <h3 style='color: #ff4b4b; margin: 0;'>⚠️ Alert Settings</h3>
        <p style='margin: 5px 0;'>Alerts are enabled for earthquakes with magnitude ≥ 6.0</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("Filters")
auto_refresh = st.sidebar.checkbox("Auto-refresh data", value=True)
refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 
                                   min_value=30, 
                                   max_value=300, 
                                   value=60)

# Manual refresh button
if st.sidebar.button("Refresh Data Now"):
    load_data()

# Historical comparison section in sidebar
st.sidebar.header("Historical Comparison")
compare_enabled = st.sidebar.checkbox("Enable Historical Comparison")
if compare_enabled:
    compare_days = st.sidebar.number_input("Days to Compare", min_value=1, max_value=30, value=7)
    compare_start = datetime.now() - timedelta(days=compare_days)
    compare_end = datetime.now() - timedelta(days=compare_days-1)
    
    if st.sidebar.button("Load Historical Data"):
        fetcher = EarthquakeDataFetcher()
        st.session_state.historical_data = fetcher.fetch_historical_data(compare_start, compare_end)

# Filter controls
min_magnitude = st.sidebar.slider("Minimum Magnitude", 0.0, 9.0, 0.0, 0.1)
max_depth = st.sidebar.slider("Maximum Depth (km)", 0, 700, 700, 10)

# Auto-refresh logic
if auto_refresh and (st.session_state.last_update is None or 
                    (datetime.now() - st.session_state.last_update).seconds > refresh_interval):
    load_data()

# Load initial data if needed
if st.session_state.data is None:
    data = load_data()
else:
    data = st.session_state.data

# Apply filters
filtered_data = data[
    (data['magnitude'] >= min_magnitude) &
    (data['depth'] <= max_depth)
]

# Display last update time
st.sidebar.text(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S') if st.session_state.last_update else 'Never'}")

# Main content
if compare_enabled and st.session_state.historical_data is not None:
    col1, col2 = st.columns(2)
else:
    col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Recent Earthquakes")
    
    # Sorting options
    sort_by = st.selectbox(
        "Sort by",
        ["Time (newest first)", "Magnitude (highest first)", "Depth (deepest first)"]
    )
    
    if sort_by == "Time (newest first)":
        filtered_data = filtered_data.sort_values('time', ascending=False)
    elif sort_by == "Magnitude (highest first)":
        filtered_data = filtered_data.sort_values('magnitude', ascending=False)
    else:
        filtered_data = filtered_data.sort_values('depth', ascending=False)
    
    # Display data table with selection
    styled_df = filtered_data.style.map(
        lambda x: get_magnitude_color(x),
        subset=['magnitude']
    )
    
    selected_indices = st.data_editor(
        styled_df,
        column_config={
            "magnitude": st.column_config.NumberColumn("Magnitude", format="%.1f"),
            "depth": st.column_config.NumberColumn("Depth (km)", format="%.1f"),
            "time": st.column_config.DatetimeColumn("Time (UTC)"),
            "latitude": st.column_config.NumberColumn("Latitude", format="%.3f"),
            "longitude": st.column_config.NumberColumn("Longitude", format="%.3f")
        },
        hide_index=True,
        use_container_width=True
    )

    # Update selected earthquake when row is clicked
    if len(selected_indices.index) > 0:
        selected_row = selected_indices.iloc[0]
        st.session_state.selected_earthquake = selected_row.to_dict()

with col2:
    st.subheader("Map View")
    if not filtered_data.empty:
        map_obj = create_earthquake_map(filtered_data)
        st_folium(map_obj, width=400)
    else:
        st.warning("No earthquake data available for the selected filters.")

# Display earthquake information card if an earthquake is selected
if st.session_state.selected_earthquake:
    st.header("Detailed Earthquake Information")
    display_earthquake_card(st.session_state.selected_earthquake)

# Historical Comparison Section
if compare_enabled and st.session_state.historical_data is not None:
    st.header("Historical Comparison")
    
    # Filter historical data
    filtered_historical = st.session_state.historical_data[
        (st.session_state.historical_data['magnitude'] >= min_magnitude) &
        (st.session_state.historical_data['depth'] <= max_depth)
    ]
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Magnitude distribution comparison
        fig_magnitude = px.histogram(
            filtered_data,
            x="magnitude",
            title="Current Magnitude Distribution",
            nbins=20
        )
        st.plotly_chart(fig_magnitude)
        
    with col4:
        # Historical magnitude distribution
        fig_historical = px.histogram(
            filtered_historical,
            x="magnitude",
            title=f"Historical Magnitude Distribution ({compare_days} days ago)",
            nbins=20
        )
        st.plotly_chart(fig_historical)
    
    # Comparison statistics
    st.subheader("Comparative Statistics")
    comp_cols = st.columns(4)
    
    with comp_cols[0]:
        current_count = len(filtered_data)
        historical_count = len(filtered_historical)
        count_diff = current_count - historical_count
        st.metric("Total Earthquakes", current_count, 
                 delta=count_diff, delta_color="normal")
    
    with comp_cols[1]:
        current_avg_mag = filtered_data['magnitude'].mean()
        historical_avg_mag = filtered_historical['magnitude'].mean()
        mag_diff = current_avg_mag - historical_avg_mag
        st.metric("Average Magnitude", f"{current_avg_mag:.1f}", 
                 delta=f"{mag_diff:+.1f}", delta_color="inverse")
    
    with comp_cols[2]:
        current_max_mag = filtered_data['magnitude'].max()
        historical_max_mag = filtered_historical['magnitude'].max()
        max_diff = current_max_mag - historical_max_mag
        st.metric("Maximum Magnitude", f"{current_max_mag:.1f}", 
                 delta=f"{max_diff:+.1f}", delta_color="inverse")
    
    with comp_cols[3]:
        current_avg_depth = filtered_data['depth'].mean()
        historical_avg_depth = filtered_historical['depth'].mean()
        depth_diff = current_avg_depth - historical_avg_depth
        st.metric("Average Depth", f"{current_avg_depth:.1f} km", 
                 delta=f"{depth_diff:+.1f}", delta_color="normal")

# Footer
st.markdown("---")
st.markdown("Data source: USGS Earthquake API")
