import numpy as np
import pandas as pd
from pathlib import Path
from remodels.qra.tester import QR_TestResults

data_path = Path(__file__).parents[1] / 'qra'
out_path = Path(__file__).parents[1] / 'qra'

quant_cols = ['qra_pred_05', 'qra_pred_10', 'qra_pred_25', 'qra_pred_50',
              'qra_pred_75', 'qra_pred_90', 'qra_pred_95']

variants = {
    'ger': ['qra', 'qra_91', 'qra_asinh', 'qra_31'],
    'es':  ['qra', 'qra_91', 'qra_asinh', 'qra_31'],
}

data = {}

# crucial postprocessing: sort quantiles to impose monotonicity/ eliminate the issue of quantile crossing
# how could i even forget this?
# it should dramatically improve the quality of my findings
for market, variant_list in variants.items():
    data[market] =  {}
    for variant in variant_list:
        csv = pd.read_csv(data_path / f'{market}_{variant}.csv',index_col=0, parse_dates=True)
        pkl = QR_TestResults.read_pickle(data_path / f'{market}_{variant}.pkl')

        csv[quant_cols] = np.sort(csv[quant_cols].values, axis= 1)
        Y_sorted = np.sort(pkl.Y_pred,axis=1)
        pkl_sorted = QR_TestResults(Y_sorted, pkl.y_test, pkl.prediction_window) # i need it to be this object categorz to run the tests from remodels

        data[market][variant] = { 'csv': csv, 'pkl': pkl_sorted}

        csv.to_csv(out_path / f'{market}_{variant}_sorted.csv')
        pkl_sorted.to_pickle(out_path / f'{market}_{variant}_sorted.pkl')
