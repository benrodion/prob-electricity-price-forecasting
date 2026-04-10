# This script adapts the LEAR model from Lago et al.'s (2021) epftoolbox to work my pre-processed data.
# The original code can be found here: https://github.com/jeslago/epftoolbox/blob/master/epftoolbox/models/_lear.py
from sklearn.utils._testing import ignore_warnings
from sklearn.linear_model import LassoLarsIC, LassoCV, Lasso, LinearRegression
from sklearn.exceptions import ConvergenceWarning
import numpy as np
import pandas as pd


@ignore_warnings(category=ConvergenceWarning)
def fit_predict_lear(df_train, df_test_day, feature_cols, target_col):
    """
    Fit 24 hourly LASSO models on df_train and predict one day ahead. Each hourly model is trained only on rows at hour h.
    Returns predictions and the best lambda for each hour.
    """
    Y_pred = np.zeros(24)
    lambdas = np.zeros(24)

    for h in range(24):
        train_h = df_train[df_train.index.hour == h]
        X_train = train_h[feature_cols].values
        Y_train = train_h[target_col].values

        X_test = df_test_day[df_test_day.index.hour == h][feature_cols].values

        try:
            lmbd_model = LassoLarsIC(criterion='aic', max_iter=2500)
            lmbd = lmbd_model.fit(X_train, Y_train).alpha_
        except ValueError:
            # LARS path solver fails on near-collinear features; fall back to CV
            lmbd_model = LassoCV(cv=5, max_iter=2500)
            lmbd = lmbd_model.fit(X_train, Y_train).alpha_
        lambdas[h] = lmbd

        # this is needed to address a sklearn-warning:
        # if lambda == 0, the forecast is done through linear regression to ensure convergence
        if lmbd== 0:
            model = LinearRegression()
        else:
            model = Lasso(max_iter=2500, alpha=lmbd)
        Y_pred[h] = model.fit(X_train, Y_train).predict(X_test)[0]

    return Y_pred, lambdas


# Rewritten code from Lago et al. 2021 with the help of Claude Sonnet 4.6
# Prompt: Please check my code and help me figure out why the model's forecast fails
def rolling_lear(df, feature_cols, target_col, calibration_window, test_days):
    """
    Rolling-window LEAR forecast. recalibrate daily and predict one day ahead.
    Returns dfs with forecasts and best lambdas.
    """
    cols = [f'h{h:02d}' for h in range(24)]
    forecasts = pd.DataFrame(index=test_days, columns=cols)
    lambdas = pd.DataFrame(index=test_days, columns=cols)

    for date in test_days:
        train_end = date-pd.Timedelta(hours=1)
        train_start = date - pd.Timedelta(days=calibration_window)

        df_train = df.loc[train_start:train_end]
        df_test_day = df.loc[date: date+pd.Timedelta(hours=23)]

        # turns out to be needed to prevent forecast failures:
        # leave NA for incomplete days
        if len(df_test_day) < 24:
            continue  

        forecasts.loc[date], lambdas.loc[date] = fit_predict_lear(df_train, df_test_day, feature_cols, target_col)

    return forecasts, lambdas
