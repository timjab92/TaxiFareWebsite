import streamlit as st
import requests
import datetime
import json
import pandas as pd
'''
# TaxiFareModel - What's a fair price for the fare?
'''

st.markdown('''
Ever been to New York City, riding a cab, wondering how much you should actually pay for your ride?

This website provides an accurate prediction of how much a taxiride in New York should cost.
''')
'''
## To make a prediction, I have to ask you for some information:
'''
date = st.date_input('Whats your current data?', datetime.date.today())
time = st.time_input('Whats your current time?', datetime.datetime.now())
pickup_datetime = str(date ) +" "+ str(time)
pickup_lon = st.number_input('Whats your pickup longitude?', value=-73.9682)
pickup_lat = st.number_input('Whats your pickup latitude?', value=40.7850)
dropoff_lon = st.number_input('Whats your dropoff longitude?', value=-73.9854)
dropoff_lat = st.number_input('Whats your dropoff latitude?', value=40.7488)
passenger_count = st.number_input('How many people are you?', min_value=0, max_value=10, value=1)
'''
## Thank you very much. Click the button to make the prediction ...
'''
url = 'https://taxifare.lewagon.ai/predict'

# 2. Let's build a dictionary containing the parameters for our API...
params = {
    'pickup_datetime': pickup_datetime,
    'pickup_longitude': str(pickup_lon),
    'pickup_latitude': str(pickup_lat),
    'dropoff_longitude': str(dropoff_lon),
    'dropoff_latitude': str(dropoff_lat),
    'passenger_count': str(passenger_count)}


@st.cache
def get_map_data():
    print('get_map_data called')
    return pd.DataFrame({'lat': [pickup_lat, dropoff_lat],
                         'lon': [pickup_lon, dropoff_lon]})
st.map(get_map_data())




if st.checkbox('Make prediction'):
    import time
    # 3. Let's call our API using the `requests` package...
    response = requests.get(url, params = params).json()

    # 4. Let's retrieve the prediction from the **JSON** returned by the API...
    prediction = response['prediction']

    'Making your prediction...'

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        #latest_iteration.text('Calculating...')
        bar.progress(i + 1)
        time.sleep(0.01)

    '...and we\'re done!'
    f'Fare should cost no more than {round(prediction,2)}$.'
