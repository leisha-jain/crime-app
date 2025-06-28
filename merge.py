import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Step 1: Load and reshape Rape data ---
rape_df = pd.read_csv("Rape.csv")
rape_df = rape_df.rename(columns={"State/UT": "State"})
rape_df = rape_df.drop(columns=["Sl. No."])
rape_long_df = pd.melt(rape_df, id_vars=["State"], var_name="Year", value_name="Rape")
rape_long_df["Year"] = rape_long_df["Year"].astype(int)

# --- Step 2: Load and reshape Literacy Rate data ---
literacy_df = pd.read_excel("literacy_rate.xlsx")
literacy_long_df = pd.melt(literacy_df, id_vars=["State"], var_name="Year", value_name="Literacy_Rate")
literacy_long_df["Year"] = literacy_long_df["Year"].astype(int)

# --- Step 3: Load and reshape Population data ---
pop_df = pd.read_excel("population.xlsx", skiprows=2, usecols=[0,1,2,3])  # Adjust as needed
pop_df.columns = ["State", "2019", "2020", "2021"]
pop_long_df = pd.melt(pop_df, id_vars=["State"], var_name="Year", value_name="Population")
pop_long_df["Year"] = pop_long_df["Year"].astype(int)
pop_long_df["Population"] = pd.to_numeric(pop_long_df["Population"], errors="coerce")

# --- Step 4: Load and reshape Unemployment data ---
unemp_df = pd.read_excel("unemployment_rate.xlsx")
unemp_df = unemp_df.rename(columns={"2018-19": "2018", "2019-20": "2019", "2020-21": "2020", "2021-22": "2021"})
unemp_long_df = pd.melt(unemp_df, id_vars=["State"], var_name="Year", value_name="Unemployment_Rate")
unemp_long_df["Year"] = unemp_long_df["Year"].astype(int)
unemp_long_df["Unemployment_Rate"] = pd.to_numeric(unemp_long_df["Unemployment_Rate"], errors="coerce")

# --- Step 5: Merge all datasets ---
merged_df = rape_long_df.merge(pop_long_df, on=["State", "Year"], how="inner")
merged_df = merged_df.merge(literacy_long_df, on=["State", "Year"], how="inner")
merged_df = merged_df.merge(unemp_long_df, on=["State", "Year"], how="inner")

# Optional: Calculate Rape rate per 100,000 people
merged_df["Rape_Rate"] = (merged_df["Rape"] / merged_df["Population"]) * 100000

# --- Step 6: Correlation Analysis per Year ---
years = sorted(merged_df["Year"].unique())

for year in years:
    print(f"\n📅 Correlation Matrix for {year}")
    year_df = merged_df[merged_df["Year"] == year]
    corr = year_df[["Rape", "Rape_Rate", "Population", "Literacy_Rate", "Unemployment_Rate"]].corr()
    print(corr.round(2))

    # Optional: Plot heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title(f"Correlation Heatmap - {year}")
    plt.show()
