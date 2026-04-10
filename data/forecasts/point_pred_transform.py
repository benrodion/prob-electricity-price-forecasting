# quickly back-transform point predictions to obtain the real forecast values
import pandas as pd
import numpy as np
from pathlib import Path
from helpers.standardization import reshape_forecast
from helpers.standardization import MedianStandardizingScaler

### Germany ###
# for the inverse standardization, I have to recover the scales and centers first...
file_path = Path(__file__).parents[1]/'processed/ger_merged.csv'
ger_data = pd.read_csv(file_path, index_col=0, parse_dates=True)

scaler = MedianStandardizingScaler(method='median')
scaler.fit(ger_data[['day_ahead_price_eur_mwh']])
ger_centers = scaler.x_centers[0]
ger_scales = scaler.x_scales[0]


## actual inverse transformations
file_path = Path(__file__).parents[0]/'ger_lear_point.csv'
ger_data = pd.read_csv(file_path, index_col=0, parse_dates=True)
cols = ger_data.columns
for c in cols: 

    #inverse arcsinh and standardization
    ger_data[c] = np.sinh(ger_data[c])*ger_scales + ger_centers


### Spain ###
# get centers and scales
file_path = Path(__file__).parents[1]/'processed/es_merged.csv'
es_data = pd.read_csv(file_path, index_col=0, parse_dates=True)

scaler = MedianStandardizingScaler(method='median')
scaler.fit(es_data[['day_ahead_price_eur_mwh']])
es_centers = scaler.x_centers[0]
es_scales = scaler.x_scales[0]

# back-transform
file_path = Path(__file__).parents[0]/'es_lear_point.csv'
es_data = pd.read_csv(file_path,index_col=0, parse_dates=True)
cols = es_data.columns
for c in cols: 

    #inverse arcsinh and standardization
    es_data[c] = np.sinh(es_data[c])*es_scales + es_centers



# reshape and svae conventional point forecasts with the simple inverse transform
ger_data = reshape_forecast(ger_data)
es_data  = reshape_forecast(es_data)

ger_data.to_csv('data/forecasts/ger_point_pred_clean.csv')
es_data.to_csv('data/forecasts/es_point_pred_clean.csv')