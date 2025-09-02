# Forecasting gas usage

Experiment: I have gas data for 2024 and 2025 - i want to see if I can predict 2025 data based on 2024 data.

Model background: I used the SARIMA (Seasonal Autoregressive Integrated Moving Average) algorithmn, which is designed for data with seasonal patterns. The model looks at the past to predict the future. It will spot trends e.g. in winter temperature is lower than in summer.

How sales changed last month (this is the autoregressive part).
How different this month’s sales are from last month (this is called differencing to remove trends).
How sales behaved in the same month last year (to catch seasonal patterns).
The mistakes it made in predicting last month’s sales, and the mistakes from the same season last year (the moving average part).

It combines all of this by multiplying those past sales and errors by certain weights it learned from the data, then adds them up to make a fresh prediction. For example:
- If last month’s change was +10 sales,
- The same month last year the change was +8 sales,
- The prediction mistake last month was 2,
- The prediction mistake same month last year was -1,
Then: 0.5×10+0.3×8+0.4×2+0.2×(−1)=7.6
This 7.6 is the predicted change in sales for the current month after adjusting for seasonality and trends.

- S - sesonal e.g. s=12 since it's monthly data
- AR - uses past values to predict future data
- I - makes data stationary by differencing
- MA - uses past errors to be more precise

Outcome: Got a similar pattern to 2024 data! Struggled with initial data since the prediction kept flatlining and took ages to run.
Trick was to pre-process into monthly data. However, data prediction was significantly higher than 2024 data, this is likely due to the end of 2024 data going up so the data continued.

Future ideas:
- plot forecast and actual data for 2025 data
- put all data in a report
- Experiment with giving 2024 and 2025 data to predict 2026 trends.