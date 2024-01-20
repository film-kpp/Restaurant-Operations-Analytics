import streamlit as st
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Restaurant Operations Analytics", page_icon=":cook:", layout="wide")

st.title(" :cook: Restaurant Operations Analytics")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

df = pd.read_csv("test_data.csv", encoding = "ISO-8859-1")

col1, col2 = st.columns((2))

df["Month"] = pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.month_name()

month_order = ['June', 'July', 'August', 'September', 'October', 'November', 'December']
df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

num_orders = df.groupby(['Month', 'Category']).size().reset_index(name='Count')

with col1:
    st.subheader('Overall quantity of products sold by category')
    fig1 = px.line(num_orders, x="Month", y='Count', color='Category',
                  labels={'Count': 'Number of Orders'},
                  height=500, width=1000, template="gridon")
    st.plotly_chart(fig1, use_container_width=True)

linechart = df.groupby(['Month', 'Category'])["Price"].sum().reset_index()

with col2:
    st.subheader('Overall Sales by category')
    fig2 = px.line(linechart, x="Month", y="Price", color="Category",
                   labels={"Price": "Amount"}, 
                   height=500, width=1000, template="gridon")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns((2))

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df["Day Of Week"] = pd.Categorical(df["Day Of Week"], categories=day_order, ordered=True)

category_count = df.groupby(['Day Of Week', 'Category']).size().reset_index(name='Count')

with col3:
    st.subheader('Quantity of products sold by Day of the week')
    fig3 = px.bar(category_count, x='Day Of Week', y='Count', color='Category',
                 labels={'Count': 'Number of Orders'}, height=500, width=1000, 
                 template="gridon", barmode='group')
    st.plotly_chart(fig3, use_container_width=True)

menu_order_counts = df['Menu'].value_counts().reset_index()
menu_order_counts.columns = ['Menu', 'Number of Orders']
menu_order_counts = menu_order_counts.sort_values(by='Number of Orders', ascending=True)

with col4:
    st.subheader('Menu Popularity')
    fig4 = px.bar(menu_order_counts, x='Number of Orders', y='Menu',
                  labels={'Number of Orders': 'Number of Orders'},
                  orientation='h', height=500, width=700, template="gridon")
    st.plotly_chart(fig4, use_container_width=True)

col5, col6 = st.columns((2))

food_df = df[df['Category'] == 'food']

with col5:
    st.subheader('Distribution of Food Order Times Throughout the Day')
    fig5 = px.histogram(food_df, x='Hour', nbins=24,
                        labels={'Hour': 'Hour of the Day', 'count': 'Number of Orders'},
                        template="gridon")
    st.plotly_chart(fig5, use_container_width=True)

drink_df = df[df['Category'] == 'drink']

with col6:
    st.subheader('Distribution of Drink Order Times Throughout the Day')
    fig6 = px.histogram(drink_df, x='Hour', nbins=24,
                  labels={'Hour': 'Hour of the Day', 'count': 'Number of Orders'},
                  template="gridon")
    st.plotly_chart(fig6, use_container_width=True)

col7, col8 = st.columns((2))

df['Serve Time'] = pd.to_datetime(df['Serve Time'], format="%d/%m/%Y %H:%M")
df['Order Time'] = pd.to_datetime(df['Order Time'], format="%d/%m/%Y %H:%M")

df['Cooking Time'] = (df['Serve Time'] - df['Order Time']).dt.total_seconds() / 60

with col7:
    st.subheader('Distribution of Cooking Times by Category')
    fig7 = px.box(df, x='Category', y='Cooking Time',
             labels={'Cooking Time': 'Cooking Time (minutes)', 'Category': 'Category'},
             template="gridon", points="all")
    st.plotly_chart(fig7, use_container_width=True)

sales_hourly = df.groupby(['Hour', 'Category'])["Price"].sum().reset_index()

with col8:
    st.subheader('Hourly Sales by category')
    fig8 = px.line(sales_hourly, x="Hour", y="Price", color="Category",
                          labels={"Price": "Amount"}, 
                          template="gridon")
    st.plotly_chart(fig8, use_container_width=True)
    