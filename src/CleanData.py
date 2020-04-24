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
    print('### Trans Currencies to USD Base Start ###')
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
    print('### Trans Currencies to USD Base Completed ###')


########################################
# Trans Yahoo Data Format to NASDAQ Data Format
def TransYahooToNASDAQ():
    print('### Trans Yahoo Data to NASDAQ Data Format Start ###')
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
        if 'Close' in df.columns.values:
            df_close = df.Close
            df = df.drop('Close', axis=1, errors='ignore')
            df.insert(1, 'Close/Last', df_close)
        # reorder in time
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True, ascending=False)
        # save
        df.to_csv(path, index=False, header=True)
    print('### Trans Yahoo Data to NASDAQ Data Format Completed ###')


########################################
# Clean Data From NASDAQ (Excepet All Stock Data)
def CleanDataFromNASDAQ():
    print('### Clean Data Sets From NASDAQ Start ###')
    file_idx = 'NasdaqSource.txt'
    file_path = {}
    for line in open(file_idx):
        path = line.strip('\n')
        name = path.split("/")[-1][:-4]
        file_path[name] = path

    for path in file_path.values():
        df = pd.read_csv(path)
        # format column name, delete redundant whitespace in column names
        df.columns = [x.strip() for x in df.columns.values if x.strip() != '']
        # remove redundant column 'Volume'
        df = df.drop('Volume', axis=1, errors='ignore')
        # save
        df.to_csv(path, index=False, header=True)
    print('### Clean Data Sets From NASDAQ Completed ###')


########################################
# Clean Data From Other Source
def CleanOtherSources():
    print('### Clean Data Sets From Other Sources Start ###')
    file_CrudeOil_WTI_MacroTrends = '../data/market/Commodities/Energies/CrudeOil_WTI_macrotrends.csv'
    file_Finance_Sector_Related_Policy_Responses = '../data/general/FinanceSectorRelatedPolicyResponses.xlsx'
    file_Industrial_Production_Index = '../data/general/IndustrialProductionIndex.csv'
    file_Initial_Jobless_Claims = '../data/employment/InitialJoblessClaims.csv'
    file_Unemployment_Rate = '../data/employment/UnemploymentRate.csv'

    # Finance Sector Related Policy Responses
    FSRPR = pd.read_excel(file_Finance_Sector_Related_Policy_Responses, sheet_name='Raw data')
    # drop redundant columns
    FSRPR = FSRPR.drop('Iso 3 Code', axis=1, errors='ignore')
    FSRPR = FSRPR.drop('Entry date', axis=1, errors='ignore')
    # reorder
    FSRPR_Country = FSRPR.Country
    FSRPR = FSRPR.drop('Country', axis=1, errors='ignore')
    FSRPR.insert(0, 'Country', FSRPR_Country)
    FSRPR.to_csv(file_Finance_Sector_Related_Policy_Responses[:-4] + 'csv', index=False, header=True)

    # CrudeOil WTI MacroTrends
    CWM = pd.read_csv(file_CrudeOil_WTI_MacroTrends)
    # reorder in time
    CWM['Date'] = pd.to_datetime(CWM['Date'])
    CWM.sort_values('Date', inplace=True, ascending=False)
    # format column name, delete redundant whitespace in column names
    CWM.columns = [x.strip() for x in CWM.columns.values if x.strip() != '']
    # delete invalid future data
    CWM.dropna(subset=['value'], inplace=True)
    CWM.to_csv(file_CrudeOil_WTI_MacroTrends, index=False, header=True)

    # Others with date (reorder date)
    file_path = []
    file_path.append(file_Industrial_Production_Index)
    file_path.append(file_Initial_Jobless_Claims)
    file_path.append(file_Unemployment_Rate)
    for path in file_path:
        df = pd.read_csv(path)
        # reorder in time
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True, ascending=False)
        # save
        df.to_csv(path, index=False, header=True)
    print('### Clean Data Sets From Other Sources Completed ###')


########################################
# this function modify Covid-19 world data from JHU CSSE
def CleanCovid19Data():
    print('### Clean Covid-19 Data Sets Start ###')
    covidDataPath = '../data/covid-19/time_series_covid19_confirmed_global.csv'
    covidDataNewPath = '../data/covid-19/time_series_covid19_confirmed_global_modified.csv'
    df = pd.read_csv(covidDataPath)
    # remove useless columns
    df = df.drop(['Province/State', 'Lat', 'Long'], 1, errors='ignore')
    if 'Country/Region' in df.columns.values:
        df.rename(columns={'Country/Region': 'Date'}, inplace=True)
        # transform date format to 'yyyy-mm-dd'
        # df.rename(lambda x: modifyDate(x), axis = 'columns', inplace = True)
        # combine province/state data to the whole country
        group_df = df[1:].groupby(df['Date'])
        sum_df = group_df.sum()
        # calculate world data
        sum_df.loc["World"] = sum_df.apply(lambda x: x.sum())
        # transposition, probably not necessary
        result = pd.DataFrame(sum_df.values.T, index=sum_df.columns, columns=sum_df.index)
        # transform date format to 'yyyy-mm-dd'
        result.index = pd.to_datetime(result.index)
        result.index.name = 'Date'
        # output
    result.to_csv(covidDataNewPath, index=True, header=True)
    print('### Clean Covid-19 Data Sets Completed ###')


########################################
# this function transform every date to format "yyyy-mm-dd"
def FormatDate():
    '''
    this function is quite dump, it walk through the whole data directory, and try to modify every csv file
    but it some how make sense since most of our file need to be transformed
    '''
    print('### Format Date Column Start ###')
    rootPath = "../data"
    for root, dirs, files in os.walk(rootPath):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith('.csv'):
                df = pd.read_csv(path)
                if 'DATE' in df.columns:
                    df.rename(columns={'DATE': 'Date'}, inplace=True)
                if 'date' in df.columns:
                    df.rename(columns={'date': 'Date'}, inplace=True)
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                df.to_csv(path, index=False, header=True)
    print('### Format Date Column Completed ###')


FormatDate()
TransToUSDBase()
TransYahooToNASDAQ()
CleanDataFromNASDAQ()
CleanOtherSources()
CleanCovid19Data()
