import pandas as pd
from pathlib import Path
from helpers.standardization import MedianStandardizingScaler
from remodels.transformers.VSTransformers import ArcsinhScaler


##### Germany #####
file_path=Path(__file__).parents[0] / 'ger_merged.csv'
ger_merged = pd.read_csv(file_path, 
            index_col=0, parse_dates=True) 


# standardize and transform 
names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday']
median_standard_scaler = MedianStandardizingScaler(method='median')
arcsinh_scaler = ArcsinhScaler()
cols_to_transform = [c for c in ger_merged if c not in names]
for c in cols_to_transform:
    median_standard_scaler.fit(ger_merged[[c]])
    standardized = median_standard_scaler.transform(ger_merged[[c]])
    ger_merged[c] = arcsinh_scaler.fit_transform(standardized)

##### Spain #####
file_path=Path(__file__).parents[0] / 'es_merged.csv'
es_merged = pd.read_csv(file_path, index_col=0, parse_dates=True)

# standardize and transform 
for c in cols_to_transform:
    median_standard_scaler.fit(es_merged[[c]])
    standardized = median_standard_scaler.transform(es_merged[[c]])
    es_merged[c] = arcsinh_scaler.fit_transform(standardized)

ger_merged.to_csv('data/processed/ger_processed.csv')
es_merged.to_csv('data/processed/es_processed.csv')