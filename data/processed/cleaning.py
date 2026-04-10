import pandas as pd
from helpers.timetransitions import fix_dst_transitions
from helpers.price_lags import add_lagged_price_features
from pathlib import Path

#### Germany  ###

file_path=Path(__file__).parents[1] / 'raw/entsoe_germany_2015_2025.csv'
data_ger = pd.read_csv(file_path)
data_ger.rename(columns={'Forecasted Load_mw': 'load_forecast_mw', 'Solar_mw': 'solar_forecast_mw', 
                         'Wind Offshore_mw': 'offshore_forecast_mw', 'Wind Onshore_mw': 'onshore_forecast_mw' }, inplace=True)


data_ger['wind_aggr_mw'] = data_ger['offshore_forecast_mw'].add(data_ger['onshore_forecast_mw'], 
                                                                fill_value=0)

# if there are NAs in both wind cols, set value in aggregated col to NA as well
data_ger.loc[data_ger['offshore_forecast_mw'].isna() & data_ger['onshore_forecast_mw'].isna(), 'wind_aggr_mw'] = pd.NA

data_ger = data_ger.drop(['offshore_forecast_mw', 'onshore_forecast_mw'], axis=1)

#  datetime format index col so that so I can work with it as time series
data_ger['Unnamed: 0'] = pd.to_datetime(data_ger['Unnamed: 0'], utc=True)
data_ger = data_ger.set_index('Unnamed: 0')
data_ger.index.name = 'datetime'  #

# remedy issues from switches to/from daylight saving time
data_ger = fix_dst_transitions(data_ger) # actually seems to be obsolete, but it doesn't hurt


data_ger_lagged = add_lagged_price_features(data_ger)
data_ger_lagged.to_csv('data/processed/data_ger_lagged.csv')


### Spain  ### 
file_path=Path(__file__).parents[1] / 'raw/entsoe_spain_2015_2025.csv'
data_es = pd.read_csv(file_path)
data_es.rename(columns={'Forecasted Load_mw': 'load_forecast_mw', 
                        'Solar_mw': 'solar_forecast_mw', 'Wind Onshore_mw': 'wind_aggr_mw'}, inplace=True)

#  datetime format index col so that so I can work with it as time series
data_es['Unnamed: 0'] = pd.to_datetime(data_es['Unnamed: 0'], utc=True)
data_es = data_es.set_index('Unnamed: 0')
data_es.index.name = 'datetime'  #

# remedy issues from switches to/from daylight saving time
data_es = fix_dst_transitions(data_es) # actually seems to be obsolete, but it doesn't hurt


data_es_lagged = add_lagged_price_features(df=data_es)
data_es_lagged = data_es_lagged.loc['2015-01-01':]
data_es_lagged.to_csv('data/processed/data_es_lagged.csv')



####### Commodity data  ####### 
from helpers.stock_data import clean_stock_data, impute_weekends, clean_ttf_data

paths = [Path(__file__).parents[1] / 'raw/CO_2_allowances_2015_2025.csv', Path(__file__).parents[1] / 'raw/oil_2015_2025.csv']
path_ttf = Path(__file__).parents[1] / 'raw/ttf_gas_2017_2025.csv' # separate solution needed because data is from different source
name_ttf = 'data/processed/gas_clean.csv'
names = ['data/processed/co2_allowances_clean.csv', 'data/processed/oil_clean.csv']

for file_path, name in zip(paths, names):
    data = pd.read_csv(file_path, sep=';')
    data = clean_stock_data(data)
    data = impute_weekends(data)
    data.to_csv(name)

# separate ttf clean-up
data = pd.read_csv(path_ttf)
data = clean_ttf_data(data)
data = impute_weekends(data)
data.to_csv(name_ttf)

##### merge commodity data with the data for Germany/Spain
co2 = pd.read_csv('data/processed/co2_allowances_clean.csv', index_col= 0, parse_dates=True)
oil = pd.read_csv('data/processed/oil_clean.csv', index_col= 0, parse_dates=True)
gas = pd.read_csv('data/processed/gas_clean.csv', index_col= 0, parse_dates=True)
ger = pd.read_csv('data/processed/data_ger_lagged.csv', index_col= 0, parse_dates=True)
es = pd.read_csv('data/processed/data_es_lagged.csv', index_col= 0, parse_dates=True)

