import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle

# Membaca data dari file CSV atau data yang sudah ada
df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv") 

# Merubah tipe data dteday dari object ke datetime
df_day["dteday"] = pd.to_datetime(df_day["dteday"])
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])

# Merubah isi kolom, dari angka menjadi keterangan sesuai kebutuhan analisis agar lebih mudah dibaca
df_day.yr.replace({0:'2011', 1:'2012'}, inplace=True)
df_hour.yr.replace({0:'2011', 1:'2012'}, inplace=True)
df_day.mnth.replace({1:'Jan', 2:'Feb', 3:'Mar' , 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}, inplace=True)
df_hour.mnth.replace({1:'Jan', 2:'Feb', 3:'Mar' , 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}, inplace=True)
df_day.season.replace({1:'Spring',2:'Summer', 3:'Fall', 4: 'Winter'}, inplace=True)
df_hour.season.replace({1:'Spring',2:'Summer', 3:'Fall', 4: 'Winter'}, inplace=True)
df_day.weathersit.replace({1:'Clear', 2:'Misty',3:'Light_snow', 4:'Heavy_rain'}, inplace=True)
df_hour.weathersit.replace({1:'Clear', 2:'Misty',3:'Light_snow', 4:'Heavy_rain'}, inplace=True)

columns = ["yr", "mnth", "season", "weathersit"]
for column in columns:
    df_day[column] =  df_day[column].astype("category")
    df_hour[column] =  df_hour[column].astype("category")


# Fungsi untuk menampilkan total bike rentals per bulan di tahun 2011
def total_bike_rentals_per_month_2011():
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_day["mnth"] = pd.Categorical(df_day["mnth"], categories=month_order, ordered=True)
    filtered_df = df_day[df_day["yr"] == "2011"].groupby(by="mnth").agg({"cnt": "sum"}).reset_index()

    st.subheader("Total Bike Rentals per Month in 2011")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(filtered_df["mnth"], filtered_df["cnt"], label="Sum", marker="o")
    ax.set_title("Total Bike Rentals per Month in 2011", fontsize=14)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Total Rentals", fontsize=12)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


# Fungsi untuk menampilkan highest bike rentals per hour di tahun 2012
def highest_bike_rentals_per_hour_2012():
    filtered_df = df_hour[df_hour["yr"] == "2012"].groupby("hr").agg({"cnt": "sum"}).sort_values(by="cnt", ascending=False).reset_index()
    top_5 = filtered_df.nlargest(5, 'cnt')
    
    st.subheader("Highest Bike Rentals by Hour in 2012")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="hr", y="cnt", data=top_5, palette= ["#DBE6F0", "#DBE6F0", "#275C8F", "#DBE6F0", "#DBE6F0"], ax=ax)
    ax.set_title("Highest Bike Rentals by Hour in 2012", fontsize=14)
    ax.set_xlabel("Hours (PM)", fontsize=12)
    ax.set_ylabel("Total Rentals", fontsize=12)
    st.pyplot(fig)


# Fungsi untuk menampilkan number of bike users berdasarkan kondisi cuaca
def number_of_bike_users_by_weather_condition():
    filtered_df = df_day.groupby(by="weathersit").agg({"cnt": ["sum"]}).reset_index()
    
    st.subheader("Number of Bike Users by Weather Condition")
    fig, ax = plt.subplots(figsize=(18, 10))
    sns.barplot(x="weathersit", y=("cnt", "sum"), palette="Blues_r", data=filtered_df, ax=ax)
    ax.set_title("Number of Bike Users by Weather Condition", fontsize=14)
    ax.set_xlabel("Weather Condition", fontsize=12)
    ax.set_ylabel("Total Rentals", fontsize=12)
    st.pyplot(fig)


# Fungsi untuk menampilkan number of bike rentals per season
def number_of_bike_rentals_by_season():
    filtered_df = df_day.groupby("season")["cnt"].sum().reset_index()
    max_value = filtered_df["cnt"].max()
    min_value = filtered_df["cnt"].min()
    colors = ["lightgrey" if val != max_value and val != min_value else "blue" if val == max_value else "red" for val in filtered_df["cnt"]]
    
    st.subheader("Number of Bike Rentals by Season")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(filtered_df["season"], filtered_df["cnt"], color=colors)
    ax.set_xlabel("Season", fontsize=12)
    ax.set_ylabel("Total Rentals", fontsize=12)
    ax.set_title("Number of Bike Rentals by Season")
    legend_handles = [
        Rectangle((0, 0), 1, 1, color='blue', label='Highest'),
        Rectangle((0, 0), 1, 1, color='red', label='Lowest')
    ]
    ax.legend(handles=legend_handles)
    
    st.pyplot(fig)

st.title("🚲 Bike Rental Dashboard")

# Sidebar untuk memilih analisis
st.sidebar.title("Select Analysis")
analysis_type = st.sidebar.selectbox(
    "Choose an analysis to view:",
    ["Total Bike Rentals per Month in 2011", 
     "Highest Bike Rentals by Hour in 2012", 
     "Number of Bike Users by Weather Condition", 
     "Number of Bike Rentals by Season"]
)
st.sidebar.caption('Copyright (c) Adrian Sanjaya 2024')

# Memanggil fungsi sesuai pilihan pengguna
if analysis_type == "Total Bike Rentals per Month in 2011":
    total_bike_rentals_per_month_2011()
elif analysis_type == "Highest Bike Rentals by Hour in 2012":
    highest_bike_rentals_per_hour_2012()
elif analysis_type == "Number of Bike Users by Weather Condition":
    number_of_bike_users_by_weather_condition()
elif analysis_type == "Number of Bike Rentals by Season":
    number_of_bike_rentals_by_season()