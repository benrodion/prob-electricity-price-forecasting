### Evaluate LEAR point forecasts:
from pathlib import Path
import pandas as pd
from scipy import stats
### 1. Get residuals for all forecasts for plotting ###
# Germany 
file_path=Path(__file__).parents[1] / 'data/forecasts/ger_point_pred_clean.csv'
ger_forecasts = pd.read_csv(file_path, index_col=0, parse_dates=True) 
file_path=Path(__file__).parents[1] / 'data/processed/ger_merged.csv'
ger_merged = pd.read_csv(file_path, index_col=0, parse_dates=True) #original price data

# merge forecasts and price data on index
ger_full = ger_forecasts.merge(ger_merged['day_ahead_price_eur_mwh'], how='inner', left_index=True, right_index=True)

ger_res_dict = {}
ger_forecast_cols = ger_forecasts.columns
print(ger_full.index.difference(ger_merged.index))
for col in ger_forecast_cols:
    ger_res_dict[f'res_{col}'] = ger_full['day_ahead_price_eur_mwh'] - ger_full[col]

ger_res = pd.DataFrame(ger_res_dict)
ger_res.to_csv('data/residuals/ger_lear_residuals.csv')

# Spain 
file_path=Path(__file__).parents[1] / 'data/forecasts/es_point_pred_clean.csv'
es_forecasts = pd.read_csv(file_path, index_col=0, parse_dates=True)
file_path=Path(__file__).parents[1] / 'data/processed/es_merged.csv'
es_merged = pd.read_csv(file_path, index_col=0, parse_dates=True) #original price data

# merge forecasts and price data on index
es_full = es_forecasts.merge(es_merged['day_ahead_price_eur_mwh'], how='inner', left_index=True, right_index=True)

es_res_dict = {}
es_forecast_cols = es_forecasts.columns
print(es_full.index.difference(es_merged.index))
for col in es_forecast_cols:
    es_res_dict[f'res_{col}'] = es_full['day_ahead_price_eur_mwh'] - es_full[col]

es_res = pd.DataFrame(es_res_dict)
es_res.to_csv('data/residuals/es_lear_residuals.csv')

### 2. Calculate MAE/rMSE ###
from sklearn.metrics import mean_absolute_error as mae 
from sklearn.metrics import root_mean_squared_error as rmse
# Germany 
# MAE
ger_mae_dict= {}
for col in ger_forecast_cols:
    ger_mae_dict[f'mae_{col}'] = mae(ger_full['day_ahead_price_eur_mwh'], ger_full[col])
ger_mae = pd.Series(ger_mae_dict)


#rMSE
ger_rmse_dict= {}
for col in ger_forecast_cols:
    ger_rmse_dict[f'rmse{col}'] = rmse(ger_full['day_ahead_price_eur_mwh'], ger_full[col])
ger_rmse = pd.Series(ger_rmse_dict)

# check out residuals for any biases
print('=== GERMANY ===')
ger_res['year'] = ger_res.index.year
res_cols_ger = [c for c in ger_res.columns if c != 'year']

print('\nMean residual by year and calibration window')
print(ger_res.groupby('year')[res_cols_ger].mean().to_string(float_format=lambda x: f'{x:.4f}'))

print('\nMedian residual by year and calibration window')
print(ger_res.groupby('year')[res_cols_ger].median().to_string(float_format=lambda x: f'{x:.4f}'))

print('\nSkewness by year and calibration window')
print(ger_res.groupby('year')[res_cols_ger].skew().to_string(float_format=lambda x: f'{x:.4f}'))

print('\n% of residuals > 0 by year and calibration window')
print(ger_res.groupby('year')[res_cols_ger].apply(lambda g: (g > 0).mean() * 100).to_string(float_format=lambda x: f'{x:.1f}'))

print('\nMAE by year and calibration window')
print(ger_res.groupby('year')[res_cols_ger].apply(lambda g: g.abs().mean()).to_string(float_format=lambda x: f'{x:.4f}'))

print('\nRMSE by year and calibration window')
print(ger_res.groupby('year')[res_cols_ger].apply(lambda g: (g**2).mean()**0.5).to_string(float_format=lambda x: f'{x:.4f}'))

