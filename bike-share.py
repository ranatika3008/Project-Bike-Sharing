import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_monthly_day_df(df):
    monthly_day_df = day_df.resample(rule='M', on='dteday').agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
    })
    monthly_day_df.index = monthly_day_df.index.strftime('%b %Y')
    monthly_day_df = monthly_day_df.reset_index()
    monthly_day_df.rename(columns={
        "dteday": "date_day",
        "cnt": "rented_total"}, inplace=True)
    return monthly_day_df

def create_byseason_df(df):
    byseason_df = day_df.groupby(by="season").cnt.nunique().reset_index()
    byseason_df['season'] = byseason_df['season'].replace({1: "Spring", 2:"Summer", 3:"Fall", 4:"Winter"})
    byseason_df.rename(columns={
        "cnt" : "rented_total"
        }, inplace=True)
    return byseason_df

day_df = pd.read_csv("day_df.csv")
hour_df = pd.read_csv("hour_df.csv")

dteday_day = ["dteday"]
for column in dteday_day:
    day_df[column] = pd.to_datetime(day_df[column])

monthly_day_df = create_monthly_day_df(day_df)
byseason_df = create_byseason_df(day_df)

st.header('Proyek Analisis Data :sparkles:')
st.subheader('Number of Orders per Month')

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    monthly_day_df["date_day"], 
    monthly_day_df["rented_total"], 
    marker='o', 
    linewidth=2, 
    color="#72BCD4"
)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=12,rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 4))
colors_ = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]
sns.barplot(
    x="season", 
    y="rented_total",
    data=byseason_df.sort_values(by="season", ascending=False),
    palette=colors_
)
ax.set_title("Rented Amount by Season", loc="center", fontsize=15)
ax.set_ylabel("Rented Total")
ax.set_xlabel("Season")
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)
