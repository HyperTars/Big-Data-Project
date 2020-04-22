import pandas as pd
import numpy as np
import os


def removeExist(path):
    if(os.path.exists(path)):
        os.remove(path)
        
removeExist('USD_AUD.csv')
removeExist('USD_EUR.csv')
removeExist('USD_GBP.csv')

currencies = ['AUD_USD.csv', 'EUR_USD.csv', 'GBP_USD.csv']

for cur in currencies:
    newName = cur[4:7] + '_' + cur[:3] + '.csv'
    df = pd.read_csv(cur)
    columns = [df.columns.values[1], df.columns.values[3], df.columns.values[4], df.columns.values[5]]
    for col in columns:
        df[col] = df[col].apply(lambda x: 1 / x)
    df.to_csv(newName, index=True)