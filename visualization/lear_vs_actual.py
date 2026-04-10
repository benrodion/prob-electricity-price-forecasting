from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

### Germany ###
actual_path = Path(__file__).parents[1] / 'data/processed/ger_merged.csv'
lear_path = Path(__file__).parents[1] / 'data/forecasts/ger_point_pred_clean.csv'
lear_data = pd.read_csv(lear_path, index_col=0, parse_dates=True)
actual_data = pd.read_csv(actual_path, index_col=0, parse_dates=True)
calibration_windows = ['6m', '12m', '18m', '24m']


forecast_start = lear_data.index[0]

for window in calibration_windows:
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(actual_data.index, actual_data['day_ahead_price_eur_mwh'], color='blue', linewidth =0.4, alpha=0.7, label='Actual')
    ax.plot(lear_data.index, lear_data[window], color='red' , linewidth=0.4, alpha=0.6, label='LEAR forecast')
    ax.axvline(forecast_start, color= 'black', linewidth=0.8, linestyle='--', label='Forecast period start')
    ax.set_ylim(-450, 1100) # this cuts some outliers out and I will have to mention it in the discussion
    ax.set_title(f'Germany: LEAR vs Actual – {window} calibration window')
    ax.set_ylabel('Price (€/MWh)')
    ax.set_xlabel('Date')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(f'results/figures/ger_lear_vs_actual_{window}.png', dpi=150)
    plt.close(fig)
figures_dir = Path(__file__).parents[1] / 'results/figures'

### Spain ###
actual_path = Path(__file__).parents[1] / 'data/processed/es_merged.csv'
lear_path = Path(__file__).parents[1] / 'data/forecasts/es_point_pred_clean.csv'
lear_data = pd.read_csv(lear_path, index_col=0, parse_dates=True)
actual_data = pd.read_csv(actual_path, index_col=0, parse_dates=True)
calibration_windows = ['6m', '12m', '18m', '24m']


forecast_start = lear_data.index[0]

for window in calibration_windows:
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(actual_data.index, actual_data['day_ahead_price_eur_mwh'], color='blue', linewidth =0.4, alpha=0.7, label='Actual')
    ax.plot(lear_data.index, lear_data[window], color='red' , linewidth=0.4, alpha=0.6, label='LEAR forecast')
    ax.axvline(forecast_start, color= 'black', linewidth=0.8, linestyle='--', label='Forecast period start')
    ax.set_ylim(-60, 800) # this cuts some outliers out and I will have to mention it in the discussion
    ax.set_title(f'Spain: LEAR vs Actual – {window} calibration window')
    ax.set_ylabel('Price (€/MWh)')
    ax.set_xlabel('Date')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(f'results/figures/es_lear_vs_actual_{window}.png', dpi=150)
    plt.close(fig)
figures_dir = Path(__file__).parents[1] / 'results/figures'
