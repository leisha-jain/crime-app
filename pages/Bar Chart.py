import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Top 5 States by Crime")

# Mapping of crime names to filenames
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

years = [2018, 2019, 2020, 2021, 2022]

# --- Sidebar: Select Crime & Year --- #
selected_crime = st.selectbox("Select Crime Type", list(crime_files.keys()))
selected_year = st.selectbox("Select Year", years)

# --- Load the selected crime file --- #
@st.cache_data
def load_crime_data(filename):
    df = pd.read_csv(filename)
    df = df.rename(columns={df.columns[0]: "State"})  # ensure first column is 'State'

    # Clean 'State' column
    df["State"] = df["State"].str.strip().str.title()

# Remove unwanted total rows
    df = df[~df["State"].isin(["Total All India", "Total States(S)","Total (All India)","Total State(S)","Total States (S)","Total Ut(S)"])]


    return df

df = load_crime_data(crime_files[selected_crime])


# --- Check and display --- #
if str(selected_year) not in df.columns:
    st.error(f"❌ Year {selected_year} not found in {selected_crime} data.")
else:
    # Clean column
    df["State"] = df["State"].str.strip().str.title()

    year_col = str(selected_year)

# Clean the year column: remove commas, spaces, and convert to numeric
    df[year_col] = (
        df[year_col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
    df = df.dropna(subset=[year_col])

    # Now safely sort and take top 5
    top_5 = df[["State", year_col]].sort_values(by=year_col, ascending=False).head(5)


    # Bar chart
    fig = px.bar(
        top_5,
        x="State",
        y=str(selected_year),
        color="State",
        text=str(selected_year),
        title=f"Top 5 States for {selected_crime} in {selected_year}"
    )
    fig.update_layout(xaxis_title="State", yaxis_title="Total Cases", showlegend=False)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    # Insights
    st.subheader("Insights")
    top_state = top_5.iloc[0]
    average_top5 = top_5[str(selected_year)].mean()
    national_avg = df[str(selected_year)].mean()

    st.markdown(f"""
    - **{top_state['State']}** reported the highest number of **{selected_crime}** cases in **{selected_year}**, with **{top_state[str(selected_year)]:,.2f} per 100,000 people**.
    - The **top 5 average** is **{average_top5:.2f}**.
    - The **national average** is **{national_avg:.2f}**, so the top state is **{(top_state[str(selected_year)]/national_avg):.1f}×** above average.
    """)
