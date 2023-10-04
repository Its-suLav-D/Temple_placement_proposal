# import streamlit as st
# import pandas as pd
# import numpy as np 


# PARQUET_FILE_PATH = "./data/temple_details.parquet"


# def load_parquet_file(path):
#     df = pd.read_parquet(path)
#     return df

# def main():
#     df = load_parquet_file(PARQUET_FILE_PATH)

#     places  = load_parquet_file("./data/places.parquet")


#     df_filtered = df[df['country'] == 'United States']


#     condition = (
#         (df_filtered['city'] == 'Idaho') |
#         (df_filtered['stateRegion'] == ' Idaho') |
#         (df_filtered['city'].isna()) |
#         (df_filtered['temple'] == 'Burley Idaho Temple')
#     )
#     df_idaho_temples = df_filtered[condition]


#     df_sorted = df_idaho_temples.sort_values(by='status')

#     st.write(df_sorted.shape)


#     st.write(df_sorted)


#     places = places.drop(columns=['open_hours'])

#     churches = places[
#         (places['location_name'] == "The Church of Jesus Christ of Latter day Saints") & 
#         (places['region'] == "ID")
#     ]

#     st.write(churches.shape)
#     st.write(churches)

# if __name__ == "__main__":
#     main()
