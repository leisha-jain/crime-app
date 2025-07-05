import streamlit as st

# Set wide layout
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Top navbar using HTML + CSS
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
      <a class="active" href="/">Home</a>
      <a href="/Bar_Chart" target="_self">Bar Chart</a>
      <a href="/CorrelationAllIndia" target="_self">Correlation (All India)</a>
      <a href="/CorrelationStateWise" target="_self">Correlation (State Wise)</a>
      <a href="/Heatmap" target="_self">Heatmap</a>
      <a href="/Prediction" target="_self">Prediction</a>
    </div>
""", unsafe_allow_html=True)

# --- Page Content ---
col1, col2 = st.columns([1, 1])
with col1:
    st.image("searching.png", width=80)  # map/magnifier icon

    st.markdown("<h1 style='margin-top: 10px; font-size:50px '>Crime Analysis</h1>", unsafe_allow_html=True)


with col2:
    st.markdown("<h2 style='margin-top: 10px; font-size:30px '></h2>", unsafe_allow_html=True)
    st.image("crime_analysis.jpg", width=1000)  # crime-related image
    





# Section title
st.markdown("""
    <div style=' padding: 50px 0;'>
        <h2 style='text-align: center; font-size: 36px; font-weight: 600; margin-top: 20px;'>
            Crime Analysis Capabilities
        </h2>
    </div>
""", unsafe_allow_html=True)

# Icons with captions using Streamlit layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    
    
    
    st.image("icons/bar-chart.png", width=80)
    st.markdown("<p style='font-size:18px;'>See Bar Charts</p>", unsafe_allow_html=True)
    


with col2:
    
    st.image("icons/correlation.png", width=80)
    st.markdown("<p style=' font-size:18px;'>Analyze Correlation</p>", unsafe_allow_html=True)
    
with col3:
    
    st.image("icons/india.png", width=70)
    st.markdown("<p style=' font-size:18px;'>See interactive HeatMaps</p>", unsafe_allow_html=True)
    
with col4:
    
    st.image("icons/predictive-chart.png", width=70)
    st.markdown("<p style='font-size:18px;'>Predict for future years</p>", unsafe_allow_html=True)
    





