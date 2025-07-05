# from sklearn.ensemble import RandomForestRegressor
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import streamlit as st

# st.header("🔮 Predict Future Rape Cases (2023–2030)")
# st.markdown("This section uses Random Forest and estimated feature trends to predict rape cases through 2030.")

# # Load and prepare merged dataset
# def load_and_aggregate(filename, value_name, agg="sum"):
#     df = pd.read_csv(filename)
    
#     if "Sl. No." in df.columns:
#         df = df.drop(columns=["Sl. No."])

#     df = df.rename(columns={df.columns[0]: "State"})

#     # Melt wide to long
#     df_long = pd.melt(df, id_vars=["State"], var_name="Year", value_name=value_name)
#     df_long["Year"] = df_long["Year"].astype(int)

#     # Convert values to numeric (handle symbols like –, NA, etc.)
#     df_long[value_name] = pd.to_numeric(df_long[value_name], errors='coerce')

#     # Aggregate across states by year
#     if agg == "sum":
#         return df_long.groupby("Year", as_index=False)[value_name].sum()
#     elif agg == "mean":
#         return df_long.groupby("Year", as_index=False)[value_name].mean()

# def load_final_merged_df():
#     rape = load_and_aggregate("Rape.csv", "Rape_Cases", "sum")
#     literacy = load_and_aggregate("literacy_rate.csv", "Literacy_Rate", "mean")
#     unemployment = load_and_aggregate("unemployment_rate.csv", "Unemployment_Rate", "mean")
#     population = load_and_aggregate("population.csv", "Population", "sum")
#     income = load_and_aggregate("Per_Capita_Income.csv", "Income", "mean")

#     df = rape.merge(literacy, on="Year") \
#              .merge(unemployment, on="Year") \
#              .merge(population, on="Year") \
#              .merge(income, on="Year")

#     return df.dropna()

# # Train model on 2019–2022
# df = load_final_merged_df()
# features = ["Population", "Literacy_Rate", "Unemployment_Rate", "Income"]
# X = df[features]
# y = df["Rape_Cases"]

# model = RandomForestRegressor(n_estimators=100, random_state=42)
# model.fit(X, y)

# # Estimated trends for 2023–2030 (adjust as needed)
# years = list(range(2023, 2031))
# future_df = pd.DataFrame({
#     "Year": years,
#     "Population": np.linspace(1410000000, 1460000000, len(years)).astype(int),       # grows by ~10 million/year
#     "Literacy_Rate": np.linspace(75.0, 78.0, len(years)),                            # gradual literacy rise
#     "Unemployment_Rate": np.linspace(6.5, 5.5, len(years)),                          # slight improvement
#     "Income": np.linspace(135000, 160000, len(years)).astype(int)                   # steady income growth
# })

# # Predict rape cases
# X_future = future_df[features]
# future_df["Predicted_Rape_Cases"] = model.predict(X_future).astype(int)

# # Combine for plotting
# historical = df[["Year", "Rape_Cases"]].rename(columns={"Rape_Cases": "Cases"})
# predicted = future_df[["Year", "Predicted_Rape_Cases"]].rename(columns={"Predicted_Rape_Cases": "Cases"})

# historical["Type"] = "Actual"
# predicted["Type"] = "Predicted"
# combined = pd.concat([historical, predicted], ignore_index=True)

# # Line Plot
# st.subheader("📈 Rape Case Trend (2019–2030)")
# plt.figure(figsize=(10, 5))
# for label, grp in combined.groupby("Type"):
#     plt.plot(grp["Year"], grp["Cases"], marker='o', linestyle='--' if label=="Predicted" else '-', label=label)

# plt.xlabel("Year")
# plt.ylabel("Rape Cases")
# plt.title("Rape Case Predictions (2019–2030)")
# plt.legend()
# plt.grid(True)
# st.pyplot(plt)

# # Display predictions table
# st.subheader("📋 Predicted Rape Cases (2023–2030)")
# st.dataframe(future_df[["Year", "Predicted_Rape_Cases"]].set_index("Year"))




# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import PoissonRegressor

# st.set_page_config(layout="wide")
# st.title("🔮 Crime Prediction using Poisson Regression")

