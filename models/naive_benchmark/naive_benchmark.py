import pandas as pd

def seasonal_naive_forecast(df, value_col='day_ahead_price_eur_mwh'):
    df = df.copy()

    lookup = df[value_col].to_dict()

    forecasts=[]
    for date in df.index:
        weekday = date.weekday()

        if weekday in [0, 5, 6]:
            lag = pd.Timedelta(days=7)
        else:
            lag = pd.Timedelta(days=1)
        forecast = date - lag
        forecasts.append(lookup.get(forecast, None))
    df['forecast_naive_bench_eur_mwh'] = forecasts
    return df
