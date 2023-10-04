import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import json

def load_parquet_file(path):
    df = pd.read_parquet(path)
    return df

class MapVisualization:
    def __init__(self, geo_json_file, chart_data):
        self.geo_json_file = geo_json_file
        self.chart_data = chart_data
        self.df_places = None
        self.df_temples = None
        self.load_geo_json_data()
        self.load_data_from_parquet()
        self.prepare_data()

    def load_geo_json_data(self):
        with open(self.geo_json_file) as f:
            self.geo_json = json.load(f)

    def load_data_from_parquet(self):
        df = load_parquet_file("./data/temple_details.parquet")
        df_filtered = df[df['country'] == 'United States']
        condition = (
            (df_filtered['city'] == 'Idaho') |
            (df_filtered['stateRegion'] == ' Idaho') |
            (df_filtered['city'].isna()) |
            (df_filtered['temple'] == 'Burley Idaho Temple')
        )
        self.df_temples = df_filtered[condition]

        places = load_parquet_file("./data/places.parquet")
        places.drop(columns=['open_hours'])
        self.df_places = places[
            (places['location_name'] == "The Church of Jesus Christ of Latter day Saints") & 
            (places['region'] == "ID")
        ]

    def update_temple_coordinates(self, temple_name, new_lat, new_lon):

        mask = self.df_temples['temple'] == temple_name
        if not mask.any():
            print(f"No temple named '{temple_name}' found.")
            return
        
        self.df_temples.loc[mask, 'lat'] = new_lat
        self.df_temples.loc[mask, 'long'] = new_lon
        print(f"Coordinates for '{temple_name}' updated.")


    def drop_temple_by_name(self, temple_name):
        if temple_name in self.df_temples['temple'].values:
            self.df_temples = self.df_temples[self.df_temples['temple'] != temple_name]
        else:
            print(f"Temple {temple_name} not found in the dataset!")


    def prepare_data(self):
        coordinates = self.geo_json['features'][30]['geometry']['coordinates']
        self.border_data = pd.DataFrame(
            [item for sublist in coordinates for item in sublist], 
            columns=['longitude', 'latitude']
        )
        self.path_data = [{'path': flat_list, 'name': 'Idaho'} for flat_list in coordinates]

    def get_churches_data(self):
        churches = pd.DataFrame({
            'latitude': self.df_places['latitude'].tolist(),
            'longitude': self.df_places['longitude'].tolist(),
            'label': self.df_places['city'].tolist(),
            'type': 'church'
        })
        return churches

    def get_temples_data(self, status="ALL"):
        if status != 'ALL':
            filtered_temples = self.df_temples[self.df_temples['status'] == status]
        else:
            filtered_temples = self.df_temples

        return pd.DataFrame({
            'latitude': filtered_temples['lat'].tolist(),
            'longitude': filtered_temples['long'].tolist(),
            'label': filtered_temples['temple'].tolist(),
            'type': 'temple'
        })


    def render_map(self, status="ALL"):
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
                # self.get_churches_label_layer(),
                self.get_temples_layer(status),
                self.get_temples_label_layer(status)
            ],
            tooltip={
                'text': '{label}'
            }
        ))

    def render_2d_map(self, status="ALL"):
        churches = self.get_churches_data()
        churches["size"] = 10000 
        churches["color"] = [[0, 128, 0, 160] for _ in range(churches.shape[0])] 
        

        temples = self.get_temples_data(status)
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
            'ColumnLayer',
            data=self.get_churches_data(),
            get_position='[longitude, latitude]',
            radius=5000,
            elevation_scale=10,
            elevation_range=[0, 1000],
            pickable=True,
            get_color=[248, 131, 121],
            auto_highlight=True,
        )


    def get_churches_label_layer(self):
        return pdk.Layer(
            'TextLayer',
            self.get_churches_data(),
            get_position='[longitude, latitude]',
            get_text='label',
            get_size=5,
            get_color=[2, 50, 255],
            get_alignment_baseline="'bottom'"
        )

    def get_temples_layer(self, status="ALL"):
        return pdk.Layer(
            'ColumnLayer',
            self.get_temples_data(status),
            get_position='[longitude, latitude]',
            get_elevation=100000, 
            radius=5000,
            get_fill_color=[0, 0, 255, 140],  
            pickable=True,
            auto_highlight=True
        )

    def get_temples_label_layer(self, status="ALL"):
        return pdk.Layer(
            'TextLayer',
            self.get_temples_data(status),
            get_position='[longitude, latitude]',
            get_text='label',
            get_size=10,
            get_color=[5, 125, 5],
            get_alignment_baseline="'bottom'"
        )


if __name__ == "__main__":

    st.title("Strategic Importance of Visualization")
    st.write("""
    By visualizing the distribution of existing temples and churches, several insights can be derived:

    1. **Density Analysis:** Areas with a high density of churches but few temples might indicate regions with substantial membership but limited temple accessibility. These are areas where a significant number of members might be traveling long distances to reach a temple.

    2. **Gap Analysis:** Visualizing can highlight regions where neither temples nor churches exist. These could be potential areas of expansion, or they might signify regions that are currently underserved.

    3. **Proximity Analysis:** By mapping the proximity of temples to churches, it becomes easier to understand member accessibility. In vast regions, if members have to travel long distances, it might become a hindrance to their temple attendance.

    4. **Trend Analysis:** Differentiating temples based on their status (e.g., ANNOUNCED, CONSTRUCTION, OPERATING) provides a visual trend of the church's growth and its focus areas in specific regions. 

    Armed with these visual insights, we can now leverage them to power our machine learning models.
    """)

    chart_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [43.6150, -116.2023],
        columns=['lat', 'lon']
    )
    viz = MapVisualization('gz_2010_us_040_00_500k.json', chart_data)
    viz.update_temple_coordinates('Burley Idaho Temple', 42.5266, -113.7651)
    viz.update_temple_coordinates('Montpelier Idaho Temple', 42.3180, -111.3017)
    viz.update_temple_coordinates('Teton River Idaho Temple',43.855150,-111.778320 )

    selected_status = st.sidebar.selectbox(
        'Select Temple Status',
        ['ALL', 'ANNOUNCED', 'CONSTRUCTION', 'OPERATING']
    )

    viz.render_map(selected_status)
    viz.render_2d_map(selected_status)


    st.title("Leveraging Visual Insights for ML Predictions")
    st.write("""
    The insights derived from visualization can be transformed into actionable features, setting the foundation for predictive ML models:

    1. **Feature Engineering:** The density of churches in temple-deficient areas can become a numeric feature, potentially indicating regions ripe for new temple placements.

    2. **Spatial Features:** Distance metrics, such as the average distance between churches and the nearest temple, can provide quantitative measures for accessibility.

    3. **Temporal Features:** Observing the progression of temple statuses over time (e.g., from ANNOUNCED to CONSTRUCTION to OPERATING) can aid in time-series forecasting of temple placements.

    4. **Categorical Encoding:** Regions, church densities, and other categorical data can be transformed into numerical values suitable for ML algorithms.

    By integrating these features into machine learning models, we enhance their ability to predict future temple placements accurately. Such predictions can guide strategic decisions, ensuring resources are allocated effectively and members' needs are met.
    """)

