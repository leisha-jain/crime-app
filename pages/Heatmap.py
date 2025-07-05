import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        
        .topnav {
            background-color: #333;
            overflow: hidden;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 50px;
            z-index: 999999;
        }

        .topnav a {
            float: left;
            color: #f2f2f2;
            text-align: center;
            padding: 14px 26px;
            text-decoration: none;
            font-size: 17px;
        }

        .topnav a:hover {
            background-color: #ddd;
            color: black;
        }

        .topnav a.active {
            background-color: #04AA6D;
            color: white;
        }

        /* Push content below navbar */
        .main .block-container {
            padding-top: 80px; /* increased from 60 to 80 for more spacing */
        }
            
        
    </style>

    <div class="topnav">
      <a href="/" target="_self">Home</a>
      <a href="/Bar_Chart" target="_self">Bar Chart</a>
      <a href="/CorrelationAllIndia" target="_self">Correlation (All India)</a>
      <a href="/CorrelationStateWise" target="_self">Correlation (State Wise)</a>
      <a class="active" href="/Heatmap" target="_self">Heatmap</a>
      <a href="/Prediction" target="_self">Prediction</a>
    </div>
""", unsafe_allow_html=True)

st.title("India Crime Rate Heatmap")

# Load India GeoJSON
@st.cache_data
def load_geojson():
    with open("india_states.geojson", "r") as f:
        gj = json.load(f)
    
    return gj


geojson = load_geojson()

# Crime file dictionary (label → filename)
crime_files = {
    "Rape": "rape.csv",
    "Murder": "murder.csv",
    "Kidnapping": "kidnapping.csv",
    "Crime Against Children": "crimeAgainstChildren.csv",
    "Dowry Death": "dowryDeaths.csv",
    "Cybercrime": "cyberCrime.csv",
    "Crime Against Women": "crimeAgainstWomen.csv",
    "Dacoity": "dacoity.csv",
    "Robbery": "robbery.csv",
    "Violent Crimes": "violentCrimes.csv"
}

years = [2019, 2020, 2021, 2022]

# Sidebar: select crime + year
selected_crime = st.selectbox("Select Crime Type", list(crime_files.keys()))
selected_year = st.selectbox("Select Year", years)

# Load selected crime file
@st.cache_data
def load_crime_data(filename):
    df = pd.read_csv(filename)
    df = df.rename(columns={df.columns[0]: "State"})
    return df

crime_df = load_crime_data(crime_files[selected_crime])

# Load population
@st.cache_data
def load_population():
    df = pd.read_csv("population.csv")
    df = df.rename(columns={df.columns[0]: "State"})
    return df

pop_df = load_population()



# Merge and calculate crime rate
merged = pd.merge(
    crime_df[["State", str(selected_year)]],
    pop_df[["State", str(selected_year)]],
    on="State", how="inner"
)

merged.columns = ["State", "Crime_Count", "Population"]
merged["Crime_Count"] = pd.to_numeric(merged["Crime_Count"], errors="coerce")
merged["Population"] = pd.to_numeric(merged["Population"], errors="coerce") * 1000
merged = merged.dropna(subset=["Crime_Count", "Population"])
merged["Crime_Rate"] = (merged["Crime_Count"] / merged["Population"]) * 100000
merged["Crime_Rate"] = merged["Crime_Rate"].round(2)

crime_df["State"] = crime_df["State"].str.strip().str.title()
pop_df["State"] = pop_df["State"].str.strip().str.title()
merged["State"] = merged["State"].str.strip().str.title()

if selected_year == 2019:
    jk_row = merged[merged["State"] == "Jammu And Kashmir"]
    if not jk_row.empty:
        ladakh_row = jk_row.copy()
        ladakh_row["State"] = "Ladakh"
        merged = pd.concat([merged, ladakh_row], ignore_index=True)

# Add hover text override
merged["Hover"] = merged["State"]
if selected_year == 2019:
    merged.loc[merged["State"] == "Ladakh", "Hover"] = "Jammu and Kashmir"


merged["State"] = merged["State"].replace({
    "Jammu And Kashmir": "Jammu and Kashmir"
})



# Plot heatmap
fig = go.Figure(go.Choroplethmapbox(
    geojson=geojson,
    locations=merged["State"],
    z=merged["Crime_Rate"],
    text=merged["Hover"],  # 🟢 used for hover
    featureidkey="properties.st_nm",
    colorscale="Reds",
    marker_opacity=0.75,
    marker_line_width=0,
    colorbar_title="Rate<br>per 100k"
))

fig.update_traces(hovertemplate="%{text}<br>Crime Rate: %{z}")


fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=3.5,
    mapbox_center={"lat": 22.9734, "lon": 78.6569},
    margin={"r":0,"t":30,"l":0,"b":0},
    title=f"{selected_crime} Rate per 100,000 Population in {selected_year}"
)

st.plotly_chart(fig, use_container_width=True)


# Optional: data table
with st.expander("📋 Show Data Table"):
    st.dataframe(merged[["State", "Crime_Count", "Population", "Crime_Rate"]])


