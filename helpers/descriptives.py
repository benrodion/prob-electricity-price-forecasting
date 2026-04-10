# make nice tables of descriptive stats 

def descr_tables(df, period_start, period_end = None, quantiles=[0.25, 0.75],
                 quantile_names=['Q25', 'Q75']):
    """
    For creating tables of descriptive stats (in- and out of sample)
    """
    df = df.loc[period_start:period_end]

    df_descr = df.agg(
        ['mean', 'std', 'min', 'median', 'max']
).T
    
    df_descr.columns= ['Mean', 'Std', ' Min.', 'Median', 'Max']
    df_descr.index.name = ('Variables')

    for quantile, name in zip(quantiles, quantile_names):
        df_descr[name] = df.quantile(q=quantile)

    # proper col order 
    df_descr = df_descr.iloc[:, [0, 1, 2, 5, 3, 6, 4]]

    return df_descr