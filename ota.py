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
import seaborn as sns
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

hotel_select = st.selectbox("Hotel", ["THE GRASS", "ASTER",'Amber PTY','ALTERA'])
if hotel_select == "THE GRASS":
    def convert_room_type(room_type):
        if re.search(r'\bCITY VIEW ONE BEDROOM SUITE\b|\bONE GRASS SUITE CITY VIEW ROOM\b', room_type):
            return 'ONE GRASS SUITE CITY VIEW'
        elif re.search(r'\bห้องสวีทแบบสองห้องนอน\b|\bTWO-BEDROOM SUITE\b|\bTWO GRASS SUITE ROOM\b|\bTWO BEDROOM SUITE\b|\bTWO GRASS SUITE\b', room_type):
            return 'TWO GRASS SUITE'
        elif re.search(r'\bห้องสวีท\b|\bSUITE\b|\bONE GRASS SUITE ROOM\b|\bONE BEDROOM SUITE\b|\bSUITE ONE GRASS SERVICE SUITE\b|\bSUITE ONE\b', room_type):
            return 'ONE GRASS SUITE'
        elif re.search(r'\bMIXED ROOM\b', room_type):
            return 'MIXED'
        else:
            return 'UNKNOWN ROOM TYPE'
elif hotel_select == "ASTER":
    def convert_room_type(room_type):
        if re.search(r'\bGRAND CORNER SUITE\b|\bGRAND CORNER SUITE ROOM\b|\bCORNER SUITE\b', room_type):
            return 'GRAND CORNER SUITE'
        elif re.search(r'\bGRAND DELUXE KING\b|\bDOUBLE GRAND DELUXE KING\b|\bDELUXE ROOM, 1 KING BED\b', room_type):
            return 'GRAND DELUXE KING'
        elif re.search(r'\bNEW DELUXE\b|\bNEW DELUXE ROOM\b|\bDOUBLE NEW DELUXE ROOM\b', room_type):
            return 'NEW DELUXE'
        elif re.search(r'\bGRAND DELUXE TWIN ROOM\b|\bGRAND DELUXE TWIN ROOM\b|\bTWIN GRAND DELUXE TWIN\b', room_type):
            return 'GRAND DELUXE TWIN'
        elif re.search(r'\bGRAND DELUXE ROOM\b|\bDOUBLE GRAND DELUXE DOUBLE ROOM\b|\bGRAND DELUXE\b|\bGRAND DELUXE DOUBLE ROOM\b', room_type):
            return 'GRAND DELUXE'
        elif re.search(r'\bMIXED ROOM\b', room_type):
            return 'MIXED'
        else:
            return 'UNKNOWN ROOM TYPE'
elif hotel_select == "Amber PTY":
    def convert_room_type(room_type):
        if re.search(r'\bGRAND CORNER SUITE\b|\bGRAND CORNER SUITE ROOM\b|\bCORNER SUITE\b', room_type):
            return 'GRAND CORNER SUITE'
        elif re.search(r'\bGRAND DELUXE KING\b|\bDOUBLE GRAND DELUXE KING\b|\bDELUXE ROOM, 1 KING BED\b', room_type):
            return 'GRAND DELUXE KING'
        elif re.search(r'\bNEW DELUXE\b|\bNEW DELUXE ROOM\b|\bDOUBLE NEW DELUXE ROOM\b', room_type):
            return 'NEW DELUXE'
        elif re.search(r'\bGRAND DELUXE TWIN ROOM\b|\bGRAND DELUXE TWIN ROOM\b|\bTWIN GRAND DELUXE TWIN\b', room_type):
            return 'GRAND DELUXE TWIN'
        elif re.search(r'\bGRAND DELUXE ROOM\b|\bDOUBLE GRAND DELUXE DOUBLE ROOM\b|\bGRAND DELUXE\b|\bGRAND DELUXE DOUBLE ROOM\b', room_type):
            return 'GRAND DELUXE'
        elif re.search(r'\bDELUXE DOUBLE OR TWIN ROOM WITH CITY VIEW\b|\bDELUXE CITY VIEW ROOM\b|\bDELUXE CITY VIEW\b', room_type):
            return 'DELUXE CITY VIEW ROOM'
        elif re.search(r'\bDELUXE DOUBLE ROOM WITH POOL VIEW\b|\bDELUXE POOL VIEW DOUBLE\b|\bDELUXE POOL VIEW-DOUBLE\b|\bDELUXE POOL VEIW DOUBLE ROOM\b|\bDELUXE POOL VIEW\b|\bDELUXE DOUBLE ROOM WITH  POOL VIEW\b', room_type):
            return 'DELUXE POOL VIEW DOUBLE'
        elif re.search(r'\bDELUXE POOL VIEW TWIN ROOM\b|\bDELUXE TWIN ROOM WITH POOL VIEW\b|\bDELUXE POOL VIEW-TWIN\b|\bDELUXE POOL VIEW TWIN\b|\bTWIN DELUXE TWIN ROOM WITH POOL VIEW\b', room_type):
            return 'DELUXE POOL VIEW TWIN'
        elif re.search(r'\bDELUXE ROOM\b|\bDOUBLE OR TWIN DELUXE DOUBLE\b|\bDELUXE DOUBLE OR TWIN ROOM\b', room_type):
            return 'DELUXE'
        elif re.search(r'\bMIXED ROOM\b', room_type):
            return 'MIXED'
        else:
            return 'UNKNOWN ROOM TYPE'