print('\n t-test: mean residual significantly different from 0?')
for col in res_cols_ger:
    t, p = stats.ttest_1samp(ger_res[col].dropna(), 0)
    print(f'{col}: t={t:.4f}, p={p:.4f}') # Victor says this is fine

# Spain
#MAE
es_mae_dict= {}
for col in es_forecast_cols:
    es_mae_dict[f'mae_{col}'] = mae(es_full['day_ahead_price_eur_mwh'], es_full[col])
es_mae = pd.Series(es_mae_dict)


#rMSE
es_rmse_dict= {}
for col in es_forecast_cols:
    es_rmse_dict[f'rmse{col}'] = rmse(es_full['day_ahead_price_eur_mwh'], es_full[col])
es_rmse = pd.Series(es_rmse_dict)

# check out residuals for any biases
print('=== SPAIN ===')
es_res['year'] = es_res.index.year
res_cols_es = [c for c in es_res.columns if c != 'year']

print('\nMean residual by year and calibration window')
print(es_res.groupby('year')[res_cols_es].mean().to_string(float_format=lambda x: f'{x:.4f}'))

print('\nMedian residual by year and calibration window')
print(es_res.groupby('year')[res_cols_es].median().to_string(float_format=lambda x: f'{x:.4f}'))

print('\nSkewness by year and calibration window')
print(es_res.groupby('year')[res_cols_es].skew().to_string(float_format=lambda x: f'{x:.4f}'))

print('\n% of residuals > 0 by year and calibration window')
print(es_res.groupby('year')[res_cols_es].apply(lambda g: (g > 0).mean() * 100).to_string(float_format=lambda x: f'{x:.1f}'))

print('\nMAE by year and calibration window')
print(es_res.groupby('year')[res_cols_es].apply(lambda g: g.abs().mean()).to_string(float_format=lambda x: f'{x:.4f}'))

print('\nRMSE by year and calibration window')
print(es_res.groupby('year')[res_cols_es].apply(lambda g: (g**2).mean()**0.5).to_string(float_format=lambda x: f'{x:.4f}'))

print('\n t-test: mean residual significantly different from 0?')
for col in res_cols_es:
    t, p = stats.ttest_1samp(es_res[col].dropna(), 0)
    print(f'{col}: t={t:.4f}, p={p:.4f}') # Victor says this is fine



### Benchmark for Comparison ###
from models.naive_benchmark import naive_benchmark
# Germany
ger_point_benchmark = naive_benchmark.seasonal_naive_forecast(df=ger_merged)

# Benchmark residuals
ger_point_benchmark['residuals'] = ger_point_benchmark['day_ahead_price_eur_mwh'] - ger_point_benchmark['forecast_naive_bench_eur_mwh']
print(ger_point_benchmark['forecast_naive_bench_eur_mwh'].isna().sum())
ger_point_benchmark = ger_point_benchmark.loc[ger_full.index].dropna()  # align to test period
ger_point_benchmark.to_csv('data/forecasts/ger_point_benchmark.csv')

# MAE/rMSE
ger_mae['point_benchmark'] = mae(ger_point_benchmark['day_ahead_price_eur_mwh'], ger_point_benchmark['forecast_naive_bench_eur_mwh'])
ger_mae.to_csv('data/residuals/ger_mae.csv')
ger_rmse['point_benchmark'] = rmse(ger_point_benchmark['day_ahead_price_eur_mwh'], ger_point_benchmark['forecast_naive_bench_eur_mwh'])
ger_rmse.to_csv('data/residuals/ger_rmse.csv')

print('\n=== GERMANY BENCHMARK ===')
ger_point_benchmark['year'] = ger_point_benchmark.index.year
print('\nBenchmark MAE by year')
print(ger_point_benchmark.groupby('year').apply(lambda g: g['residuals'].abs().mean()).to_string(float_format=lambda x: f'{x:.4f}'))
print('\nBenchmark RMSE by year')
print(ger_point_benchmark.groupby('year').apply(lambda g: (g['residuals']**2).mean()**0.5).to_string(float_format=lambda x: f'{x:.4f}'))