#perform merge
co2['date'] = pd.to_datetime(co2.index).normalize()
oil['date'] = pd.to_datetime(oil.index).normalize()
gas['date'] = pd.to_datetime(gas.index).normalize()
# ensure column identifiability
co2 = co2.rename(columns=lambda c: f'co2_{c}' if c != 'date' else c)
oil = oil.rename(columns=lambda c: f'oil_{c}' if c != 'date' else c)
gas = gas.rename(columns=lambda c: f'gas_{c}' if c != 'date' else c)

def merge_commodities(entsoe_df):
    entsoe_df = entsoe_df.copy()
    entsoe_df.index = pd.to_datetime(entsoe_df.index).tz_localize(None) # remove UTC
    original_index =entsoe_df.index
    entsoe_df['date'] = entsoe_df.index.normalize()

    for commodity_df in [co2, oil, gas]:
        entsoe_df = entsoe_df.merge( commodity_df, on='date', how='left')

    entsoe_df = entsoe_df.drop(columns=['date','co2_first_course_eur', 'oil_first_course_eur', 'gas_first_course_eur'])
    entsoe_df.index = original_index
    return entsoe_df

es_merged = merge_commodities(es)
es_merged_2 = es_merged # separate version to keep my descriptive plot script viable
ger_merged = merge_commodities(ger)
ger_merged_2 = ger_merged  # separate version to keep my descriptive plot script viable


# include commoditz prices for d-2
ger_merged['gas_d_2'] = ger_merged['gas_last_course_eur'].shift(freq=pd.Timedelta('2 days'))
ger_merged['oil_d_2'] = ger_merged['oil_last_course_eur'].shift(freq=pd.Timedelta('2 days'))
ger_merged['co2_d_2'] = ger_merged['co2_last_course_eur'].shift(freq=pd.Timedelta('2 days'))
es_merged['gas_d_2'] = es_merged['gas_last_course_eur'].shift(freq=pd.Timedelta('2 days'))
es_merged['oil_d_2'] = es_merged['oil_last_course_eur'].shift(freq=pd.Timedelta('2 days'))
es_merged['co2_d_2'] = es_merged['co2_last_course_eur'].shift(freq=pd.Timedelta('2 days'))

#and remove all rows with missing values + unneccessary columns 
# for Germany: around 1100 due to missing load forecasts, should be verschmerzbar
# for Spain: around 150 due to missing RES forecasts, also verschmerzbar
es_merged = es_merged.dropna()
es_merged_2 = es_merged_2.dropna()
es_merged = es_merged.drop(columns=['co2_last_course_eur', 'oil_last_course_eur', 'gas_last_course_eur'])
es_merged = es_merged.loc['01-01-2018':]
es_merged_2 = es_merged_2.loc['01-01-2018':]
ger_merged = ger_merged.dropna()
ger_merged_2 = ger_merged_2.dropna()
ger_merged = ger_merged.drop(columns=['co2_last_course_eur', 'oil_last_course_eur', 'gas_last_course_eur'])
ger_merged = ger_merged.loc['01-01-2018':]
ger_merged_2 = ger_merged_2.loc['01-01-2018':]

# add weekday dummies
names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday']
ger_dummies = pd.get_dummies(pd.Series(ger_merged.index.get_level_values(0).day_name(), index=ger_merged.index)).reindex(columns=names, fill_value=0)
ger_merged = ger_merged.join(ger_dummies)

es_dummies = pd.get_dummies(pd.Series(es_merged.index.get_level_values(0).day_name(), index=es_merged.index)).reindex(columns=names, fill_value=0)
es_merged = es_merged.join(es_dummies)


ger_merged.to_csv('data/processed/ger_merged.csv')
es_merged.to_csv('data/processed/es_merged.csv')
es_merged_2.to_csv('data/processed/es_merged_2.csv')
ger_merged_2.to_csv('data/processed/ger_merged_2.csv')