# # --- Crime file mapping --- #
# crime_files = {
#     "Rape": "Rape.csv",
#     "Murder": "Murder.csv",
#     "Kidnapping": "kidnapping.csv",
#     "Crime Against Children": "crimeAgainstChildren.csv",
#     "Dowry Death": "dowryDeaths.csv",
#     "Cybercrime": "cyberCrime.csv",
#     "Crime Against Women": "crimeAgainstWomen.csv",
#     "Dacoity": "dacoity.csv",
#     "Robbery": "robbery.csv",
#     "Violent Crimes": "violentCrimes.csv"
# }

# # --- Helper to reshape data --- #
# def melt_df(file, value_name):
#     df = pd.read_csv(file)
#     df = df.rename(columns={df.columns[0]: "State"})
#     df = df.melt(id_vars="State", var_name="Year", value_name=value_name)
#     df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
#     df[value_name] = pd.to_numeric(df[value_name], errors="coerce")
#     df["State"] = df["State"].str.strip().str.title()
#     return df.dropna()

# # --- Load and combine data --- #
# @st.cache_data
# def load_combined(crime_file):
#     crime = melt_df(crime_file, "Crime_Count")
#     literacy = melt_df("literacy_rate.csv", "Literacy_Rate")
#     unemp = melt_df("unemployment_rate.csv", "Unemployment_Rate")
#     pop = melt_df("population.csv", "Population")
#     income = melt_df("Per_Capita_Income.csv", "Income")

#     merged = crime.merge(literacy, on=["State", "Year"], how="inner") \
#                   .merge(unemp, on=["State", "Year"], how="inner") \
#                   .merge(pop, on=["State", "Year"], how="inner") \
#                   .merge(income, on=["State", "Year"], how="inner")

#     return merged.dropna()

# # --- Forecast a feature using linear regression --- #
# from sklearn.linear_model import LinearRegression

# def forecast_feature(df_state, feature, year):
#     feature_df = df_state[["Year", feature]].dropna()
#     model = LinearRegression()
#     model.fit(feature_df[["Year"]], feature_df[feature])
#     return float(model.predict([[year]])[0])

# # --- UI Selections --- #
# selected_crime = st.selectbox("🧭 Select Crime Type", list(crime_files.keys()))
# df = load_combined(crime_files[selected_crime])
# states = sorted([s for s in df["State"].unique() if "total" not in s.lower()])
# selected_state = st.selectbox("📍 Select State", states)
# selected_year = st.selectbox("📅 Select Future Year", list(range(2023, 2031)))

# # --- Filter for selected state --- #
# df_state = df[df["State"] == selected_state]

# # --- Prepare training data --- #
# X = df_state[["Year", "Literacy_Rate", "Unemployment_Rate", "Population", "Income"]]
# y = df_state["Crime_Count"]

# # --- Forecast future inputs --- #
# future_df = pd.DataFrame({
#     "Year": [selected_year],
#     "Literacy_Rate": [forecast_feature(df_state, "Literacy_Rate", selected_year)],
#     "Unemployment_Rate": [forecast_feature(df_state, "Unemployment_Rate", selected_year)],
#     "Population": [forecast_feature(df_state, "Population", selected_year)],
#     "Income": [forecast_feature(df_state, "Income", selected_year)]
# })

# st.subheader(f"📈 Forecasted Inputs for {selected_state} in {selected_year}")
# st.dataframe(future_df)

# # --- Train and predict with Poisson Regression --- #
# model = PoissonRegressor(max_iter=500)
# model.fit(X, y)
# raw_pred = model.predict(future_df)[0]
# prediction = int(np.round(raw_pred))

# # --- Display --- #
# st.subheader(f"🔮 Predicted {selected_crime} Cases in {selected_state} for {selected_year}")
# st.markdown(f"📉 Raw Model Output: `{raw_pred:.2f}`")
# st.markdown(f"✅ Final Prediction: **{prediction} cases**")

# # --- Plot --- #
# fig, ax = plt.subplots(figsize=(10, 5))
# ax.plot(df_state["Year"], df_state["Crime_Count"], marker='o', label="Historical")
# ax.plot([selected_year], [prediction], marker='s', color="green", label="Poisson Prediction")
# ax.set_title(f"{selected_state} - {selected_crime} Forecast ({selected_year})")
# ax.set_xlabel("Year")
# ax.set_ylabel("Crime Cases")
# ax.legend()
# st.pyplot(fig)

# # --- Download --- #
# result_df = future_df.copy()
# result_df["Predicted_Crime_Cases"] = prediction
# csv = result_df.to_csv(index=False).encode("utf-8")
# st.download_button("📥 Download Prediction", data=csv, file_name="crime_prediction_poisson.csv", mime="text/csv")



