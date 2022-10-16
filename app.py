import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

### CONFIG
st.set_page_config(
    page_title="E-commerce",
    page_icon="💸",
    layout="wide"
  )

### TITLE AND TEXT
st.title("GetAround dashboards with Streamlit 🎨")

st.markdown("""
    Welcome to this awesome `streamlit` dashboard. This library is great to build very fast and
    intuitive charts and application running on the web. Here is a showcase of what you can do with
    it. Our data comes from an e-commerce website that simply displays samples of customer sales. Let's check it out.
    Also, if you want to have a real quick overview of what streamlit is all about, feel free to watch the below video 👇
""")

### LOAD AND CACHE DATA
DATA_URL = ('get_around_delay_analysis.xlsx')

@st.cache # this lets the 
def load_data(nrows):
    data0 = pd.read_excel(DATA_URL, nrows=nrows)
    
    data = data0.merge(data0[['rental_id','delay_at_checkout_in_minutes']], left_on='previous_ended_rental_id', right_on='rental_id', how='left')

        # keeps only the delays and sets the other values to 0
    data['delay_at_checkout_in_minutes'] = data['delay_at_checkout_in_minutes_x'].apply(lambda x : x if x >0
    else 0)
    data['delay'] = data["delay_at_checkout_in_minutes"].apply(lambda x : "yes" if x > 0 else "no")
    # keeps only the delays and sets the other values to o
    data['delay_at_checkout_with_previous_rental'] = data['delay_at_checkout_in_minutes_y'].apply(lambda x : x if x >0
    else 0)
    # calculate the delay at checkin
    data['delay_at_checkin_in_minutes'] = data['delay_at_checkout_with_previous_rental'] - data['time_delta_with_previous_rental_in_minutes']
    data['delay_at_checkin_in_minutes'] = data['delay_at_checkin_in_minutes'].apply(lambda x : x if x >0 else 0)
    # create a booleen feature : delay_checkin yes or no
    data['delay_checkin'] = data['delay_at_checkin_in_minutes'].apply(lambda x : "yes" if x >0
    else "no")
    # drop the old columns
    data.drop(columns=['delay_at_checkout_in_minutes_y','delay_at_checkout_in_minutes_x','rental_id_y' ], inplace = True)
        
    return data

data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data) 

### SHOW GRAPH STREAMLIT

st.subheader("Percentage of car rental delays")
fig = px.pie(data, 'delay')
st.plotly_chart(fig, use_container_width=True)

### SHOW GRAPH PLOTLY + STREAMLIT

st.subheader("Simple bar chart built with Plotly")
st.markdown("""
    Now, the best thing about `streamlit` is its compatibility with other libraries. For example, you
    don't need to actually use built-in charts to create your dashboard, you can use :
    
    * [`plotly`](https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart) 
    * [`matplotlib`](https://docs.streamlit.io/library/api-reference/charts/st.pyplot)
    * [`bokeh`](https://docs.streamlit.io/library/api-reference/charts/st.bokeh_chart)
    * ...
    This way, you have all the flexibility you need to build awesome dashboards. 🥰
""")
fig = px.histogram(data, 
                    x = 'delay',
                    color = 'checkin_type',
                    facet_row = 'checkin_type',
                    histnorm = 'probability',
                    text_auto = '.2%',
                    title = '% delay by checkin type')

st.plotly_chart(fig, use_container_width=True)


### SIDEBAR
st.sidebar.header("Build dashboards with Streamlit")
st.sidebar.markdown("""
    * [Load and showcase data](#load-and-showcase-data)
    * [Charts directly built with Streamlit](#simple-bar-chart-built-directly-with-streamlit)
    * [Charts built with Plotly](#simple-bar-chart-built-with-plotly)
    * [Input Data](#input-data)
""")
e = st.sidebar.empty()
e.write("")
st.sidebar.write("Made with 💖 by [Jedha](https://jedha.co)")