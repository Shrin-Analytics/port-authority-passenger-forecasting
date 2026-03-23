import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pmdarima import auto_arima

# Load dataset
df = pd.read_excel("FinalWeeklyRidership.xlsx")

# Convert date column
df["WeekStartDate"] = pd.to_datetime(df["WeekStartDate"])

# Aggregate weekly passenger count
weekly_df = df.groupby("WeekStartDate")["PassengerCount"].sum().reset_index()

# Sort and set index
weekly_df = weekly_df.sort_values("WeekStartDate")
weekly_df.set_index("WeekStartDate", inplace=True)

# Set weekly frequency
weekly_df = weekly_df.asfreq("W-MON")

# Fill missing values
weekly_df["PassengerCount"] = weekly_df["PassengerCount"].interpolate()

# -----------------------------
# Exponential Smoothing Model
# -----------------------------
exp_model = ExponentialSmoothing(
    weekly_df["PassengerCount"],
    trend="add",
    seasonal=None
)
exp_fit = exp_model.fit()

exp_forecast = exp_fit.forecast(steps=260)

# Future dates
future_dates = pd.date_range(
    start=weekly_df.index[-1] + pd.Timedelta(weeks=1),
    periods=260,
    freq="W-MON"
)

exp_forecast = pd.Series(exp_forecast.values, index=future_dates)

# Plot Exponential Smoothing
plt.figure(figsize=(12,6))
plt.plot(weekly_df.index, weekly_df["PassengerCount"], label="Actual")
plt.plot(exp_forecast.index, exp_forecast, label="Exp Smoothing Forecast")
plt.axvline(x=weekly_df.index[-1], linestyle="--", label="Forecast Start")
plt.title("Exponential Smoothing Forecast (2026–2030)")
plt.xlabel("Week")
plt.ylabel("Passenger Count")
plt.legend()
plt.tight_layout()
plt.savefig("exp_forecast.png")
#plt.show()

# -----------------------------
# ARIMA Model
# -----------------------------
# ARIMA Model
from pmdarima import auto_arima

arima_model = auto_arima(
    weekly_df["PassengerCount"],
    seasonal=False,
    trace=True,
    error_action="ignore",
    suppress_warnings=True
)

arima_forecast = arima_model.predict(n_periods=260)

future_dates_arima = pd.date_range(
    start=weekly_df.index[-1] + pd.Timedelta(weeks=1),
    periods=260,
    freq="W-MON"
)

arima_forecast = pd.Series(arima_forecast, index=future_dates_arima)

print("ARIMA model built successfully")

# Plot ARIMA
plt.figure(figsize=(12,6))
plt.plot(weekly_df.index, weekly_df["PassengerCount"], label="Actual")
plt.plot(arima_forecast.index, arima_forecast, label="ARIMA Forecast")
plt.axvline(x=weekly_df.index[-1], linestyle="--", label="Forecast Start")
plt.title("ARIMA Forecast (2026–2030)")
plt.legend()

plt.savefig("arima_forecast.png")

plt.show(block=False)
plt.close()

from sklearn.metrics import mean_absolute_error

# Align actual and predicted (last part)
actual = weekly_df["PassengerCount"]

exp_pred = exp_forecast[:len(actual)]
arima_pred = arima_forecast[:len(actual)]

# Calculate MAE
exp_mae = mean_absolute_error(actual, exp_pred)
arima_mae = mean_absolute_error(actual, arima_pred)

print("Exponential Smoothing MAE:", exp_mae)
print("ARIMA MAE:", arima_mae)


from sklearn.metrics import mean_squared_error
import numpy as np

exp_rmse = np.sqrt(mean_squared_error(actual, exp_pred))
arima_rmse = np.sqrt(mean_squared_error(actual, arima_pred))

print("Exponential Smoothing RMSE:", exp_rmse)
print("ARIMA RMSE:", arima_rmse)
