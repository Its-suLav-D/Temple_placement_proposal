import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import json

class MapVisualization:
    def __init__(self, geo_json_file, chart_data):
        self.geo_json_file = geo_json_file
        self.chart_data = chart_data
        self.load_geo_json_data()
        self.prepare_data()

    def load_geo_json_data(self):
        with open(self.geo_json_file) as f:
            self.geo_json = json.load(f)

    def prepare_data(self):
        coordinates = self.geo_json['features'][30]['geometry']['coordinates']
        self.border_data = pd.DataFrame(
            [item for sublist in coordinates for item in sublist], 
            columns=['longitude', 'latitude']
        )
        self.path_data = [{'path': flat_list, 'name': 'Idaho'} for flat_list in coordinates]

    def get_churches_data(self):
        return pd.DataFrame({
            'latitude': [43.6150, 43.4919, 43.8231],
            'longitude': [-116.2023, -112.0405, -116.9008],
            'label': ['Church 1', 'Church 2', 'Church 3'],
            'type': 'church'
        })

    def get_temples_data(self):
        return pd.DataFrame({
            'latitude': [43.6629, 43.8250],
            'longitude': [-116.1633, -111.7892],
            'label': ['Temple 1', 'Temple 2'],
            'type': 'temple'
        })

    def render_map(self):
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=44.0682,
                longitude=-114.7420,
                zoom=6,
                pitch=50,
            ),
            layers=[
                self.get_border_layer(),
                self.get_churches_layer(),
                self.get_churches_label_layer(),
                self.get_temples_layer(),
                self.get_temples_label_layer()
            ],
            tooltip={
                'html': '<b>{label}</b>',
                'style': {
                    'color': 'white'
                }
            }
        ))

    def render_2d_map(self):
        churches = self.get_churches_data()
        churches["size"] = 20000 
        churches["color"] = [[0, 128, 0, 160] for _ in range(churches.shape[0])] 
        

        temples = self.get_temples_data()
        temples["size"] = 20000  
        temples["color"] = [[128, 0, 0, 160] for _ in range(temples.shape[0])]  
        

        self.border_data["size"] = 50  
        self.border_data["color"] = [[0, 0, 128, 160] for _ in range(self.border_data.shape[0])]  
        
  
        combined_data = pd.concat([self.border_data, churches, temples], ignore_index=True)
        

        st.map(combined_data, latitude='latitude', longitude='longitude', size='size', color='color')




    def get_border_layer(self):
        return pdk.Layer(
            'PathLayer',
            self.path_data,
            get_path='path',
            get_width=100,
            get_color=[180, 0, 200, 140],  
            pickable=True,
            width_scale=20,
            width_min_pixels=2
        )

    def get_churches_layer(self):
        return pdk.Layer(
            'HexagonLayer',
            data=self.chart_data,
            get_position='[lon, lat]',
            radius=1000,
            elevation_scale=20,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True
        )

    def get_churches_label_layer(self):
        return pdk.Layer(
            'TextLayer',
            self.get_churches_data(),
            get_position='[longitude, latitude]',
            get_text='label',
            get_size=16,
            get_color=[2, 2, 255],
            get_alignment_baseline="'bottom'"
        )

    def get_temples_layer(self):
        return pdk.Layer(
            'ColumnLayer',
            self.get_temples_data(),
            get_position='[longitude, latitude]',
            get_elevation=100000, 
            get_fill_color=[0, 0, 255, 140],  
            pickable=True,
            auto_highlight=True
        )

    def get_temples_label_layer(self):
        return pdk.Layer(
            'TextLayer',
            self.get_temples_data(),
            get_position='[longitude, latitude]',
            get_text='label',
            get_size=16,
            get_color=[5, 125, 5],
            get_alignment_baseline="'bottom'"
        )


if __name__ == "__main__":
    chart_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [43.6150, -116.2023],
        columns=['lat', 'lon']
    )
    viz = MapVisualization('gz_2010_us_040_00_500k.json', chart_data)
    viz.render_map()

    viz.render_2d_map()

    st.sidebar.subheader('View Church & Temple Locations')

    county = st.sidebar.selectbox(
        'County',
        ('Madison', 'Bonneville', 'Bannock', 'Bingham', 'Power', 'Jefferson', 'Fremont', 'Teton', 'Clark', 'Caribou', 'Bear Lake', 'Oneida', 'Franklin', 'Butte', 'Custer', 'Lemhi', 'Idaho', 'Blaine', 'Camas', 'Lincoln', 'Minidoka', 'Cassia', 'Jerome', 'Gooding', 'Twin Falls', 'Elmore', 'Ada', 'Boise', 'Gem', 'Payette', 'Washington', 'Valley', 'Canyon', 'Owyhee', 'Adams', 'Latah', 'Lewis', 'Nez Perce', 'Clearwater', 'Kootenai', 'Benewah', 'Shoshone', 'Boundary', 'Bonner', 'Idaho')
    )

    church_and_temple = st.sidebar.selectbox(
        'Church & Temple',
        ('Church', 'Temple')
    )