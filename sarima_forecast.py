import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX

class ForeCast():
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

    def preproc_data(self):
        self.df['date'] = pd.to_datetime(self.df[' Start'], utc=True).dt.tz_localize(None)
        self.df.set_index('date', inplace=True)
        self.df['value'] = pd.to_numeric(self.df['Consumption (kwh)'], errors='coerce')

    def resample_mon(self):
        monthly_series = self.df['value'].resample('M').sum()
        self.df = monthly_series.to_frame(name='monthly_consumption')
        self.df.index.freq = 'M'
        self.df.to_csv('data/input_mon.csv')
        self.df['log_consumption'] = np.log(self.df['monthly_consumption'] + 1e-6)

    def ini_df(self):
        return self.df

    def fit_model(self):
        model = SARIMAX(
            self.df['monthly_consumption'],
            order=(1,1,1),
            seasonal_order=(1,1,0,12),
            trend = 'n'
        )
        model_fit = model.fit()
        forecast = model_fit.get_forecast(steps=12)

        return forecast.summary_frame()

    def plot_data(self, df, y, name):
        print(df.columns)
        sns.lineplot(
            x=df.index,
            y=df[y],
            data=df
        )
        plt.savefig(f'plots/{name}.png')
        plt.clf()

    def output_forecast_data(self, forecast_df):

        start_date = self.df.index[-1] + pd.Timedelta(days=1)
        forecast_df.index = pd.date_range(start=start_date, periods=len(forecast_df), freq='M')

        output_df = pd.DataFrame(
            data={
                "date":forecast_df.index,
                "price":forecast_df['mean']
                }
            )
        output_df.to_csv('data/forecast_data.csv')
        return output_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')

    args = parser.parse_args()
    input_filepath = args.file
    forecast = ForeCast(input_filepath)
    forecast.preproc_data()
    forecast.resample_mon()
    df = forecast.ini_df()
    forecast.plot_data(df, 'monthly_consumption', 'input_df')
    forecast_df = forecast.fit_model()
    output_df = forecast.output_forecast_data(forecast_df)
    forecast.plot_data(output_df, 'price', 'forecast_df')

