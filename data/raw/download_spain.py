import pandas as pd
from entsoe import EntsoePandasClient
from dotenv import load_dotenv
from pathlib import Path
import os

# set up client
load_dotenv(dotenv_path=Path(__file__).parents[2] / 'config/.env')
API_KEY = os.getenv('API_KEY') # IMPORTANT: if you cloned this repo, you need to insert your own ENTSOE-API key here
client = EntsoePandasClient(api_key=API_KEY)

country_code = 'ES'
start = pd.Timestamp('20141223', tz='Europe/Madrid') #start 2014 for timelag data for  start of 2015
end   = pd.Timestamp('20251001', tz='Europe/Madrid')

# get data
day_ahead_prices = client.query_day_ahead_prices(country_code, start=start, end=end)
load_forecast = client.query_load_forecast(country_code, start=start, end=end)
wind_solar_forecast  = client.query_wind_and_solar_forecast(country_code, start=start, end=end, psr_type=None)

# resample to hourly
day_ahead_prices=day_ahead_prices.resample('h').mean()
load_forecast = load_forecast.resample('h').mean()
wind_solar_forecast = wind_solar_forecast.resample('h').mean()


df = pd.DataFrame({'day_ahead_price_eur_mwh': day_ahead_prices})
df =df.join(load_forecast.add_suffix('_mw'))
df = df.join(wind_solar_forecast.add_suffix('_mw'))

print(df.head())
print(df.columns.tolist())
print(df.shape)

# save df 
df.to_csv('data/raw/entsoe_spain_2015_2025.csv')

