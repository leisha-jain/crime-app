# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# from streamlit_folium import folium_static
# import geopandas as gpd
# import json
# import plotly.express as px

# from streamlit_option_menu import option_menu





# # Load shapefile
# gdf = gpd.read_file("india-polygon.shp")

# # Save as GeoJSON
# gdf.to_file("india_states.geojson", driver="GeoJSON")


# # Streamlit app title
# st.title("India Crime Heatmap for 2021")

# # Load crime data
# @st.cache_data
# def load_data():
#     df = pd.read_excel("crimes.xlsx")
#     return df

# @st.cache_data
# def load_geojson():
#     with open("india_states.geojson", "r") as file:
#         geojson = json.load(file)
#     return geojson

# df = load_data()
# geojson = load_geojson()

# # Select crime type
# crime_types = df.columns[1:]  # assuming first column is State
# crime_type = st.selectbox("Select Crime Type", crime_types)

# # Filter data
# filtered = df[["State", crime_type]]
# filtered.columns = ["State", "Rate"]



# # Plot
# geojson_state_key ="st_nm"



# fig = go.Figure(go.Choroplethmapbox(
#     geojson=geojson,
#     locations=df["State"],
#     z=df[crime_type],
#     featureidkey=f"properties.{geojson_state_key}",  # Adjust if different
#     colorscale="OrRd",
#     marker_opacity=0.7,
#     marker_line_width=0
# ))

# fig.update_layout(
#     mapbox_style="carto-positron",
#     mapbox_zoom=3,
#     mapbox_center={"lat": 22.9734, "lon": 78.6569},  # center of India
#     margin={"r":0,"t":30,"l":0,"b":0},
#     title=f"{crime_type} Rates Across Indian States"
# )

# st.plotly_chart(fig)

import streamlit as st
from streamlit_option_menu import option_menu



import streamlit as st
from PIL import Image

st.set_page_config(page_title="India Crime Dashboard", layout="wide")

# --- Banner ---
st.markdown("<h1 style='text-align: center;'>Crime Data Analysis</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Visualizing crime trends across Indian states</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- Description Section ---
st.markdown("### Welcome!")
st.write("""
This interactive dashboard lets you explore and analyze crime data across India. 
View heatmaps, top 5 crime-affected states, and draw insights from trends in crimes.
""")

