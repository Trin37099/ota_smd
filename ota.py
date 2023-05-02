import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
import datetime
import altair as alt
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import re
import warnings
import calendar
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

def clean_room_type(room_type):
    if ' X ' in room_type:
        room_type = 'MIXED ROOM'
    return room_type

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
    all1['Booked'] = pd.to_datetime(all1['Booked'])
    all1["Check-out"] = pd.to_datetime(all1["Check-out"])
    all1["Length of stay"] = (all1["Check-out"] - all1["Check-in"]).dt.days
    all1["Lead time"] = (all1["Check-in"] - all1["Booked"]).dt.days

    all1['Room'] = all1['Room'].str.upper()
    all1['Booking reference'] = all1['Booking reference'].astype('str')
    all1['Total price'] = all['Total price'].str.strip('THB')
    all1['Total price'] = all1['Total price'].astype('float64')

    all1['Quantity'] = all1['Room'].str.extract('^(\d+)', expand=False).astype(int)
    all1['Room Type'] = all1['Room'].str.replace('^DELUXE \(DOUBLE OR TWIN\) ROOM ONLY$', 'DELUXE TWIN')
    all1['Room Type'] = all1['Room Type'].str.replace('-.*', '', regex=True)
    all1['Room Type'] = all1['Room Type'].apply(lambda x: re.sub(r'^\d+\sX\s', '', x))
    all1['Room Type'] = all1['Room Type'].apply(clean_room_type)
    all1['Room Type'] = all1['Room Type'].str.replace('(NRF)', '').apply(lambda x: x.replace('()', ''))
    all1['Room Type'] = all1['Room Type'].str.replace('WITH BREAKFAST', '')
    all1['Room Type'] = all1['Room Type'].str.replace('ROOM ONLY', '')
    all1['Room Type'] = all1['Room Type'].replace('', 'UNKNOWN ROOM')
    all1['Room Type'] = all1['Room Type'].str.strip()
    all1['ADR'] = (all1['Total price']/all1['Length of stay'])/all1['Quantity']
    all1['RN'] = all1['Length of stay']*all1['Quantity']

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
                 ,'RN'
                 ,'Quantity'
                 ,'Room'
                 ,'Room Type']]
    return all2

all2 =  perform(all)
channels = all2['Channel'].unique()
room_type_options = all2['Room Type'].unique().tolist()

counts = all2[['Channel', 'Room Type']].groupby(['Channel', 'Room Type']).size().reset_index(name='Count')
total_count = counts['Count'].sum()

fig = px.treemap(counts, path=['Channel', 'Room Type'], values='Count', color='Count',color_continuous_scale='YlOrRd')


#start_date = st.sidebar.date_input('Start date', pd.to_datetime(all2['Check-in']).min())
#end_date = st.sidebar.date_input('End date', pd.to_datetime(all2['Check-out']).max())
channels = all2['Channel'].unique()
room_type_options =   all2['Room Type'].unique().tolist()
selected_channels = st.sidebar.multiselect('Select channels', channels, default=channels)
selected_room_types = st.sidebar.multiselect('Select room types', room_type_options, default=room_type_options)


if selected_channels:
    filtered_df = all2[all2['Channel'].isin(selected_channels)]
    if selected_room_types:
        if 'All' not in selected_room_types:
            filtered_df = filtered_df[filtered_df['Room Type'].isin(selected_room_types)]
    else:
        if selected_room_types:
            if 'All' not in selected_room_types:
                filtered_df = all2[all2['Room Type'].isin(selected_room_types)]
else:
    filtered_df = all2

col1, col2 = st.columns([2.5,1])
with col1:
    st.plotly_chart(fig)
with col2:
    st.markdown('## GUIDE')
    st.markdown('**-You can multiselect Channels. If you do not select anything, It would be All Channels**')
    st.markdown('**-You can multiselect Room Type. If you do not select anything, It would be All Room Type**')
    st.markdown('NOTE: Some Room Type it is difference name but it is same type EX. DELUXE DOUBLE OR TWIN = DELUXE TWIN ')

month_dict = {v: k for k,v in enumerate(calendar.month_name)}
months = list(calendar.month_name)[1:]
selected_month = st.multiselect('Select a month', months)
if selected_month:
    selected_month_nums = [month_dict[month_name] for month_name in selected_month]
    filtered_df = filtered_df[filtered_df['Booked'].dt.month.isin(selected_month_nums)]


tab1, tab2, tab3 ,tab4, tab5= st.tabs(["Average", "Median", "Statistic",'Data','Bar Chart'])
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col4.metric('**ADR**',f'{round(filtered_df["ADR"].mean(),4)}',)
    col1.metric("**A.LT**", f'{round(filtered_df["Lead time"].mean(),4)}')
    col2.metric("**A.LOS**", f'{round(filtered_df["Length of stay"].mean(),4)}')
    col3.metric("**A.RN**", f'{round(filtered_df["RN"].mean(),4)}')
with tab2:
    col1, col2, col3, col4 = st.columns(4)
    col4.metric('ADR',f'{round(filtered_df["ADR"].median(),4)}')
    col1.metric("A.LT", f'{round(filtered_df["Lead time"].median(),4)}')
    col2.metric("A.LOS", f'{round(filtered_df["Length of stay"].median(),4)}')
    col3.metric("A.RN", f'{round(filtered_df["RN"].median(),4)}')
