import folium
from folium import plugins
import streamlit as st
from streamlit_folium import folium_static

def create_earthquake_map(df):
    """Create a Folium map with earthquake markers"""
    # Create base map centered on mean coordinates
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
    
    # Add earthquake markers
    for idx, row in df.iterrows():
        color = get_marker_color(row['magnitude'])
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['magnitude'] * 3,
            popup=f"Magnitude: {row['magnitude']}<br>"
                  f"Location: {row['place']}<br>"
                  f"Depth: {row['depth']} km<br>"
                  f"Time: {row['time']}",
            color=color,
            fill=True,
            fillColor=color
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def get_marker_color(magnitude):
    """Return color based on earthquake magnitude"""
    if magnitude < 2.0:
        return 'green'
    elif magnitude < 4.0:
        return 'yellow'
    elif magnitude < 6.0:
        return 'orange'
    else:
        return 'red'