# Spain
es_point_benchmark = naive_benchmark.seasonal_naive_forecast(df=es_merged)
# benchmark residuals
es_point_benchmark['residuals'] = es_point_benchmark['day_ahead_price_eur_mwh'] - es_point_benchmark['forecast_naive_bench_eur_mwh']
print(es_point_benchmark['forecast_naive_bench_eur_mwh'].isna().sum())
es_point_benchmark = es_point_benchmark.loc[es_full.index].dropna()  # align to test period
es_point_benchmark.to_csv('data/forecasts/es_point_benchmark.csv')

# MAE/rMSE
es_mae['point_benchmark'] = mae(es_point_benchmark['day_ahead_price_eur_mwh'], es_point_benchmark['forecast_naive_bench_eur_mwh'])
es_mae.to_csv('data/residuals/es_mae.csv')
es_rmse['point_benchmark'] = rmse(es_point_benchmark['day_ahead_price_eur_mwh'], es_point_benchmark['forecast_naive_bench_eur_mwh'])
es_rmse.to_csv('data/residuals/es_rmse.csv')

print('\n=== SPAIN BENCHMARK ===')
es_point_benchmark['year'] = es_point_benchmark.index.year
print('\nBenchmark MAE by year')
print(es_point_benchmark.groupby('year').apply(lambda g: g['residuals'].abs().mean()).to_string(float_format=lambda x: f'{x:.4f}'))
print('\nBenchmark RMSE by year')
print(es_point_benchmark.groupby('year').apply(lambda g: (g['residuals']**2).mean()**0.5).to_string(float_format=lambda x: f'{x:.4f}'))




#### 3. Diebold-Mariano test: verify if all LEAR models significantly outperform the benchmark ###
from epftoolbox.evaluation import DM
# Germany
# realign forecast data to handle differences in data length from dropping NA
common_idx = ger_full.index.intersection(ger_point_benchmark.index)
print(len(common_idx) % 24 == 0) # conditinoo not met, so I have to remove any incomplete days

# only select days with all 24h represented
# only 73 observations disappear because of this operation (37104 instead of 37177)
common_dates = pd.Series(common_idx.date)
complete_days = common_dates[common_dates.map(common_dates.value_counts()) == 24].unique()
common_idx = common_idx[pd.Series(common_idx.date).isin(complete_days).values]

# align data & reshape
p_real = ger_merged.loc[common_idx, 'day_ahead_price_eur_mwh'].values.reshape(-1, 24)
p_bench = ger_point_benchmark.loc[common_idx, 'forecast_naive_bench_eur_mwh'].values.reshape(-1, 24)

# run DM-test and compare 
for col in ger_forecast_cols: 
    p_lear = ger_full.loc[common_idx, col].values.reshape(-1, 24)
    p_value = DM(p_real=p_real, p_pred_1=p_bench, p_pred_2=p_lear, norm=1, version='multivariate')
    print(f'{col}: p-value = {p_value:.10f}')


# Spain
# realign forecast data to handle differences in data length from dropping NA
common_idx = es_full.index.intersection(es_point_benchmark.index)
print(len(common_idx) % 24 == 0) # conditinoo not met, so I have to remove any incomplete days

common_dates = pd.Series(common_idx.date)
complete_days = common_dates[common_dates.map(common_dates.value_counts()) == 24].unique()
common_idx = common_idx[pd.Series(common_idx.date).isin(complete_days).values]

# align data & reshape
p_real = es_merged.loc[common_idx, 'day_ahead_price_eur_mwh'].values.reshape(-1, 24)
p_bench = es_point_benchmark.loc[common_idx, 'forecast_naive_bench_eur_mwh'].values.reshape(-1, 24)

# run DM-test and compare 
for col in es_forecast_cols: 
    p_lear = es_full.loc[common_idx, col].values.reshape(-1, 24)
    p_value = DM(p_real=p_real, p_pred_1=p_bench, p_pred_2=p_lear, norm=1, version='multivariate')
    print(f'{col}: p-value = {p_value:.100f}')
