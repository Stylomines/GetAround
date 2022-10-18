import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

### CONFIG
st.set_page_config(
    page_title="GetAround",
    layout="wide"
  )

### TITLE AND TEXT
st.title("GetAround dashboards")

st.markdown("""
    Analysis of delays in car rentals
""")

### LOAD AND CACHE DATA
DATA_URL = ('get_around_delay_analysis.xlsx')

@st.cache # this lets the 
def load_data():
    data0 = pd.read_excel(DATA_URL)
    
    data = data0.merge(data0[['rental_id','delay_at_checkout_in_minutes']], left_on='previous_ended_rental_id', right_on='rental_id', how='left')

        # keeps only the delays and sets the other values to 0
    data['delay_at_checkout_in_minutes'] = data['delay_at_checkout_in_minutes_x'].apply(lambda x : x if x >0
    else 0)
    data['delay'] = data["delay_at_checkout_in_minutes"].apply(lambda x : "yes" if x > 0 else "no")
    # keeps only the delays and sets the other values to 0
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

data_load_state = st.text('Loading and processing data...')
data = load_data()
data_load_state.text("data load ✅") # change text from "Loading data..." to "" once the the load_data function has run

## Run the below code if the check is checked ✅
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data) 

### SHOW Percentage of car rental delays

st.subheader("Percentage of car rental delays")
st.markdown(f"""

    * number of delays : {sum(data["delay"]=="yes")}
    * number of rental cars : {len(data["delay"])}
   
""")
fig = px.pie(data, 'delay')
st.plotly_chart(fig, use_container_width=True)

### SHOW GRAPH delay by checkin type

st.subheader("Delay by checkin type")

st.markdown(f"""
   The main checkin is mobile but with lot of canceled
""")

fig = px.histogram(data, 
                    x = 'checkin_type',
                    color = 'delay',
                    text_auto = '.0f',
                    barmode = 'group',
                    title = 'delay by checkin type')


st.plotly_chart(fig, use_container_width=True)

### SHOW GRAPH Impact to the next driver

st.subheader("Impact to the next driver")
st.markdown(f"""
   Only {sum(data['delay_checkin']=="yes")} impact impact to the next driver for {sum(data["delay"]=="yes")} delays
""")
fig = px.histogram(data[data['delay_checkin']=="yes"],
                    x = "state",
                    color = 'state',
                    text_auto = '.0f',
                    )


st.plotly_chart(fig, use_container_width=True)

### SHOW GRAPH Rentals affected in function connect & mobile

st.subheader("Rentals affected")

st.markdown(f"""
   Rentals affected in function of time and by connect & mobile
""")

fig = px.histogram(data[data["previous_ended_rental_id"].notna()],
                    x ='time_delta_with_previous_rental_in_minutes',
                    color = 'checkin_type',
                    range_x = [0,600],
                    range_y = [0,1600],
                    nbins=3000,
                    cumulative = True
                    )

st.plotly_chart(fig, use_container_width=True)


### SHOW GRAPH Problematic cases in fonction connect & mobile

st.subheader("Problematic cases")

st.markdown(f"""
   Problematic cases in function of time and by connect & mobile
""")

fig = px.histogram(data[data['delay_at_checkin_in_minutes']>0],
                    x ='delay_at_checkin_in_minutes',
                    color = 'checkin_type',
                    range_x = [0,300],
                    nbins=3000,
                    cumulative = True
                    )

st.plotly_chart(fig, use_container_width=True)



### SHOW Threshold in percentage

st.subheader("Threshold in percentage")

st.markdown("""
   Percentage of rentals affected and problematic cases solved and in fonction connect & mobile
""")

with st.form("average_sales_per_country"):
    checkin_type = st.selectbox("Select type oo checkin", ["all","connect", "mobile"])
    minutes = st.number_input("Select the minimum delay", min_value = 0, step=1)
    
    submit = st.form_submit_button("submit")

    if submit:

        df_with_previous_rental = data[data["previous_ended_rental_id"].notna()]
    
        if checkin_type == "all":
            df_delay_checkin = data[data['delay_at_checkin_in_minutes']>0]
        
            st.markdown(f"""Percentage of rentals affected : 
            {round(100*len(df_with_previous_rental[df_with_previous_rental['time_delta_with_previous_rental_in_minutes']<minutes]
            )/len(df_with_previous_rental),2)}%""")
            st.markdown(f"""Percentage of problematic cases solved :
            {round(100*len(df_delay_checkin[df_delay_checkin['delay_at_checkin_in_minutes']<=minutes])/len(df_delay_checkin),2)} %""")
        else:
            df = df_with_previous_rental[df_with_previous_rental['checkin_type']==checkin_type]
            df_delay_checkin = df[df['delay_at_checkin_in_minutes']>0]
        
            st.markdown(f"""Percentage of rentals affected:
            {round(100*len(df[df['time_delta_with_previous_rental_in_minutes']<minutes])/len(df),2)}%""")
            st.markdown(f"""Percentage of problematic cases solved :
            {round(100*len(df_delay_checkin[df_delay_checkin['delay_at_checkin_in_minutes']<=minutes])/len(df_delay_checkin),2)} %""")
        

### SIDEBAR
st.sidebar.header("GetAround")
st.sidebar.markdown("""
    * [Percentage of car rental delays](#Percentage-of-car-rental-delays)
    * [Delay by checkin type](#Delay-by-checkin-type)
    * [Impact to the next driver](#Impact-to-the-next-driver)
    * [Rentals affected](#Rentals-affected)
    * [Problematic cases](#Problematic-cases)
    * [Threshold in percentage](#Threshold-in-percentage)
""")
e = st.sidebar.empty()
e.write("")
st.sidebar.write("Made with 💖 by Sylvain")