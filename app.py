import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load the trained ARIMA model
try:
    model = joblib.load('arima_model.joblib')

st.title('Demand Forecasting App')
st.write('Forecast future demand using the trained ARIMA model.')

# User input for number of periods to forecast
periods = st.slider('Select number of periods to forecast (months):', 1, 36, 12)

if st.button('Generate Forecast'):
    if periods > 0:
        # Make predictions
        forecast = model.predict(n_periods=periods)
       
        