elif hotel_select == "ALTERA":
    def convert_room_type(room_type):
        if re.search(r'\bDELUXE ROOM WITH KITCHENETTE\b|\bDELUXE DOUBLE BED ROOM WITH KITCHENETTE\b|\bDELUXE DOUBLE ROOM\b|\bDOUBLE DELUXE\b', room_type):
            return 'DELUXE'
        elif re.search(r'\bGRAND SUITE WITH DOUBLE BED\b|\bGRAND SUITE WITH KITCHENETTE\b|\bGRAND SUITE ROOM DOUBLE BED WITH KITCHENETTE\b|\bSUITE GRAND SUITE\b', room_type):
            return 'GRAND SUITE'
        elif re.search(r'\bDELUXE CITY VIEW ROOM WITH KITCHENETTE\b|\bDELUXE CITY VIEW ROOM\b|\bDELUXE CITY VIEW ROOM DOUBLE OR TWIN BED WITH KITCHENETTE\b|\bDOUBLE OR TWIN DELUXE CITY VIEW DOUBLE OR TWIN\b', room_type):
            return 'DELUXE CITY VIEW'
        elif re.search(r'\bGRAND SUITES POOL VIEW ROOM WITH KITCHENETTE\b|\bSUITE GRAND POOL VIEW\b|\bGRAND SUITE WITH POOL VIEW\b|\bGRAND SUITE POOL VIEW ROOM WITH KITCHENETTE\b|\bGRAND SUITE POOL VIEW ROOM DOUBLE BED WITH KITCHENETTE\b|\bGRAND POOL VIEW SUITE WITH KITCHENETTE\b', room_type):
            return 'GRAND SUITE POOL VIEW'
        elif re.search(r'\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\b|\bDOUBLE DELUXE POOL VIEW DOUBLE\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\(DOUBLE BED\)\b', room_type):
            return 'DELUXE POOL VIEW'
        elif re.search(r'\bTWO BEDROOM FAMILY SUITE WITH KITCHENETTE\b|\b2-BEDROOM FAMILY SUITE WITH KITCHENETTE\b|\bFAMILY SUITES TWO BEDROOM\b|\bFAMILY TWO-BEDROOM SUITE\b|\bFAMILY ROOM FAMILY TWO BEDROOMS\b|\bFAMILY SUITE TWO BEDROOM WITH KITCHENETTE\b', room_type):
            return 'TWO BEDROOM FAMILY SUITE'
        elif re.search(r'\bDELUXE TWIN ROOM WITH POOL VIEW\b|\bDELUXE DOUBLE OR TWIN ROOM WITH POOL VIEW\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\(TWIN BED\)\b|\bDELUXE TWIN ROOM WITH POOL VIEW\b|\bDELUXE POOL VIEW TWIN\b|\bDELUXE POOL VIEW ROOM WITH KITCHENETTE\b|\bTWIN DELUXE POOL VIEW TWIN\b', room_type):
            return 'DELUXE TWIN POOL VIEW'
        elif re.search(r'\bGRAND SUITE ROOM TWIN BED WITH KITCHENETTE\b|\bGRAND SUITE TWIN\b|\bTWIN GRAND TWIN\b', room_type):
            return 'GRAND SUITE ROOM TWIN BED WITH KITCHENETTE'
        elif re.search(r'\bMIXED ROOM\b', room_type):
            return 'MIXED'
        else:
            return 'UNKNOWN'
