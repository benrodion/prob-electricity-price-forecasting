import numpy as np
from remodels.qra import QRA
import pandas as pd
from pathlib import Path

### QRA for Germany ###
file_path = Path(__file__).parents[1]/'processed/ger_merged.csv'
ger_data_original = pd.read_csv(file_path, index_col=0, parse_dates=True)
file_path = Path(__file__).parents[1]/'forecasts/ger_point_pred_clean.csv' # data without advanced asinh-inverse
ger_data_lear = pd.read_csv(file_path, index_col=0, parse_dates=True)

# merge orignal price data and forecasts for consistency
ger_merged = ger_data_lear.join(ger_data_original[['day_ahead_price_eur_mwh']], how='inner')

#train-test split 
X_cols = ger_merged.columns[0:4]
Y_col = ger_merged.columns[-1]

train_ger = ger_merged.loc['2020-01-01':'2020-04-01'] # adjusted training window for 91 day cal. period
X_train_ger = train_ger[X_cols].to_numpy()
Y_train_ger = train_ger[Y_col].to_numpy()
test_ger = ger_merged.loc['2020-04-02': ] # adjusted test window
X_test_ger = test_ger[X_cols].to_numpy()


# run Qra
quantiles = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95]
quant_name = ['qra_pred_05', 'qra_pred_10', 'qra_pred_25', 'qra_pred_50', 'qra_pred_75', 'qra_pred_90', 'qra_pred_95']
qra_ger = {}

for q, n in zip(quantiles, quant_name):
    qra_ger[n] = QRA(quantile=q, fit_intercept=True).fit(X_train_ger, Y_train_ger).predict(X_test_ger)

qra_ger["y_true"] = ger_merged.loc['2020-04-02': ,'day_ahead_price_eur_mwh']

qra_ger = pd.DataFrame(qra_ger)
qra_ger.to_csv('data/qra/ger_qra_91.csv')


## oh no, this seems to have been wrong...
# I need to do it with the QR_Tester if I wnat to use the Christoffersen test later...
if __name__ == '__main__': # without this, the QR_tester cannot run
    from remodels.qra.tester import QR_Tester
    qra_model = QRA(fit_intercept=True)
    X = ger_merged[X_cols].to_numpy()
    y = ger_merged[Y_col].to_numpy()

    ger_results = QR_Tester(
        calibration_window=91*24, # 90 days window is an experiment. Original is 182
        prediction_window=24,
        qr_model=qra_model,
        max_workers=10,
    ).fit_predict(X, y)

    # apparently it HAS to be pickled for the Christoffersen test to work 
    ger_results.to_pickle('data/qra/ger_qra_91.pkl')
    ger_results = pd.DataFrame(ger_results.Y_pred)


### QRA for Spain ###
file_path = Path(__file__).parents[1]/'processed/es_merged.csv'
es_data_original = pd.read_csv(file_path, index_col=0, parse_dates=True)
file_path = Path(__file__).parents[1]/'forecasts/es_point_pred_clean.csv' # data without advanced asinh-inverse
es_data_lear = pd.read_csv(file_path, index_col=0, parse_dates=True)

# merge orignal price data and forecasts for consistency
es_merged = es_data_lear.join(es_data_original[['day_ahead_price_eur_mwh']], how='inner')

#train-test split 
X_cols = es_merged.columns[0:4]
Y_col = es_merged.columns[-1]

train_es = es_merged.loc['2020-01-01':'2020-04-01'] # adjusted training window for 91 day cal. period
X_train_es = train_es[X_cols].to_numpy()
Y_train_es = train_es[Y_col].to_numpy()
test_es= es_merged.loc['2020-04-02': ] # adjusted test window
X_test_es = test_es[X_cols].to_numpy()


# run Qra
quantiles = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95]
quant_name = ['qra_pred_05', 'qra_pred_10', 'qra_pred_25', 'qra_pred_50', 'qra_pred_75', 'qra_pred_90', 'qra_pred_95']
qra_es = {}

for q, n in zip(quantiles, quant_name):
    qra_es[n] = QRA(quantile=q, fit_intercept=True).fit(X_train_es, Y_train_es).predict(X_test_es)

qra_es["y_true"] = es_merged.loc['2020-04-02': ,'day_ahead_price_eur_mwh']
qra_es = pd.DataFrame(qra_es)
qra_es.to_csv('data/qra/es_qra_91.csv')


# and now the proper version from above...
if __name__ == '__main__': # without this, the QR_tester cannot run
    from remodels.qra.tester import QR_Tester
    qra_model = QRA(fit_intercept=True)
    X = es_merged[X_cols].to_numpy()
    y = es_merged[Y_col].to_numpy()

    es_results = QR_Tester(
        calibration_window=91*24, # 90 days window is an experiment. Original is 182
        prediction_window=24,
        qr_model=qra_model,
        max_workers=10,
    ).fit_predict(X, y)

    # apparently it HAS to be pickled for the Christoffersen test to work 
    es_results.to_pickle('data/qra/es_qra_91.pkl')
    es_results = pd.DataFrame(es_results.Y_pred)

