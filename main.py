import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_theme(style='dark')

# helper function 1
def create_monthly_rent_df(df, year):
    monthly_rent_df = df[df['yr']==year].resample(rule='M', on='dteday').agg({
    'casual':'sum',
    'registered':'sum',
    'cnt':'sum'
    })

    monthly_rent_df.index = monthly_rent_df.index.strftime('%Y-%m')
    monthly_rent_df = monthly_rent_df.reset_index()
    monthly_rent_df.rename(columns={
        "cnt":"total"
    }, inplace=True)

    return monthly_rent_df

# helper function 2
def create_season_rent_df(df, year):
    season_rent_df = df[df['yr']==year].groupby(by='season').cnt.sum().sort_values(ascending=False).reset_index()
    
    return season_rent_df

# helper function 3
def create_daily_rent_df(df, year):
    daily_rent_df = df[df['yr']==year].groupby(by='workingday').agg({
    'casual':'sum',
    'registered':'sum',
    'cnt':'sum',
    }).sort_values(by='workingday').reset_index()

    melted_df_daily = pd.melt(daily_rent_df, id_vars=['workingday'], value_vars=['casual', 'registered'], var_name='cust_type', value_name='rent')

    return melted_df_daily

# helper function 4
def create_hourly_rent_df(df, year):
    hourly_rent_df = df[df['yr']==year].groupby(by='timeperiod').cnt.sum().sort_values(ascending=False).reset_index()

    return hourly_rent_df

# load berkas new_hour.csv
hour_df = pd.read_csv('new_hour.csv')

# memastikan kolom dteday berformat datetime
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# membuat sidebar untuk filter tahun
with st.sidebar:
    year = st.radio(
    label="Choose Year to see data",
    options=(2011, 2012),
    horizontal=True)

monthly_rent_df = create_monthly_rent_df(hour_df, year)
season_rent_df = create_season_rent_df(hour_df, year)
daily_rent_df = create_daily_rent_df(hour_df, year)
hourly_rent_df = create_hourly_rent_df(hour_df, year)

# Header
st.header(':bike: Bike Sharing Data Dashboard :bike:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Current Data Info Year', value=year)

with col2:
    total_rent = monthly_rent_df['total'].sum()
    st.metric('Total Rent', value=total_rent)

# Visualisasi data performa sharing tiap bulan
st.subheader('Monthly Bike Sharing Performance Analysis')

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(monthly_rent_df['dteday'], monthly_rent_df['casual'], label='casual', color='#23326A', linewidth=3)
ax.plot(monthly_rent_df['dteday'], monthly_rent_df['registered'], label='registered', color='#FABB23', linewidth=3)
ax.plot(monthly_rent_df['dteday'], monthly_rent_df['total'], label='total', color='#D9D4CE', linewidth=3)
ax.set_xlabel('Month',size=15)
ax.set_ylabel('Rent',size=15)
ax.legend()

st.pyplot(fig)

# Visualisasi data performa sharing tiap musim
st.subheader("Seasonal Bike Sharing Performance Analysis")

colors = ["#FABB23", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

fig, ax = plt.subplots(figsize=(12, 3))

sns.barplot(x="cnt", y="season", data=season_rent_df, palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis ='y', labelsize=12)

st.pyplot(fig)

# Visualisasi data peminjaman sepeda ketika libur dan tidak libur
st.subheader("Eventual Bike Sharing Performance")

fig, ax = plt.subplots(figsize=(12, 3))

sns.barplot(x="workingday", y="rent", data=daily_rent_df, hue='cust_type', ax=ax)
ax.set_ylabel(None)
ax.set_xlabel('Working Days')
ax.tick_params(axis ='x', labelsize=12)

st.pyplot(fig)

# Visualisasi data untuk informasi periode waktu terbaik dan terburuk sharing sepeda
st.subheader('Best and Worst Performing Time by Number of Rent')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

sns.barplot(x="cnt", y="timeperiod", data=hourly_rent_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Time", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="cnt", y="timeperiod", data=hourly_rent_df.sort_values(by="cnt", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Time", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

st.caption('Copyright (c) Hanafi 2024')