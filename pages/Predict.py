from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

st.header("🔮 Predict Future Rape Cases (2023–2030)")
st.markdown("This section uses Random Forest and estimated feature trends to predict rape cases through 2030.")

# Load and prepare merged dataset
def load_and_aggregate(filename, value_name, agg="sum"):
    df = pd.read_csv(filename)
    
    if "Sl. No." in df.columns:
        df = df.drop(columns=["Sl. No."])

    df = df.rename(columns={df.columns[0]: "State"})

    # Melt wide to long
    df_long = pd.melt(df, id_vars=["State"], var_name="Year", value_name=value_name)
    df_long["Year"] = df_long["Year"].astype(int)

    # Convert values to numeric (handle symbols like –, NA, etc.)
    df_long[value_name] = pd.to_numeric(df_long[value_name], errors='coerce')

    # Aggregate across states by year
    if agg == "sum":
        return df_long.groupby("Year", as_index=False)[value_name].sum()
    elif agg == "mean":
        return df_long.groupby("Year", as_index=False)[value_name].mean()

def load_final_merged_df():
    rape = load_and_aggregate("Rape.csv", "Rape_Cases", "sum")
    literacy = load_and_aggregate("literacy_rate.csv", "Literacy_Rate", "mean")
    unemployment = load_and_aggregate("unemployment_rate.csv", "Unemployment_Rate", "mean")
    population = load_and_aggregate("population.csv", "Population", "sum")
    income = load_and_aggregate("Per_Capita_Income.csv", "Income", "mean")

    df = rape.merge(literacy, on="Year") \
             .merge(unemployment, on="Year") \
             .merge(population, on="Year") \
             .merge(income, on="Year")

    return df.dropna()

# Train model on 2019–2022
df = load_final_merged_df()
features = ["Population", "Literacy_Rate", "Unemployment_Rate", "Income"]
X = df[features]
y = df["Rape_Cases"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Estimated trends for 2023–2030 (adjust as needed)
years = list(range(2023, 2031))
future_df = pd.DataFrame({
    "Year": years,
    "Population": np.linspace(1410000000, 1460000000, len(years)).astype(int),       # grows by ~10 million/year
    "Literacy_Rate": np.linspace(75.0, 78.0, len(years)),                            # gradual literacy rise
    "Unemployment_Rate": np.linspace(6.5, 5.5, len(years)),                          # slight improvement
    "Income": np.linspace(135000, 160000, len(years)).astype(int)                   # steady income growth
})

# Predict rape cases
X_future = future_df[features]
future_df["Predicted_Rape_Cases"] = model.predict(X_future).astype(int)

# Combine for plotting
historical = df[["Year", "Rape_Cases"]].rename(columns={"Rape_Cases": "Cases"})
predicted = future_df[["Year", "Predicted_Rape_Cases"]].rename(columns={"Predicted_Rape_Cases": "Cases"})

historical["Type"] = "Actual"
predicted["Type"] = "Predicted"
combined = pd.concat([historical, predicted], ignore_index=True)

# Line Plot
st.subheader("📈 Rape Case Trend (2019–2030)")
plt.figure(figsize=(10, 5))
for label, grp in combined.groupby("Type"):
    plt.plot(grp["Year"], grp["Cases"], marker='o', linestyle='--' if label=="Predicted" else '-', label=label)

plt.xlabel("Year")
plt.ylabel("Rape Cases")
plt.title("Rape Case Predictions (2019–2030)")
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Display predictions table
st.subheader("📋 Predicted Rape Cases (2023–2030)")
st.dataframe(future_df[["Year", "Predicted_Rape_Cases"]].set_index("Year"))


