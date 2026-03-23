# Port Authority Passenger Forecasting (2026–2030)

## Project Overview
This project represents Phase-2 of a larger data analytics project and focuses on forecasting passenger demand for the Port Authority Bus Terminal using Python time series models.

## Models Used
- Exponential Smoothing (Holt’s Linear Trend)
- ARIMA (Auto ARIMA)

## Evaluation Metrics
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)

## Results
Exponential Smoothing performed better than ARIMA based on both MAE and RMSE.

## Forecast Visualizations

### Exponential Smoothing Forecast
![Exponential Forecast](exp_forecast.png)

### ARIMA Forecast
![ARIMA Forecast](arima_forecast.png)


## Key Insights
- Passenger demand shows a steady upward trend
- Seasonal variation was not strong enough to improve model accuracy significantly
- Long-term trend plays a more significant role than seasonality in this dataset

## Tools & Technologies
- Python
- Pandas
- Statsmodels
- pmdarima
- Matplotlib

## Files
- `forecast.py` - forecasting code
- `passenger_forcasting_report.pdf` - final report
- `exp_forecast.png` - Exponential Smoothing forecast plot
- `arima_forecast.png` - ARIMA forecast plot
