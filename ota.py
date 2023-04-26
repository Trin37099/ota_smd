import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
import datetime
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(
    page_title="Siteminder OTA",
    layout = 'wide',
)
st.title('Online Travel Agent')

st.subheader('Please Upload CSV Files')
uploaded_files = st.file_uploader("Choose a CSV file",type = 'CSV', accept_multiple_files=True)
for uploaded_file in uploaded_files:
    all = pd.read_csv(uploaded_file,thousands=',')
    
def perform(all): 
    all1 = all[['Booking reference'
                ,'Guest names'
                ,'Check-in'
                ,'Check-out'
                ,'Channel'
                ,'Room'
                ,'Booked-on date'
                ,'Total price']]
    all1 = all1.dropna()

    all1["Check-in"] = pd.to_datetime(all1["Check-in"])
    all1['Booked-on date'] = pd.to_datetime(all1['Booked-on date'], format='%Y/%m/%d')
    all1['Booked'] = all1['Booked-on date'].dt.strftime('%m/%d/%Y')
    all1["Check-out"] = pd.to_datetime(all1["Check-out"])
    all1["Length of stay"] = (all1["Check-out"] - all1["Check-in"]).dt.days
    all1["Lead time"] = (all1["Check-in"] - all1["Booked-on date"]).dt.days

    all1['Room'] = all1['Room'].str.upper()
    all1['Booking reference'] = all1['Booking reference'].astype('str')
    all1['Total price'] = all['Total price'].str.strip('THB')
    all1['Total price'] = all1['Total price'].astype('float64')

    all1['Quantity'] = all1['Room'].str.extract('^(\d+)', expand=False).astype(int)
    all1['Room Type'] = all1['Room'].str.extract('^[^a-zA-Z]+([a-zA-Z\s]+)', expand=False)
    all1['Room Type'] = all1['Room Type'].str.strip('X')
    all1['Room Type'] = all1['Room Type'].str.strip('ONLY')
    all1['Room Type'] = all1['Room Type'].replace(' ', 'UNKNOWN ROOM')
    all1['Room Type'] = all1['Room Type'].str.strip()
    all1['ADR'] = (all1['Total price']/all1['Length of stay'])/all1['Quantity']

    all2 = all1[['Booking reference'
                 ,'Guest names'
                 ,'Check-in'
                 ,'Check-out'
                 ,'Channel'
                 ,'Booked'
                 ,'Total price'
                 ,'ADR'
                 ,'Length of stay'
                 ,'Lead time'
                 ,'Quantity','Room Type']]
    return all2

all2 =  perform(all)
channels = all2['Channel'].unique()
room_type_options = all2['Room Type'].unique().tolist()

fig = px.pie(all2['Channel'].value_counts()
             , values=all2['Channel'].value_counts()
             , names=all2['Channel'].value_counts().index)

st.plotly_chart(fig)

channels = all2['Channel'].unique()
room_type_options =   all2['Room Type'].unique().tolist()
selected_channel = st.sidebar.selectbox('Select channel', ['All'] + list(channels))
selected_room_types = st.sidebar.multiselect('Select room types', room_type_options,default=room_type_options)


if selected_channel != 'All':
    filtered_df = all2[all2['Channel'] == selected_channel]
    if selected_room_types:
        if 'All' not in selected_room_types:
            filtered_df = filtered_df[filtered_df['Room Type'].isin(selected_room_types)]
else:
    if selected_room_types:
        if 'All' not in selected_room_types:
            filtered_df = all2[all2['Room Type'].isin(selected_room_types)]
    else:
        filtered_df = all2

fig1 = px.pie(filtered_df['Room Type'].value_counts()
             , values=filtered_df['Room Type'].value_counts()
             , names=filtered_df['Room Type'].value_counts().index)

st.write(filtered_df)
st.plotly_chart(fig1)
st.write(filtered_df.describe())

filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['ADR'])
st.bar_chart(filtered_df_pi)
filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['Lead time'])
st.bar_chart(filtered_df_pi)
filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['Length of stay'])
st.bar_chart(filtered_df_pi)