with tab3:
    st.write(filtered_df.describe())
with tab4:
    st.write(filtered_df)
with tab5:
    tab11, tab12, tab13, tab14 = st.tabs(['A.LT','A.LOS','A.RN','ADR by month'])
    with tab14:
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        mean_adr_by_month = filtered_df.groupby(filtered_df['Booked'].dt.month_name()).mean()['ADR'].reset_index()
        mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)
        bar_chart = alt.Chart(mean_adr_by_month).mark_bar().encode(x=alt.X('Booked:O', sort=month_order),y='ADR')
        st.altair_chart(bar_chart, use_container_width=True)
    with tab11:
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        mean_adr_by_month = filtered_df.groupby(filtered_df['Booked'].dt.month_name()).mean()['Lead time'].reset_index()
        mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)
        bar_chart = alt.Chart(mean_adr_by_month).mark_bar().encode(x=alt.X('Booked:O', sort=month_order),y='Lead time')
        st.altair_chart(bar_chart, use_container_width=True)
    with tab12:
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        mean_adr_by_month = filtered_df.groupby(filtered_df['Booked'].dt.month_name()).mean()['Length of stay'].reset_index()
        mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)
        bar_chart = alt.Chart(mean_adr_by_month).mark_bar().encode(x=alt.X('Booked:O', sort=month_order),y='Length of stay')
        st.altair_chart(bar_chart, use_container_width=True)
    with tab13:
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        mean_adr_by_month = filtered_df.groupby(filtered_df['Booked'].dt.month_name()).mean()['RN'].reset_index()
        mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)
        bar_chart = alt.Chart(mean_adr_by_month).mark_bar().encode(x=alt.X('Booked:O', sort=month_order),y='RN')
        st.altair_chart(bar_chart, use_container_width=True)


filtered_df['Booked'] = pd.to_datetime(filtered_df['Booked'])
filtered_df['Day Name'] = filtered_df['Booked'].dt.strftime('%A')
filtered_df['Week of Year'] = filtered_df['Booked'].dt.weekofyear


col1, col2 = st.columns(2)
with col1:
    st.markdown('**count Booking in week of Year (calendar)**')
    pt = filtered_df.pivot_table(index='Week of Year', columns='Day Name', aggfunc='size', fill_value=0)
    if set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).issubset(filtered_df['Day Name'].unique()):
        pt = filtered_df.pivot_table(index='Week of Year', columns='Day Name', aggfunc='size', fill_value=0)
        pt = pt[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
        st.write(pt.style.background_gradient(cmap='coolwarm', axis=1))
    else:
        st.write('Not enough data to create a pivot table')

with col2:
    filtered_df1 =filtered_df[['Booked','RN']]
    df_grouped = filtered_df1.groupby('Booked').sum().reset_index()
    pivot_df = df_grouped.pivot_table(values='RN'
                                  , index=df_grouped['Booked'].dt.weekofyear
                                  , columns=df_grouped['Booked'].dt.day_name(), aggfunc='sum', fill_value=0)
    st.markdown('**count Roomnight in week of Year (calendar)**')
    if set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).issubset(filtered_df['Day Name'].unique()):
        pt = pivot_df[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
        st.write(pt.style.background_gradient(cmap='coolwarm', axis=1))
    else:
        st.write('Not enough data to create a pivot table')


st.markdown('**Pivot table by Booked**')
t1,t2,t3,t4 = st.tabs(['ADR','LT','LOS','RN'])
with t1:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['ADR'])
    st.bar_chart(filtered_df_pi)
with t2:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['Lead time'])
    st.bar_chart(filtered_df_pi)
with t3:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['Length of stay'])
    st.bar_chart(filtered_df_pi)
with t4:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['RN'])
    st.bar_chart(filtered_df_pi)

st.markdown('**Pivot table by lead time**')
t1,t2,t3 = st.tabs(['ADR','LOS','RN'])
with t1:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Lead time',values=['ADR'])
    st.bar_chart(filtered_df_pi)
with t2:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Lead time',values=['Length of stay'])
    st.bar_chart(filtered_df_pi)
with t3:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Lead time',values=['RN'])
    st.bar_chart(filtered_df_pi)

st.markdown('**Pivot table by LOS**')
t1,t2,t3 = st.tabs(['ADR','LT','RN'])
with t1:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Length of stay',values=['ADR'])
    st.bar_chart(filtered_df_pi)
with t2:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Length of stay',values=['Lead time'])
    st.bar_chart(filtered_df_pi)
with t3:
    filtered_df_pi = pd.pivot_table(filtered_df, index='Length of stay',values=['RN'])
    st.bar_chart(filtered_df_pi)

st.markdown('**Pivot table by RN**')
t1,t2,t3 = st.tabs(['ADR','LOS','LT'])
with t1:
    filtered_df_pi = pd.pivot_table(filtered_df, index='RN',values=['ADR'])
    st.bar_chart(filtered_df_pi)
with t2:
    filtered_df_pi = pd.pivot_table(filtered_df, index='RN',values=['Length of stay'])
    st.bar_chart(filtered_df_pi)
with t3:
    filtered_df_pi = pd.pivot_table(filtered_df, index='RN',values=['Lead time'])
    st.bar_chart(filtered_df_pi)
