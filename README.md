# Real-Time Earthquake Monitoring Dashboard 🌍

A comprehensive real-time earthquake monitoring system that provides interactive visualization and analysis of seismic activity worldwide. The dashboard offers live updates, interactive mapping, and advanced filtering capabilities to track and analyze earthquake data.

## Features

### Real-Time Monitoring
- Live earthquake data updates from USGS
- Auto-refresh functionality with customizable intervals
- Interactive data table with sorting capabilities
- Color-coded magnitude indicators

### Interactive Mapping
- Dynamic map visualization using Folium
- Color-coded markers based on earthquake magnitude
- Popup information for each earthquake event
- Global coverage with automatic centering

### Alert System
- Automated notifications for major earthquakes (magnitude ≥ 6.0)
- Toast notifications in the sidebar
- Real-time alert delivery

### Data Analysis
- Historical comparison capabilities
- Statistical analysis tools
- Customizable filtering options:
  - Magnitude range
  - Depth range
  - Time period

### Detailed Information
- Comprehensive earthquake information cards
- Magnitude gauge charts
- Precise location details
- UTC timestamp display

## Technology Stack

- **Frontend Framework:** Streamlit
- **Mapping:** Folium
- **Data Processing:** Pandas
- **Visualization:** Plotly
- **Data Source:** USGS Earthquake API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/U-C4N/earthquake-monitor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Access the dashboard at `http://localhost:5000`

## Dashboard Sections

### Main Interface
- **Real-Time Data Table:** View and sort recent earthquakes
- **Interactive Map:** Visualize earthquake locations
- **Filtering Options:** Customize data display

### Sidebar Controls
- **Auto-refresh Toggle:** Enable/disable automatic updates
- **Refresh Interval:** Set update frequency
- **Magnitude Filter:** Set minimum magnitude threshold
- **Depth Filter:** Set maximum depth threshold

### Historical Comparison
- Compare current seismic activity with historical data
- Analyze trends and patterns
- View statistical comparisons

### Detailed Information Cards
- Comprehensive earthquake details
- Magnitude gauge visualization
- Precise location coordinates
- Event timing information

## Data Source

This project uses data from the United States Geological Survey (USGS) Earthquake Hazards Program. The data is fetched in real-time through their public API.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- USGS for providing the earthquake data API
- Streamlit team for the excellent framework
- Folium contributors for the mapping capabilities