def convert_RF(room_type):
    if re.search(r'\bNON REFUNDABLE\b|\bไม่สามารถคืนเงินจอง\b|\bNON REFUND\b|\bNON-REFUNDABLE\b|\bNRF\b', room_type):
        return 'NRF'
    elif re.search(r'\bUNKNOWN ROOM\b', room_type):
        return 'UNKNOWN'
    elif  room_type == "1 X " or room_type == "2 X " or room_type == "3 X " or room_type == "4 X ":
        return 'UNKNOWN'
    else:
        return 'Flexible'

    
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
    all1['Booked-on date'] = pd.to_datetime(all1['Booked-on date'])
    all1['Booked'] = all1['Booked-on date'].dt.strftime('%m/%d/%Y')
    all1['Booked'] = pd.to_datetime(all1['Booked'])
    all1["Check-out"] = pd.to_datetime(all1["Check-out"])
    all1["Length of stay"] = (all1["Check-out"] - all1["Check-in"]).dt.days
    all1["Lead time"] = (all1["Check-in"] - all1["Booked"]).dt.days
    value_ranges = [-1, 0, 1, 2, 3, 4, 5, 6, 7,8, 14, 30, 90, 120]
    labels = ['-one', 'zero', 'one', 'two', 'three', 'four', 'five', 'six','seven', '8-14', '14-30', '31-90', '90-120', '120+']
    all1['Lead time range'] = pd.cut(all1['Lead time'], bins=value_ranges + [float('inf')], labels=labels, right=False)

    all1['Room'] = all1['Room'].str.upper()
    all1['Booking reference'] = all1['Booking reference'].astype('str')
    all1['Total price'] = all['Total price'].str.strip('THB')
    all1['Total price'] = all1['Total price'].astype('float64')

    all1['Quantity'] = all1['Room'].str.extract('^(\d+)', expand=False).astype(int)
    #all1['Room Type'] = all1['Room'].apply(lambda x: convert_room_type(x))
    #all1['Room Type'] = all1['Room'].str.replace('^DELUXE \(DOUBLE OR TWIN\) ROOM ONLY$', 'DELUXE TWIN')
    all1['Room Type'] = all1['Room'].str.replace('-.*', '', regex=True)
    all1['Room Type'] = all1['Room Type'].apply(lambda x: re.sub(r'^\d+\sX\s', '', x))
    all1['Room Type'] = all1['Room Type'].apply(clean_room_type)
    all1['Room Type'] = all1['Room Type'].apply(lambda x: convert_room_type(x))
    all1['F/NRF'] = all1['Room'].apply(lambda x: convert_RF(x))
    #all1['Room Type'] = all1['Room Type'].str.replace('(NRF)', '').apply(lambda x: x.replace('()', ''))
    #all1['Room Type'] = all1['Room Type'].str.replace('WITH BREAKFAST', '')
    #all1['Room Type'] = all1['Room Type'].str.replace('ROOM ONLY', '')
    #all1['Room Type'] = all1['Room Type'].replace('', 'UNKNOWN ROOM')
    #all1['Room Type'] = all1['Room Type'].str.strip()
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
                 ,'Room Type'
                 ,'F/NRF'
                 ,'Lead time range']]
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
        st.plotly_chart(fig, use_container_width=True)
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
    color_scale1 =  {channel: colors[i % num_colors] for i, channel in enumerate(channels)}
    with col1:
        grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
        fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        grouped = filtered_df.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
        fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
        st.plotly_chart(fig,use_container_width=True)
        
    tab1, tab2, tab3 ,tab4, tab5 , tab6 ,tab7,tab8= st.tabs(["Average", "Median", "Statistic",'Data'
                                                    ,'Bar Chart','Room roomnight by channel'
                                                    ,'Room revenue by channel','Flexible/NRF'])
    with tab1:
        col0, col1, col2, col4 = st.columns(4)
        filtered_df['ADR discount'] = filtered_df["ADR"]*filtered_df["Length of stay"]*filtered_df["Quantity"]
        col0.metric('**Revenue**',f'{round(filtered_df["ADR discount"].sum(),4)}')
        col4.metric('**ADR with discount commission**',f'{round(filtered_df["ADR"].mean(),4)}',)
        col1.metric("**A.LT**", f'{round(filtered_df["Lead time"].mean(),4)}')
        col2.metric("**A.LOS**", f'{round(filtered_df["Length of stay"].mean(),4)}')
    with tab2:
        col1, col2, col3 = st.columns(3)
        col3.metric('ADR with discount commission',f'{round(filtered_df["ADR"].median(),4)}')
        col1.metric("A.LT", f'{round(filtered_df["Lead time"].median(),4)}')
        col2.metric("A.LOS", f'{round(filtered_df["Length of stay"].median(),4)}')
    with tab3:
        st.write(filtered_df.describe())
    with tab4:
        st.write(filtered_df)
    with tab5:
        tab11, tab12, tab13, tab14 = st.tabs(['A.LT','A.LOS','A.RN','ADR by month'])
        with tab14:
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Booked'].dt.month_name()])['ADR'].mean().reset_index()
            mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)

            bar_chart = px.bar(mean_adr_by_month, x='Booked', y='ADR', color='Room Type',category_orders={'Booked': month_order},
                   text='ADR')
            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
            st.plotly_chart(bar_chart, use_container_width=True)
        with tab11:
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Booked'].dt.month_name()])['Lead time'].mean().reset_index()
            mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)

            bar_chart = px.bar(mean_adr_by_month, x='Booked', y='Lead time', color='Room Type',category_orders={'Booked': month_order},
                   text='Lead time')
            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
            st.plotly_chart(bar_chart, use_container_width=True)
        with tab12:
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Booked'].dt.month_name()])['Length of stay'].mean().reset_index()
            mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)

            bar_chart = px.bar(mean_adr_by_month, x='Booked', y='Length of stay', color='Room Type',category_orders={'Booked': month_order},
                   text='Length of stay')
            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
            st.plotly_chart(bar_chart, use_container_width=True)
        with tab13:
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            mean_adr_by_month = filtered_df.groupby(['Room Type', filtered_df['Booked'].dt.month_name()])['RN'].mean().reset_index()
            mean_adr_by_month['Booked'] = pd.Categorical(mean_adr_by_month['Booked'], categories=month_order)

            bar_chart = px.bar(mean_adr_by_month, x='Booked', y='RN', color='Room Type',category_orders={'Booked': month_order},
                   text='RN')
            bar_chart.update_traces(texttemplate='%{text:.2f}', textposition='auto')
            st.plotly_chart(bar_chart, use_container_width=True)
    with tab6:
        counts = filtered_df[['Channel', 'Room Type','RN']].groupby(['Channel', 'Room Type']).sum().reset_index()
        fig = px.treemap(counts, path=['Channel', 'Room Type','RN'], values='RN', color='RN',color_continuous_scale='YlOrRd')
        st.plotly_chart(fig)
    with tab7:
        counts = filtered_df[['Channel', 'Room Type','ADR discount']].groupby(['Channel', 'Room Type']).sum().reset_index()
        fig = px.treemap(counts, path=['Channel', 'Room Type','ADR discount'], values='ADR discount', color='ADR discount',color_continuous_scale='YlOrRd')
        st.plotly_chart(fig)
    with tab8:
        counts = all2[['Channel','F/NRF']].groupby(['Channel', 'F/NRF']).size().reset_index(name='Count')
        total_count = counts['Count'].sum()
        fig = px.treemap(counts, path=['Channel', 'F/NRF'], values='Count', color='Count',color_continuous_scale='YlOrRd')
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
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['ADR'])
        st.markdown('Average ADR by booked')
        #st.bar_chart(filtered_df_pi)
        adr_avg = filtered_df.groupby(['Booked', 'Room Type'])['ADR'].mean().reset_index()
        fig = px.bar(adr_avg, x='Booked', y='ADR', color='Room Type',text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Booked', 'ADR']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)

    with t2:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['Lead time'])
        st.markdown('Average LT by booked')
        #st.bar_chart(filtered_df_pi)
        adr_LT = filtered_df.groupby(['Booked', 'Room Type'])['Lead time'].mean().reset_index()
        fig = px.bar(adr_LT, x='Booked', y='Lead time', color='Room Type',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Booked', 'Lead time range']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Lead time range',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
    with t3:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['Length of stay'])
        st.markdown('Average LOS by Booked')
        #st.bar_chart(filtered_df_pi)
        adr_LOS = filtered_df.groupby(['Booked', 'Room Type'])['Length of stay'].mean().reset_index()
        fig = px.bar(adr_LOS, x='Booked', y='Length of stay', color='Room Type',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Booked', 'Length of stay']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
    with t4:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Booked',values=['RN'])
        st.markdown('Average RN by booked')
        #st.bar_chart(filtered_df_pi)
        adr_RN = filtered_df.groupby(['Booked', 'Room Type'])['RN'].mean().reset_index()
        fig = px.bar(adr_RN, x='Booked', y='RN', color='Room Type',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Booked', 'RN']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Booked', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Booked', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)

    st.markdown('**Pivot table by lead time**')
    t1,t2,t3 = st.tabs(['ADR','LOS','RN'])
    with t1:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Lead time',values=['ADR'])
        st.markdown('Average ADR by LT')
        #st.bar_chart(filtered_df_pi)
        grouped = filtered_df.groupby(['Lead time range', 'Room Type'])['ADR'].mean().reset_index()
        fig = px.bar(grouped, x='Lead time range', y='ADR', color='Room Type',color_discrete_map=color_scale, barmode='stack',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Lead time range', 'ADR']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time range', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
    with t2:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Lead time',values=['Length of stay'])
        st.markdown('Average LOS by LT')
        #st.bar_chart(filtered_df_pi)
        grouped = filtered_df.groupby(['Lead time range', 'Room Type'])['Length of stay'].mean().reset_index()
        fig = px.bar(grouped, x='Lead time range', y='Length of stay', color='Room Type',color_discrete_map=color_scale, barmode='stack',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Lead time range', 'Length of stay']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time range', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
    with t3:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Lead time',values=['Length of stay'])
        st.markdown('Average RN by LT')
        #st.bar_chart(filtered_df_pi)
        grouped = filtered_df.groupby(['Lead time range', 'Room Type'])['RN'].mean().reset_index()
        fig = px.bar(grouped, x='Lead time range', y='RN', color='Room Type',color_discrete_map=color_scale, barmode='stack',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Lead time range', 'RN']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time range', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)

    st.markdown('**Pivot table by LOS**')
    t1,t2,t3 = st.tabs(['ADR','LT','RN'])
    with t1:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Length of stay',values=['ADR'])
        st.markdown('Average ADR by LOS')
        #st.bar_chart(filtered_df_pi)
        adr_ADR = filtered_df.groupby(['Length of stay', 'Room Type'])['ADR'].mean().reset_index()
        fig = px.bar(adr_ADR, x='Length of stay', y='ADR', color='Room Type',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Length of stay', 'ADR']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
    with t2:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Length of stay',values=['Lead time'])
        st.markdown('Average LT by LOS')
        #st.bar_chart(filtered_df_pi)
        adr_LOS = filtered_df.groupby(['Length of stay', 'Room Type'])['Lead time'].mean().reset_index()
        fig = px.bar(adr_LOS, x='Length of stay', y='Lead time', color='Room Type',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Length of stay', 'Lead time range']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='Lead time range',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
    with t3:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='Length of stay',values=['RN'])
        st.markdown('Average RN by LOS')
        #st.bar_chart(filtered_df_pi)
        adr_RN = filtered_df.groupby(['Length of stay', 'Room Type'])['RN'].mean().reset_index()
        fig = px.bar(adr_RN, x='Length of stay', y='RN', color='Room Type',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['Length of stay', 'RN']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='RN',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['Length of stay', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='Length of stay', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)

    st.markdown('**Pivot table by RN**')
    t1,t2,t3 = st.tabs(['ADR','LOS','LT'])
    with t1:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='RN',values=['ADR'])
        st.markdown('Average ADR by RN')
        #st.bar_chart(filtered_df_pi)
        adr_RN = filtered_df.groupby(['RN', 'Room Type'])['ADR'].mean().reset_index()
        fig = px.bar(adr_RN, x='RN', y='ADR', color='Room Type',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['RN', 'ADR']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='ADR',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['RN', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
    with t2:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='RN',values=['Length of stay'])
        st.markdown('Average LOS by RN')
        #st.bar_chart(filtered_df_pi)
        adr_RN = filtered_df.groupby(['RN', 'Room Type'])['Length of stay'].mean().reset_index()
        fig = px.bar(adr_RN, x='RN', y='Length of stay', color='Room Type',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['RN', 'Length of stay']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Length of stay',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['RN', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
    with t3:
        #filtered_df_pi = pd.pivot_table(filtered_df, index='RN',values=['Lead time'])
        st.markdown('Average LT by RN')
        #st.bar_chart(filtered_df_pi)
        adr_RN = filtered_df.groupby(['RN', 'Room Type'])['Lead time'].mean().reset_index()
        fig = px.bar(adr_RN, x='RN', y='Lead time', color='Room Type',text_auto=True)
        st.plotly_chart(fig,use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            grouped = filtered_df.groupby(['RN', 'Lead time range']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Lead time range',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            grouped = filtered_df.groupby(['RN', 'Channel']).size().reset_index(name='counts')
            fig = px.bar(grouped, x='RN', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
            st.plotly_chart(fig,use_container_width=True)

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
filtered_df = filtered_df[['Stay','Check-in','Guest names','Channel','ADR','Length of stay','Lead time','Lead time range','RN','Quantity','Room Type']]
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
    st.plotly_chart(fig,use_container_width=True)
with col2:
    grouped = filtered_df.groupby(['Lead time range', 'Channel']).size().reset_index(name='counts')
    fig = px.bar(grouped, x='Lead time range', y='counts', color='Channel',color_discrete_map=color_scale, barmode='stack')
    st.plotly_chart(fig,use_container_width=True)



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


