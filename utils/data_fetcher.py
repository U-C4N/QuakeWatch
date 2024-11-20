import pandas as pd
import requests
from datetime import datetime, timedelta

class EarthquakeDataFetcher:
    def __init__(self):
        self.base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.geojson_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary"
        self.endpoint = "/all_day.geojson"
        self.major_earthquake_threshold = 6.0
        self.last_major_earthquakes = set()  # Store IDs of previously alerted earthquakes

    def fetch_data(self):
        """Fetch current earthquake data from USGS API"""
        try:
            response = requests.get(f"{self.geojson_url}{self.endpoint}")
            response.raise_for_status()
            data = self._process_response(response.json())
            self._check_major_earthquakes(data)
            return data
        except Exception as e:
            print(f"Error fetching current data: {e}")
            return pd.DataFrame()

    def fetch_historical_data(self, start_time, end_time):
        """Fetch historical earthquake data from USGS API"""
        try:
            params = {
                'format': 'geojson',
                'starttime': start_time.strftime('%Y-%m-%d'),
                'endtime': end_time.strftime('%Y-%m-%d'),
                'minmagnitude': 0
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return self._process_response(response.json())
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()

    def _process_response(self, data):
        """Process JSON response into DataFrame"""
        earthquakes = []
        for feature in data['features']:
            props = feature['properties']
            coords = feature['geometry']['coordinates']
            earthquakes.append({
                'id': props['ids'] if 'ids' in props else props['code'],
                'magnitude': props['mag'],
                'place': props['place'],
                'time': datetime.fromtimestamp(props['time'] / 1000.0),
                'depth': coords[2],
                'latitude': coords[1],
                'longitude': coords[0],
                'type': props['type']
            })
        
        return pd.DataFrame(earthquakes)

    def _check_major_earthquakes(self, data):
        """Check for new major earthquakes and return them"""
        if data.empty:
            return []
        
        major_quakes = data[data['magnitude'] >= self.major_earthquake_threshold]
        new_major_quakes = []
        
        for _, quake in major_quakes.iterrows():
            if quake['id'] not in self.last_major_earthquakes:
                self.last_major_earthquakes.add(quake['id'])
                new_major_quakes.append(quake)
        
        return new_major_quakes

    def get_new_major_earthquakes(self, data):
        """Return list of new major earthquakes since last check"""
        return self._check_major_earthquakes(data)
