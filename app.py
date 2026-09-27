
import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Load the trained ARIMA model
model = joblib.load('arima_model.joblib')

st.title('Demand Forecasting App')
st.write('Forecast future demand using the trained ARIMA model.')

# User input for number of periods to forecast
periods = st.slider('Select number of periods to forecast (months):', 1, 36, 12)

if st.button('Generate Forecast'):
    if periods > 0:
        # Make predictions
        forecast = model.predict(n_periods=periods)

        # Create a date range for the forecast (assuming monthly data starting from last known date in original df)
        # Assuming df is available from previous cells or loaded
        # For demonstration, we'll create a dummy date index if df is not directly accessible here
        try:
            # Get the last date from the original dataframe
            last_date = pd.to_datetime(df.index[-1])
        except NameError:
            st.error("Original dataframe 'df' not found. Please ensure it's loaded in the session.")
            st.stop()
        except IndexError:
            st.error("Original dataframe 'df' is empty.")
            st.stop()

        forecast_index = pd.date_range(start=last_date, periods=periods + 1, freq='MS')[1:] # Exclude the start date itself
        forecast_df = pd.DataFrame(forecast, index=forecast_index, columns=['Forecasted Demand_000L'])

        st.subheader(f'Forecasted Demand for the next {periods} months:')
        st.dataframe(forecast_df)

        # Plotting the forecast
        fig, ax = plt.subplots(figsize=(10, 6))
        if 'df' in locals(): # Plot original data if available
            ax.plot(df['Demand_000L'], label='Historical Demand', marker='o')
        ax.plot(forecast_df['Forecasted Demand_000L'], label='Forecasted Demand', color='red', linestyle='--', marker='x')
        ax.set_title('Demand Forecast')
        ax.set_xlabel('Date')
        ax.set_ylabel('Demand (000L)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    else:
        st.warning('Please select at least 1 period to forecast.')
