from pathlib import Path
import pandas as pd
from remodels.qra.tester import QR_TestResults
from helpers.qra_tests import subset_year, christoffersen_per_hour

# The visual inspection of the QRA width yields something strange: negative values 
# this means my QRA results have a problem: the prediction intervals seem to to cross(?), which should be impossible 
# here I want to make a detailed comparative analysis of all QRA variantsI tried to figure which one performs best and where the errors occur 
# I also wnat to see how bad the crossing is
# Nevermind: I fixed the problem through postprocessing. But the error analysis is still valuable for my thesis : )

data_path = Path(__file__).parents[1] / 'data' / 'qra'
results_path = Path(__file__).parents[1] / 'results' / 'tables'

alphas = [5, 50, 95]
significance = 0.05
markets = ['ger', 'es']
qra_variants= ['qra_sorted','qra_91_sorted', 'qra_31_sorted']

data = {m: {} for m in markets}
for market in markets:
    for variant in qra_variants:
        pkl = QR_TestResults.read_pickle(data_path / f'{market}_{variant}.pkl')
        index = pd.read_csv(data_path / f'{market}_{variant}.csv', index_col=0, parse_dates=True).index
        data[market][variant] = (pkl, index)

all_years = sorted({y for m in markets for _, (_, idx) in data[m].items() for y in idx.year.unique()})


###Christoffersen Test 
for alpha in alphas:
    for market in markets:
        df = pd.DataFrame(index=all_years, columns=qra_variants, dtype=object)
        for variant in qra_variants:
            results, index = data[market][variant]
            for year in all_years:
                sub =subset_year(results, index, year)
                if sub is None or len(sub.y_test) < 24:
                    continue
                n_pass = christoffersen_per_hour(sub , alpha, significance).sum()
                df.at[year, variant] = f'{n_pass}/24'
        print(f'\nChristoffersen  alpha={alpha}% {market.upper()}')
        print( df.to_string())
        df.to_csv(results_path / f'christoffersen_alpha{alpha}_{market}.csv')


### Average empirical Coverage
for alpha in alphas:
    for market in markets:
        df = pd.DataFrame(index=all_years, columns=qra_variants, dtype=float)
        for variant in qra_variants:
            results, index = data[market][variant]
            for year in all_years:
                sub =subset_year(results, index, year)
                if sub is None:
                    continue
                df.at[year, variant] = round(sub.aec(alpha) * 100, 2)
        print(f'\nAEC  alpha={alpha}%  {market.upper()} (expected: {alpha}%)')
        print( df.to_string())
        df.to_csv(results_path / f'aec_alpha{alpha}_{market}.csv')


### Aggregate Pinball Score
for market in markets:
    df = pd.DataFrame(index=all_years, columns=qra_variants, dtype=float)
    for variant in qra_variants:
        results, index = data[market][variant]
        for year in all_years:
            sub =subset_year(results, index, year)
            if sub is None:
                continue
            df.at[year, variant] = round(sub.aps(), 4)
    print(f'\nAPS {market.upper()}')
    print( df.to_string())
    df.to_csv(results_path / f'aps_{market}.csv')



### Quantile levels and actual price by year (
for market in markets:
    df = pd.read_csv(data_path / f'{market}_qra_sorted.csv', index_col=0, parse_dates=True)
    df['year'] = df.index.year
    df['range_q5_q95'] = df['qra_pred_95'] - df['qra_pred_05']
    summary = df.groupby('year').agg(
        Q5=('qra_pred_05', 'median'),
        Q50=('qra_pred_50', 'median'),
        Q95=('qra_pred_95', 'median'),
        range_Q5_Q95=('range_q5_q95', 'median'),
        actual_meadian=('y_true', 'median'),
    ).round(2)
    print(f'\nQuantile levels & actual price by year  {market}  (qra_sorted, median of hourly values)')
    print(summary.to_string())


# check how bad is the crossing
# obsolete now. I fixed the problem by sortin the quantiles
#for market in markets:
#    for variant in qra_variants:
#        df = pd.read_csv(data_path / f'{market}_{variant}.csv', index_col=0, parse_dates=True)
#        print(f'\n Crossing {market} {variant}')
#        for year in all_years:
#            sub = df[df.index.year == year]
#            if sub.empty: continue
#            n = (sub['qra_pred_05'] > sub['qra_pred_95']).sum()
#            print(f'  {year}: {n/len(sub)*100:.1f}%')
