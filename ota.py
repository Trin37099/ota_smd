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
    if ' X '  in room_type:
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
    all1['Booked-on date'] = pd.to_datetime(all1['Booked-on date'],format='%d/%m/%Y %H:%M:%S')
    all1['Booked'] = all1['Booked-on date'].dt.strftime('%d/%m/%Y')
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
    all1.loc[(all1['Channel']=='Expedia') | (all1['Channel']=='Booking.com'),'ADR'] = all1['ADR'] *0.82
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

tab1, tab_stay = st.tabs(['Book on date','Stay on date'])
with tab1:
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
        st.markdown('NOTE: Some Room Type it is difference name but it is same type EX. DELUXE DOUBLE OR TWIN = DELUXE TWIN and Discount commission rate 18%')

    month_dict = {v: k for k,v in enumerate(calendar.month_name)}
    months = list(calendar.month_name)[1:]
    selected_month = st.multiselect('Select a month', months)
    if selected_month:
            selected_month_nums = [month_dict[month_name] for month_name in selected_month]
            filtered_df = filtered_df[filtered_df['Booked'].dt.month.isin(selected_month_nums)]

    col1 , col2 ,col3 = st.columns(3)
    with col2:
        filter_LT = st.checkbox('Filter by LT ')
        if filter_LT:
            min_val, max_val = int(filtered_df['Lead time'].min()), int(filtered_df['Lead time'].max())
            LT_min, LT_max = st.slider('Select a range of LT', min_val, max_val, (min_val, max_val))
            filtered_df = filtered_df[(filtered_df['Lead time'] >= LT_min) & (filtered_df['Lead time'] <= LT_max)]
        else:
            filtered_df = filtered_df.copy()
    with col1:
        filter_LOS = st.checkbox('Filter by LOS ')
        if filter_LOS:
            min_val, max_val = int(filtered_df['Length of stay'].min()), int(filtered_df['Length of stay'].max())
            LOS_min, LOS_max = st.slider('Select a range of LOS', min_val, max_val, (min_val, max_val))
            filtered_df = filtered_df[(filtered_df['Length of stay'] >= LOS_min) & (filtered_df['Length of stay'] <= LOS_max)]
        else:   
            filtered_df = filtered_df.copy()
    with col3:
        filter_rn = st.checkbox('Filter by Roomnight')
        if filter_rn:
            min_val, max_val = int(filtered_df['RN'].min()), int(filtered_df['RN'].max())
            rn_min, rn_max = st.slider('Select a range of roomnights', min_val, max_val, (min_val, max_val))
            filtered_df = filtered_df[(filtered_df['RN'] >= rn_min) & (filtered_df['RN'] <= rn_max)]
        else:
            filtered_df = filtered_df.copy()

    col1, col2 = st.columns(2)
    channels = filtered_df['Channel'].unique()
    num_colors = len(channels)
    existing_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#6392FF']
    additional_colors = ['#FFD700', '#8B008B', '#00FF00']
    combined_colors = existing_colors + additional_colors
    colors = combined_colors
    color_scale =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}
    with col1:
        grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
        fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
        st.plotly_chart(fig)
    with col2:
        grouped = filtered_df.groupby(['Lead time', 'Channel']).size().reset_index(name='counts')
        fig = px.bar(grouped, x='Lead time', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
        st.plotly_chart(fig)


    tab1, tab2, tab3 ,tab4, tab5 , tab6 ,tab7= st.tabs(["Average", "Median", "Statistic",'Data'
                                                    ,'Bar Chart','Room roomnight by channel'
                                                    ,'Room revenue by channel'])
    with tab1:
        col0, col1, col2, col3, col4 = st.columns(5)
        filtered_df['ADR discount'] = filtered_df["ADR"]*filtered_df["Length of stay"]*filtered_df["Quantity"]
        col0.metric('**Revenue**',f'{round(filtered_df["ADR discount"].sum(),4)}')
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
    with tab6:
        counts = filtered_df[['Channel', 'Room Type','RN']].groupby(['Channel', 'Room Type']).sum().reset_index()
        fig = px.treemap(counts, path=['Channel', 'Room Type','RN'], values='RN', color='RN',color_continuous_scale='YlOrRd')
        st.plotly_chart(fig)
    with tab7:
        counts = filtered_df[['Channel', 'Room Type','ADR discount']].groupby(['Channel', 'Room Type']).sum().reset_index()
        fig = px.treemap(counts, path=['Channel', 'Room Type','ADR discount'], values='ADR discount', color='ADR discount',color_continuous_scale='YlOrRd')
        st.plotly_chart(fig)

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
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Booked', 'ADR']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)

    with t2:
        filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['Lead time'])
        st.bar_chart(filtered_df_pi)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Booked', 'Lead time']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Lead time',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
    with t3:
        filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['Length of stay'])
        st.bar_chart(filtered_df_pi)
        
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Booked', 'Length of stay']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
    with t4:
        filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['RN'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Booked', 'RN']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)

    st.markdown('**Pivot table by lead time**')
    t1,t2,t3 = st.tabs(['ADR','LOS','RN'])
    with t1:
        filtered_df_pi = pd.pivot_table(filtered_df, index='Lead time',values=['ADR'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Lead time', 'ADR']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Lead time', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
    with t2:
        filtered_df_pi = pd.pivot_table(filtered_df, index='Lead time',values=['Length of stay'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Lead time', 'Length of stay']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Lead time', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
    with t3:
        filtered_df_pi = pd.pivot_table(filtered_df, index='Lead time',values=['RN'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Lead time', 'RN']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Lead time', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)

    st.markdown('**Pivot table by LOS**')
    t1,t2,t3 = st.tabs(['ADR','LT','RN'])
    with t1:
        filtered_df_pi = pd.pivot_table(filtered_df, index='Length of stay',values=['ADR'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Length of stay', 'ADR']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
    with t2:
        filtered_df_pi = pd.pivot_table(filtered_df, index='Length of stay',values=['Lead time'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Length of stay', 'Lead time']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='Lead time',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
    with t3:
        filtered_df_pi = pd.pivot_table(filtered_df, index='Length of stay',values=['RN'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Length of stay', 'RN']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)

    st.markdown('**Pivot table by RN**')
    t1,t2,t3 = st.tabs(['ADR','LOS','LT'])
    with t1:
        filtered_df_pi = pd.pivot_table(filtered_df, index='RN',values=['ADR'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['RN', 'ADR']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['RN', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
    with t2:
        filtered_df_pi = pd.pivot_table(filtered_df, index='RN',values=['Length of stay'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['RN', 'Length of stay']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['RN', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
    with t3:
        filtered_df_pi = pd.pivot_table(filtered_df, index='RN',values=['Lead time'])
        st.bar_chart(filtered_df_pi)

        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['RN', 'Lead time']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Lead time',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)
        with col2:
            grouped = filtered_df.groupby(['RN', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig)

with tab_stay:
    all3 =  perform(all)
    if selected_channels:
        filtered_df = all3[all3['Channel'].isin(selected_channels)]
        if selected_room_types:
            if 'All' not in selected_room_types:
                filtered_df = filtered_df[filtered_df['Room Type'].isin(selected_room_types)]
        else:
            if selected_room_types:
                if 'All' not in selected_room_types:
                    filtered_df = all3[all3['Room Type'].isin(selected_room_types)]
    else:
        filtered_df = all3

filtered_df['Stay'] = filtered_df.apply(lambda row: pd.date_range(row['Check-in'], row['Check-out']), axis=1)
filtered_df = filtered_df.explode('Stay').reset_index(drop=True)
filtered_df = filtered_df[['Stay','Check-in','Guest names','Channel','ADR','Length of stay','Lead time','RN','Quantity','Room Type']]
#all3['Total discount'] = all3["ADR"]*all3["Length of stay"]*all3["Quantity"]
filtered_df['Day Name'] = filtered_df['Stay'].dt.strftime('%A')
filtered_df['Week of Year'] = filtered_df['Stay'].dt.weekofyear

month_dict = {v: k for k,v in enumerate(calendar.month_name)}
months = list(calendar.month_name)[1:]
selected_month = st.multiselect('Select a month stay', months)
if selected_month:
        selected_month_nums = [month_dict[month_name] for month_name in selected_month]
        filtered_df = filtered_df[filtered_df['Stay'].dt.month.isin(selected_month_nums)]

col1 , col2 = st.columns(2)
with col2:
    filter_LT = st.checkbox('Filter by LT')
    if filter_LT:
        min_val, max_val = int(filtered_df['Lead time'].min()), int(filtered_df['Lead time'].max())
        LT_min, LT_max = st.slider('Select a range of LT', min_val, max_val, (min_val, max_val))
        filtered_df = filtered_df[(filtered_df['Lead time'] >= LT_min) & (filtered_df['Lead time'] <= LT_max)]
    else:
        filtered_df = filtered_df.copy()
with col1:
    filter_LOS = st.checkbox('Filter by LOS')
    if filter_LOS:
        min_val, max_val = int(filtered_df['Length of stay'].min()), int(filtered_df['Length of stay'].max())
        LOS_min, LOS_max = st.slider('Select a range of LOS', min_val, max_val, (min_val, max_val))
        filtered_df = filtered_df[(filtered_df['Length of stay'] >= LOS_min) & (filtered_df['Length of stay'] <= LOS_max)]
    else:
        filtered_df = filtered_df.copy()

st.markdown('**You can zoom in**')
col1, col2 = st.columns(2)
channels = filtered_df['Channel'].unique()
num_colors = len(channels)
existing_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#6392FF']
additional_colors = ['#FFD700', '#8B008B', '#00FF00']
combined_colors = existing_colors + additional_colors
colors = combined_colors
color_scale =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}
with col1:
    grouped = filtered_df.groupby(['Stay', 'Channel']).size().reset_index(name='counts')
    fig = px.bar(grouped, x='Stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
    st.plotly_chart(fig)
with col2:
    grouped = filtered_df.groupby(['Lead time', 'Channel']).size().reset_index(name='counts')
    fig = px.bar(grouped, x='Lead time', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
    st.plotly_chart(fig)



col1, col2 = st.columns(2)
with col1:
    st.markdown('**count Stay in week of Year (calendar)**')
    pt = filtered_df.pivot_table(index='Week of Year', columns='Day Name', aggfunc='size')
    if set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).issubset(filtered_df['Day Name'].unique()):
        pt = filtered_df.pivot_table(index='Week of Year', columns='Day Name', aggfunc='size', fill_value=0)
        pt = pt[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
        st.write(pt.style.background_gradient(cmap='coolwarm', axis=1))
    else:
        st.write('Not enough data to create a pivot table')
with col2:
    st.markdown('**A.LT that Check-in in week of Year (calendar)**')
    grouped = filtered_df.groupby(['Week of Year', 'Day Name'])
    averages = grouped['Lead time'].mean().reset_index()
    pt = pd.pivot_table(averages, values='Lead time', index=['Week of Year'], columns=['Day Name'])
    if set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).issubset(filtered_df['Day Name'].unique()):
        pt = pt.loc[:, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
        st.write(pt.style.format("{:.2f}").background_gradient(cmap='coolwarm', axis=1))
    else:
        st.write('Not enough data to create a pivot table')


