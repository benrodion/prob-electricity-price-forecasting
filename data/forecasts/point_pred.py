from models.lear.model import  rolling_lear
from helpers.standardization import reshape_forecast
from pathlib import Path
import pandas as pd

### Germany ###
file_path=Path(__file__).parents[1] / 'processed/ger_merged.csv'
ger_data = pd.read_csv(file_path, parse_dates=True, index_col=0)
test_days= pd.date_range(start='2020-01-01', end= '2025-09-30')
feature_cols = ger_data.columns[1:]
target_col = ger_data.columns[0]
#  6 months calibration window
ger_6_forecast, ger_6_lambdas = rolling_lear(df=ger_data, feature_cols=feature_cols, target_col=target_col,
                              calibration_window=182, test_days=test_days)

print('Germany 6 months pred done')
#12 months calibration window
ger_12_forecast, ger_12_lambdas = rolling_lear(df=ger_data, feature_cols=feature_cols, target_col=target_col,
                              calibration_window=364, test_days=test_days)
print('Germany 12 months pred done')
#18 months calibration widnow
ger_18_forecast, ger_18_lambdas = rolling_lear(df=ger_data, feature_cols=feature_cols, target_col=target_col,
                              calibration_window=546, test_days=test_days)
print('Germany 18 months pred done')
# 24 month calibration window
ger_24_forecast, ger_24_lambdas = rolling_lear(df=ger_data, feature_cols=feature_cols, target_col=target_col,
                              calibration_window=728, test_days=test_days)

print('Germany 24 months pred done')

ger_forecast_transformed = (ger_6_forecast.add_suffix('_6m').merge(ger_12_forecast.add_suffix('_12m'), left_index=True, right_index=True)
                            .merge(ger_18_forecast.add_suffix('_18m'), left_index=True, right_index=True)
                            .merge(ger_24_forecast.add_suffix('_24m'),left_index=True, right_index=True))

ger_lambdas_transformed = (ger_6_lambdas.add_suffix('_6m').merge(ger_12_lambdas.add_suffix('_12m'), left_index=True, right_index=True)
                           .merge(ger_18_lambdas.add_suffix('_18m'), left_index=True, right_index=True)
                           .merge(ger_24_lambdas.add_suffix('_24m'), left_index=True, right_index=True))

### Spain ###
file_path=Path(__file__).parents[1] / 'processed/es_merged.csv'
es_data = pd.read_csv(file_path, index_col=0, parse_dates=True)
#  6 months calibration window
es_6_forecast, es_6_lambdas = rolling_lear(df=es_data, feature_cols=feature_cols, target_col=target_col,
                              calibration_window=182, test_days=test_days)
print('Spain 6 months pred done')
#12 months calibration window
es_12_forecast, es_12_lambdas = rolling_lear(df=es_data, feature_cols=feature_cols, target_col=target_col,
                              calibration_window=364, test_days=test_days)
print('Spain 12 months pred done')
#18 months calibration widnow
es_18_forecast, es_18_lambdas = rolling_lear(df=es_data, feature_cols=feature_cols, target_col=target_col,
                              calibration_window=546, test_days=test_days)

print('Spain 18 months pred done')
# 24 month calibration window
es_24_forecast, es_24_lambdas = rolling_lear(df=es_data, feature_cols=feature_cols, target_col=target_col,
                              calibration_window=728, test_days=test_days)
print('Spain 24 months pred done')

es_forecast_transformed = (es_6_forecast.add_suffix('_6m').merge(es_12_forecast.add_suffix('_12m'), left_index=True, right_index=True)
                .merge(es_18_forecast.add_suffix('_18m'), left_index=True, right_index=True)
                .merge(es_24_forecast.add_suffix('_24m'),left_index=True, right_index=True))

es_lambdas_transformed = (es_6_lambdas.add_suffix('_6m')
                .merge(es_12_lambdas.add_suffix('_12m'), left_index=True, right_index=True)
                .merge(es_18_lambdas.add_suffix('_18m'), left_index=True, right_index=True)
                .merge(es_24_lambdas.add_suffix('_24m'), left_index=True, right_index=True))


ger_forecast_transformed.to_csv('data/forecasts/ger_lear_point.csv')
es_forecast_transformed.to_csv('data/forecasts/es_lear_point.csv')
ger_lambdas_transformed.to_csv('data/forecasts/ger_lear_lambdas.csv')
es_lambdas_transformed.to_csv('data/forecasts/es_lear_lambdas.csv')
