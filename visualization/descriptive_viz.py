# descriptive visualization of the cleaned data
from helpers.visualization import plot_energy_timeseries
from pathlib import Path
import pandas as pd

##### Descriptive time-series graphs like in Marcjasz et al. 2023 ####
file_path=Path(__file__).parents[1] / 'data/processed/ger_merged_2.csv'
save_path=Path(__file__).parents[1] / 'results/figures/ger_descr_plot.png'
data_ger = pd.read_csv(file_path, index_col=0 )

# make plot for Germany
ger_descr_plot = plot_energy_timeseries(data_ger, title='Time Series Data Germany', save_path=save_path)

# and for Spain 
file_path=Path(__file__).parents[1] / 'data/processed/es_merged_2.csv'
save_path=Path(__file__).parents[1] / 'results/figures/es_descr_plot.png'
data_es = pd.read_csv(file_path, index_col=0)

# make plot for Germany
es_descr_plot = plot_energy_timeseries(data_es, title='Time Series Data Spain', save_path=save_path)


#####Table of descriptive statistics in/out of sample
from helpers.descriptives import descr_tables

lag_cols = ['gas_d_2', 'oil_d_2', 'co2_d_2']
data_ger = data_ger.drop(columns=lag_cols, errors='ignore')
data_es = data_es.drop(columns=lag_cols, errors='ignore')

# Germany
ger_in_sample_descr = descr_tables(data_ger,period_start='2018-01-01', period_end='2021-07-02')
ger_out_of_sample_descr = descr_tables(data_ger,period_start='2021-07-03')

combined = pd.concat([ger_in_sample_descr, ger_out_of_sample_descr], 
                     keys=['In-sample (01.01.2018–02.07.2021)', 
                           'Out-of-sample (03.07.2021-30.09.2025)'])
print(combined.index.levels[1].tolist())

combined.index = combined.index.set_levels([
    combined.index.levels[0],
    ['Day-Ahead Price (EUR/MWh)', 'Load Forecast (MW)', 'Solar Forecast (MW)',  'Wind Aggregated (MW)', 
     'Price D-1 H (EUR/MWh)','Price D-2 H (EUR/MWh)','Price D-7 H (EUR/MWh)','Price D-1 24H (EUR/MWh)', 'Price D-1 Min (EUR/MWh)',
     'Price D-1 Max (EUR/MWh)','CO2 Allowances (EUR/t)', 'Brent Oil (EUR/bbl.)',
     'TTF Gas (EUR/MWh)'
    ]
])
print(combined.to_latex(float_format="%.1f"))


# Germany
es_in_sample_descr = descr_tables(data_es,period_start='2018-01-01', period_end='2021-07-02')
es_out_of_sample_descr = descr_tables(data_es,period_start='2021-07-03')


combined = pd.concat([es_in_sample_descr, es_out_of_sample_descr], 
                     keys=['In-sample (01.01.2018–02.07.2021)', 
                           'Out-of-sample (03.07.2021-30.09.2025)'])
print(combined.index.levels[1].tolist())

combined.index = combined.index.set_levels([
    combined.index.levels[0],
    ['Day-Ahead Price (EUR/MWh)', 'Load Forecast (MW)', 'Solar Forecast (MW)',  'Wind Aggregated (MW)', 
     'Price D-1 H (EUR/MWh)','Price D-2 H (EUR/MWh)','Price D-7 H (EUR/MWh)','Price D-1 24H (EUR/MWh)', 'Price D-1 Min (EUR/MWh)',
     'Price D-1 Max (EUR/MWh)','CO2 Allowances (EUR/t)', 'Brent Oil (EUR/bbl.)',
     'TTF Gas (EUR/MWh)'
    ]
])
print(combined.to_latex(float_format="%.1f"))
