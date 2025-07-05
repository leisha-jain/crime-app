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
      <a class="active" href="/CorrelationAllIndia" target="_self">Correlation (All India)</a>
      <a href="/CorrelationStateWise" target="_self">Correlation (State Wise)</a>
      <a href="/Heatmap" target="_self">Heatmap</a>
      <a href="/Prediction" target="_self">Prediction</a>
    </div>
""", unsafe_allow_html=True) 

st.title("Correlation Between Crime and Socioeconomic Factors (All India)")

# --- Crime file mapping --- #
crime_files = {
    "Rape": "Rape.csv",
    "Murder": "Murder.csv",
    "Kidnapping": "Kidnapping.csv",
    "Crime Against Children": "crimeAgainstChildren.csv",
    "Dowry Death": "dowryDeaths.csv",
    "Cybercrime": "cyberCrime.csv",
    "Crime Against Women": "crimeAgainstWomen.csv",
    "Dacoity": "dacoity.csv",
    "Robbery": "robbery.csv",
    "Violent Crimes": "violentCrimes.csv"
}

# --- Function to load, clean, melt, and aggregate --- #
def load_aggregate_csv(filename, value_name, agg="sum"):
    df = pd.read_csv(filename)

    # Rename first column to "State"
    df = df.rename(columns={df.columns[0]: "State"})

    # Normalize state names
    df["State"] = df["State"].astype(str).str.strip().str.title()
    df["State"] = df["State"].replace({
        "Total State(S)": "Total",
        "Total States(S)": "Total",
        "Total (All India)": "Total",
        "Total Ut(S)": "Total",
        "Total All India":"Total"
    })

    # Drop total rows (we want to aggregate manually)
    df = df[~df["State"].str.contains("Total", case=False, na=False)]
    df = df[~df["State"].str.contains("All India", case=False, na=False)]

    # Melt to long format
    df_long = pd.melt(df, id_vars=["State"], var_name="Year", value_name=value_name)
    df_long["Year"] = pd.to_numeric(df_long["Year"], errors="coerce")
    df_long[value_name] = pd.to_numeric(df_long[value_name], errors="coerce")

    # Group by year
    if agg == "sum":
        return df_long.groupby("Year", as_index=False)[value_name].sum()
    elif agg == "mean":
        return df_long.groupby("Year", as_index=False)[value_name].mean()

# --- Sidebar selectors --- #
selected_crime = st.selectbox(" Select Crime Type", list(crime_files.keys()))
selected_factor = st.selectbox(" Select Socioeconomic Factor", ["Literacy_Rate", "Unemployment_Rate", "Population", "Income"])

# --- Load aggregated national data --- #
crime_data = load_aggregate_csv(crime_files[selected_crime], "Crime_Cases", agg="sum")
literacy_avg = load_aggregate_csv("literacy_rate.csv", "Literacy_Rate", agg="mean")
unemp_avg = load_aggregate_csv("unemployment_rate.csv", "Unemployment_Rate", agg="mean")
pop_total = load_aggregate_csv("population.csv", "Population", agg="sum")
income_avg = load_aggregate_csv("Per_Capita_Income.csv", "Income", agg="mean")

# --- Merge on year --- #
df = crime_data.merge(literacy_avg, on="Year", how="left") \
               .merge(unemp_avg, on="Year", how="left") \
               .merge(pop_total, on="Year", how="left") \
               .merge(income_avg, on="Year", how="left")

df = df[df["Year"] >= 2019]


df = df.dropna(subset=["Crime_Cases", selected_factor])  # Clean up missing values

# --- Line Chart --- #
st.subheader(f"{selected_crime} Cases vs {selected_factor.replace('_', ' ')} (All India)")

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.set_xlabel("Year")
ax1.set_ylabel(f"{selected_crime} Cases", color="red")
ax1.plot(df["Year"], df["Crime_Cases"], marker="o", color="red", label="Crime")
ax1.tick_params(axis="y", labelcolor="red")

ax2 = ax1.twinx()
ax2.set_ylabel(selected_factor.replace("_", " "), color="blue")
ax2.plot(df["Year"], df[selected_factor], marker="s", color="blue", label=selected_factor)
ax2.tick_params(axis="y", labelcolor="blue")

fig.tight_layout()
st.pyplot(fig)

# --- Correlation --- #
if len(df) >= 2:
    corr = df["Crime_Cases"].corr(df[selected_factor])
    st.markdown(f"### Pearson Correlation Coefficient: **`{corr:.3f}`**")

    if abs(corr) >= 0.7:
        strength = "strong"
    elif abs(corr) >= 0.4:
        strength = "moderate"
    elif abs(corr) >= 0.2:
        strength = "weak"
    else:
        strength = "very weak or no"

    st.markdown(f" This indicates a **{strength} correlation** between **{selected_crime.lower()} cases** and **{selected_factor.replace('_', ' ')}**.")
else:
    st.warning("⚠️ Not enough data to calculate correlation.")

# --- Data Table --- #
with st.expander(" Show All-India Yearly Data"):
    st.dataframe(df)