import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.holtwinters import Holt
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
      <a href="/CorrelationStateWise" target="_self">Correlation (State Wise)</a>
      <a href="/Heatmap" target="_self">Heatmap</a>
      <a class="active" href="/Prediction" target="_self">Prediction</a>
    </div>
""", unsafe_allow_html=True) 

st.title("📈 Crime Forecast App (Random Forest + Scaled Features)")

# --- Crime files mapping ---
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

# --- Load and reshape function ---
def melt_df(file, value_name):
    df = pd.read_csv(file)
    df.rename(columns={df.columns[0]: "State"}, inplace=True)
    df = df.melt(id_vars=["State"], var_name="Year", value_name=value_name)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df[value_name] = pd.to_numeric(df[value_name], errors="coerce")
    df["State"] = df["State"].str.strip().str.title()
    return df.dropna()

# --- Forecast using Holt’s method ---
def forecast_holt(df_state, feature, year):
    df_feat = df_state[["Year", feature]].dropna().sort_values("Year")
    if len(df_feat) < 3:
        return float(df_feat[feature].mean())
    values = df_feat[feature].values
    model = Holt(values)
    fit = model.fit()
    steps = year - int(df_feat["Year"].max())
    forecast = fit.forecast(steps) if steps > 0 else [values[-1]]
    pred = forecast[-1]

    if "literacy" in feature.lower():
        pred = np.clip(pred, values[-1], 100)
    elif "unemployment" in feature.lower():
        pred = np.clip(pred, 0, 50)
    else:
        pred = max(pred, 0)
    return round(pred, 2)

# --- Load and merge all files ---
@st.cache_data
def load_combined(crime_file):
    crime = melt_df(crime_file, "Crime_Count")
    literacy = melt_df("literacy_rate.csv", "Literacy_Rate")
    unemp = melt_df("unemployment_rate.csv", "Unemployment_Rate")
    pop = melt_df("population.csv", "Population")
    income = melt_df("Per_Capita_Income.csv", "Income")

    merged = crime.merge(literacy, on=["State", "Year"], how="inner") \
                  .merge(unemp, on=["State", "Year"], how="inner") \
                  .merge(pop, on=["State", "Year"], how="inner") \
                  .merge(income, on=["State", "Year"], how="inner")
    return merged.dropna()

# --- UI Selections ---
crime_type = st.selectbox("🧭 Select Crime Type", list(crime_files.keys()))
df = load_combined(crime_files[crime_type])
states = sorted(df["State"].unique())
selected_state = st.selectbox("📍 Select State", states)

# --- Filter for selected state ---
df_state = df[df["State"] == selected_state].copy()

# --- Forecast for multiple years ---
future_years = list(range(2023, 2031))
future_data = []

for year in future_years:
    row = {
        "Year": year,
        "Literacy_Rate": forecast_holt(df_state, "Literacy_Rate", year),
        "Unemployment_Rate": forecast_holt(df_state, "Unemployment_Rate", year),
        "Population": forecast_holt(df_state, "Population", year),
        "Income": forecast_holt(df_state, "Income", year)
    }
    future_data.append(row)

future_df = pd.DataFrame(future_data)

# --- Show Forecasted Inputs ---
st.subheader(f"📊 Forecasted Inputs for {selected_state} (2023–2030)")
st.dataframe(future_df)

# --- Train ML Model with Scaling ---
X = df_state[["Year", "Literacy_Rate", "Unemployment_Rate", "Population", "Income"]]
y = df_state["Crime_Count"]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
future_scaled = scaler.transform(future_df)

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_scaled, y)

# --- Predict for all future years ---
predictions = model.predict(future_scaled)
future_df["Predicted_Crime_Count"] = predictions.astype(int)

# --- Plot Historical + Predicted ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_state["Year"], df_state["Crime_Count"], marker='o', label="Historical")
ax.plot(future_df["Year"], future_df["Predicted_Crime_Count"], marker='s', color='red', label="Prediction")
ax.set_title(f"{selected_state} - {crime_type} Forecast (2023–2030)")
ax.set_xlabel("Year")
ax.set_ylabel("Crime Cases")
ax.legend()
st.pyplot(fig)

# --- Show prediction table ---
st.subheader("📈 Forecasted Crime Cases (2023–2030)")
st.dataframe(future_df)

# --- Download ---
csv = future_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Forecast CSV", csv, "crime_forecast_random_forest.csv", "text/csv")




