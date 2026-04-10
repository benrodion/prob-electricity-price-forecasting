import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
# quick and dirty plots of the distribution of the LEAR residuals
# to find out WHY THE QRA FORECASTS ARE SO BAD

### Germany ### 
file_path=Path(__file__).parents[1] / 'data/residuals/ger_lear_residuals.csv'
ger_res = pd.read_csv(file_path, parse_dates=True, index_col=0)

col_names = ger_res.columns


for col in col_names:
    sns.set_style('whitegrid')
    fig, ax = plt.subplots()
    sns.kdeplot(np.array(ger_res[col]), bw_adjust=2.0, ax=ax)
    ax.set_xlim(-45, 45)
    fig.savefig(f'results/figures/ger_{col}_residual_distr')
    plt.close(fig)
    

### Spain ###
file_path=Path(__file__).parents[1] / 'data/residuals/es_lear_residuals.csv'
es_res = pd.read_csv(file_path, parse_dates=True, index_col=0)

col_names = es_res.columns


for col in col_names:
    sns.set_style('whitegrid')
    fig, ax = plt.subplots()
    sns.kdeplot(np.array(ger_res[col]), bw_adjust=2.0, ax=ax)
    ax.set_xlim(-45, 45)
    fig.savefig(f'results/figures/residuals/es_{col}_residual_distr')
    plt.close(fig)
    