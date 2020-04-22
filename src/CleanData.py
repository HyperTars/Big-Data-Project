import pandas as pd
import numpy as np
import os


def removeExist(path):
    if(os.path.exists(path)):
        os.remove(path)


########################################
# Trans currencies to USD base
def TransToUSDBase():
    currenciesPath = '../data/market/Currencies/'
    currencies = ['AUD_USD.csv', 'EUR_USD.csv', 'GBP_USD.csv']
    for currency in currencies:
        curPath = currenciesPath + currency
        newPath = currenciesPath + currency[4:7] + '_' + currency[:3] + '.csv'
        df = pd.read_csv(curPath)
        columns = [df.columns.values[1], df.columns.values[3], df.columns.values[4], df.columns.values[5]]
        for col in columns:
            df[col] = df[col].apply(lambda x: 1 / x)
        removeExist(newPath)
        df.to_csv(newPath, index=False, header=True)


########################################
# Clean Data From NASDAQ (Excepet All Stock Data)
def CleanDataFromNASDAQ():
    file_idx = 'NasdaqSource.txt'
    file_path = {}
    for line in open(file_idx):
        path = line.strip('\n')
        name = path.split("/")[-1][:-4]
        file_path[name] = path

    for name in file_path:
        print(name + ': ' + file_path[name])

    for path in file_path.values():
        df = pd.read_csv(path)
        # format column name
        df.columns = [x.strip() for x in df.columns.values if x.strip() != '']
        # remove redundant column 'Volume'
        df = df.drop('Volume', axis=1, errors='ignore')
        # save
        df.to_csv(path, index=False, header=True)
        print(path)
        print(df.columns)


########################################
# Clean Data From Other Source
def CleanOtherSources():
    CrudeOil_WTI_MacroTrends = '../data/market/Commodities/Energies/CrudeOil_WTI_macrotrends.csv'
    Finance_Sector_Related_Policy_Responses = '../data/general/FinanceSectorRelatedPolicyResponses.xlsx'
    Industrial_Production_Index = '../data/general/IndustrialProductionIndex.csv'
    Initial_Jobless_Claims = '../data/employment/InitialJoblessClaims.csv'
    Unemployment_Rate = '../data/employment/UnemploymentRate.csv'


TransToUSDBase()
CleanDataFromNASDAQ()
# CleanOtherSources()
