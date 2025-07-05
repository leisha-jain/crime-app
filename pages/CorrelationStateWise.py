import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
      <a class="active" href="/CorrelationStateWise" target="_self">Correlation (State Wise)</a>
      <a href="/Heatmap" target="_self">Heatmap</a>
      <a href="/Prediction" target="_self">Prediction</a>
    </div>
""", unsafe_allow_html=True) 

st.title("Correlation Between Crime and Socioeconomic Factors(State Wise)")

# --- Config ---
crime_files = {
    "Rape": "Rape.csv",
    "Murder": "Murder.csv",
    "Kidnapping": "kidnapping.csv",
    "Crime Against Children": "crimeAgainstChildren.csv",
    "Dowry Death": "dowryDeaths.csv",
    "Cybercrime": "cyberCrime.csv",
    "Crime Against Women": "crimeAgainstWomen.csv",
    "Dacoity": "dacoity.csv",
    "Robbery": "robbery.csv",
    "Violent Crimes": "violentCrimes.csv"
}

factor_files = {
    "Literacy Rate": "literacy_rate.csv",
    "Unemployment Rate": "unemployment_rate.csv",
    "Income": "Per_Capita_Income.csv",
    "Population": "population.csv"
}

years = [2019, 2020, 2021, 2022]

# --- Sidebar: Selections ---
selected_crime = st.selectbox(" Select Crime Type", list(crime_files.keys()))
selected_factor = st.selectbox("Select Socioeconomic Factor", list(factor_files.keys()))

# Load and filter state list
state_list = pd.read_csv("Rape.csv").iloc[:, 0].dropna().unique()
state_list = [s.strip().title() for s in state_list if "total" not in s.lower()]
state_list = sorted(set(state_list))  # remove duplicates

# Use filtered list directly
selected_state = st.selectbox(" Select a State", state_list)


# --- Load & Melt Helper ---
def load_and_melt(filename, value_name):
    df = pd.read_csv(filename)
    if "Sl. No." in df.columns:
        df = df.drop(columns=["Sl. No."])
    df = df.rename(columns={df.columns[0]: "State"})
    df.columns = df.columns.astype(str)
    df = pd.melt(df, id_vars=["State"], var_name="Year", value_name=value_name)
    df["Year"] = df["Year"].str.replace(".0", "").astype(int)
    df[value_name] = pd.to_numeric(df[value_name], errors="coerce")
    df["State"] = df["State"].str.strip().str.title()
    return df.dropna()









# --- Load Data ---
crime_df = load_and_melt(crime_files[selected_crime], "Crime_Count")
factor_df = load_and_melt(factor_files[selected_factor], selected_factor)








# --- Merge ---
merged = pd.merge(crime_df, factor_df, on=["State", "Year"], how="inner")





# --- Filter by State ---
df_state = merged[merged["State"] == selected_state].dropna()








# --- Plot and Correlation ---
if df_state.empty:
    st.warning("No data available for this state and selection.")
else:
    st.subheader(f"{selected_state}: {selected_crime} vs {selected_factor} ")

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.set_xlabel("Year")
    ax1.set_ylabel(selected_crime, color="red")
    ax1.plot(df_state["Year"], df_state["Crime_Count"], marker="o", color="red", label=selected_crime)
    ax1.tick_params(axis="y", labelcolor="red")

    ax2 = ax1.twinx()
    ax2.set_ylabel(selected_factor, color="blue")
    ax2.plot(df_state["Year"], df_state[selected_factor], marker="s", color="blue", label=selected_factor)
    ax2.tick_params(axis="y", labelcolor="blue")

    fig.tight_layout()
    st.pyplot(fig)


    



    # Correlation
    corr = df_state["Crime_Count"].corr(df_state[selected_factor])
    st.markdown(f"### Correlation Coefficient: **{corr:.3f}**")

    if abs(corr) >= 0.7:
        strength = "strong"
    elif abs(corr) >= 0.4:
        strength = "moderate"
    elif abs(corr) >= 0.2:
        strength = "weak"
    else:
        strength = "very weak or no"

    st.markdown(f" This indicates a **{strength} correlation** between **{selected_crime}** and **{selected_factor}** in **{selected_state}**.")

    with st.expander(" Show Data Table"):
        st.dataframe(df_state)

    # Optional CSV download
    csv = df_state.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name=f"{selected_crime}_{selected_factor}_{selected_state}.csv", mime="text/csv")
