import pandas as pd
import numpy as np
import os
import xlrd

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
# Trans Yahoo Data Format to NASDAQ Data Format
def TransYahooToNASDAQ():
    path_index = '../data/market/Index/'
    file_path = []
    file_path.append(path_index + 'CBOE_VolatilityIndex.csv')
    file_path.append(path_index + 'DowJones_IndustrialAvg.csv')
    file_path.append(path_index + 'NASDAQ_100_Index.csv')
    file_path.append(path_index + 'Russell_2000.csv')
    for path in file_path:
        df = pd.read_csv(path)
        # remove redundant column 'Adj Close'
        df = df.drop('Adj Close', axis=1, errors='ignore')
        # rename Close to Close/Last and put to second place
        df_close = df.Close
        df = df.drop('Close', axis=1, errors='ignore')
        df.insert(1, 'Close/Last', df_close)
        # reorder in time
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True, ascending=False)
        # save
        df.to_csv(path, index=False, header=True)


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
        # format column name, delete redundant whitespace in column names
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
    file_CrudeOil_WTI_MacroTrends = '../data/market/Commodities/Energies/CrudeOil_WTI_macrotrends.csv'
    file_Finance_Sector_Related_Policy_Responses = '../data/general/FinanceSectorRelatedPolicyResponses.xlsx'
    file_Industrial_Production_Index = '../data/general/IndustrialProductionIndex.csv'
    file_Initial_Jobless_Claims = '../data/employment/InitialJoblessClaims.csv'
    file_Unemployment_Rate = '../data/employment/UnemploymentRate.csv'

    CWM = pd.read_csv(file_CrudeOil_WTI_MacroTrends)
    # reorder in time
    CWM['date'] = pd.to_datetime(CWM['date'])
    CWM.sort_values('date', inplace=True, ascending=False)
    CWM.to_csv(file_CrudeOil_WTI_MacroTrends, index=False, header=True)

    FSRPR = pd.read_excel(file_Finance_Sector_Related_Policy_Responses, sheet_name='Raw data')
    # drop redundant columns
    FSRPR = FSRPR.drop('Iso 3 Code', axis=1, errors='ignore')
    FSRPR = FSRPR.drop('Entry date', axis=1, errors='ignore')
    # reorder
    FSRPR_Country = FSRPR.Country
    FSRPR = FSRPR.drop('Country', axis=1, errors='ignore')
    FSRPR.insert(0, 'Country', FSRPR_Country)
    FSRPR.to_csv(file_Finance_Sector_Related_Policy_Responses[:-4] + 'csv', index=False, header=True)

    IPI = pd.read_csv(file_Industrial_Production_Index)
    # reorder in time
    IPI['DATE'] = pd.to_datetime(IPI['DATE'])
    IPI.sort_values('DATE', inplace=True, ascending=False)
    IPI.to_csv(file_Industrial_Production_Index, index=False, header=True)

    IJC = pd.read_csv(file_Initial_Jobless_Claims)
    IJC['DATE'] = pd.to_datetime(IJC['DATE'])
    IJC.sort_values('DATE', inplace=True, ascending=False)
    IJC.to_csv(file_Initial_Jobless_Claims, index=False, header=True)

    UR = pd.read_csv(file_Unemployment_Rate)
    # reorder in time
    UR['DATE'] = pd.to_datetime(UR['DATE'])
    UR.sort_values('DATE', inplace=True, ascending=False)
    UR.to_csv(file_Unemployment_Rate, index=False, header=True)

#TransToUSDBase()
#TransYahooToNASDAQ()
#CleanDataFromNASDAQ()
CleanOtherSources()
