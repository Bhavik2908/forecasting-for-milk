import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load the trained ARIMA model
try:
    model = joblib.load('arima_model.joblib')
except FileNotFoundError:
    st.error("ARIMA model file 'arima_model.joblib' not found. Please ensure it's in the same directory as app.py.")
    st.stop()
except Exception as e:
    st.error(f"Error loading ARIMA model: {e}")
    st.stop()

# Load the original data to get the last date for forecasting and for plotting historical data
df_original = None # Initialize df_original
last_date = None # Initialize last_date
try:
    df_original = pd.read_csv("demand_data - demand_data.csv")
    df_original["Month"] = pd.to_datetime(df_original["Month"], format='%b-%Y')
    df_original.set_index("Month", inplace=True)

    if df_original.empty:
        st.error("Original data file 'demand_data - demand_data.csv' is empty or contains no valid data.")
        st.stop()

    last_date = df_original.index[-1]
except FileNotFoundError:
    st.error("Original data file 'demand_data - demand_data.csv' not found. Please ensure it's in the same directory as app.py.")
    st.stop()
except Exception as e:
    st.error(f"Error loading or processing original data: {e}")
    st.stop()

st.title('Demand Forecasting App')
st.write('Forecast future demand using the trained ARIMA model.')

# User input for number of periods to forecast
periods = st.slider('Select number of periods to forecast (months):', 1, 36, 12)

if st.button('Generate Forecast'):
    if periods > 0:
        # Make predictions
        forecast = model.predict(n_periods=periods)

        # Create a date range for the forecast
        if last_date is None:
            st.error("Could not determine the last date from the original data. Cannot generate forecast index.")
            st.stop()

        forecast_index = pd.date_range(start=last_date, periods=periods + 1, freq='MS')[1:] # Exclude the start date itself
        forecast_df = pd.DataFrame(forecast, index=forecast_index, columns=['Forecasted Demand_000L'])

        st.subheader(f'Forecasted Demand for the next {periods} months:')
        st.dataframe(forecast_df)

        # Plotting the forecast
        fig, ax = plt.subplots(figsize=(10, 6))
        if df_original is not None and not df_original.empty:
            ax.plot(df_original['Demand_000L'], label='Historical Demand', marker='o')
        else:
            st.warning("Historical data could not be plotted as the original dataframe was not loaded or was empty.")

        ax.plot(forecast_df['Forecasted Demand_000L'], label='Forecasted Demand', color='red', linestyle='--', marker='x')
        ax.set_title('Demand Forecast')
        ax.set_xlabel('Date')
        ax.set_ylabel('Demand (000L)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    else:
        st.warning('Please select at least 1 period to forecast.')



       
        
