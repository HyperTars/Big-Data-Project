import pandas as pd
import numpy as np
import platform as pf
import os
import xlrd
import matplotlib
import shutil
from matplotlib import pyplot as plt
from sklearn import preprocessing as pprs
from scipy import stats
from datetime import datetime
from datetime import datetime
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

pd.set_option('max_row', 1000)
pd.set_option('max_column', 10)

covidDP_confirmed = '../clean_data/covid-19/time_series_covid19_confirmed_global.csv'
covidDP_deaths = '../clean_data/covid-19/time_series_covid19_deaths_global.csv'
directories = ['Commodities/Energies', 'Commodities/Grains', 'Commodities/Meats',
               'Commodities/Metals', 'Commodities/Softs', 'Cryptocurrencies', 'Currencies',
               'Funds_ETFs', 'Index']
#directories = ['Commodities/Energies']
marketDataFP = '../clean_data/market/'
markerStyle = ['.', ',', 'o', 'v', '^', '1', 'p', 'P', '*', '+']

filePaths = []
def readMarketCSV():
    rootPath = '../clean_data/market'
    for root, dirs, files in os.walk(rootPath):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith('.csv') and 'companylist' not in path and 'NewCompanyList' not in path:
                filePaths.append(path)
    print('### Load market files completed ###')


def getDailyChange(filePath):
    print('### Get Daily Change, file Name:', filePath)
    df = pd.read_csv(filePath)

    if 'DailyIncreasingRate' in df.columns.values:
        df = df.drop('DailyIncreasingRate', axis=1)
    if 'DailyFlucRange' in df.columns.values:
        df = df.drop('DailyFlucRange', axis=1)
    if 'DailyFlucRate' in df.columns.values:
        df = df.drop('DailyFlucRate', axis=1)
    if 'OpenLastCloseRate' in df.columns.values:
        df = df.drop('OpenLastCloseRate', axis=1)

    if 'Close/Last' in df.columns.values:
        close = df.sort_values('Date', ascending=True)['Close/Last']
        close_change = close.pct_change().sort_index(ascending=True)
        df['DailyIncreasingRate'] = close_change * 100
    if 'High' in df.columns.values:
        df['DailyFlucRange'] = df['High'] - df['Low']
    if 'DailyFlucRange' in df.columns.values:
        # 后期更新波动率公式
        df['DailyFlucRate'] = df['DailyFlucRange'] / df['Close/Last'] * 100
    if 'Open' in df.columns.values:
        df['OpenLastCloseRate'] = (df['Open'] - df['Close/Last'].shift(-1)) / df['Close/Last'].shift(-1) * 100
    df.to_csv(filePath, index=False, header=True)


def getDataValues(data: 'data DateFrame', attr: 'value attribute', date: 'date range list'):
    minmax_scaler = pprs.MinMaxScaler()
    # re-sort
    data = data.sort_values('Date', ascending=True)
    # date range
    data = data[(data['Date'] >= date[0]) & (data['Date'] <= date[-1])]
    # specified data attribute
    data_date = data['Date'].tolist()
    data_value = data[attr].values.reshape(-1, 1)
    data_value = minmax_scaler.fit_transform(data_value)
    return [data_date, data_value]


def analyzeMarketCSVByDirectory():
    covidDF_confirmed = pd.read_csv(covidDP_confirmed)
    date = covidDF_confirmed['Date'].tolist()
    for directory in directories:
        rootPath = marketDataFP + directory
        timeSeries = []
        dailyIncreasingRate = []
        dailyFlucRange = []
        dailyFlucRate = []
        openLastCloseRate = []
        for root, dirs, files in os.walk(rootPath):
            for file in files:
                path = os.path.join(root, file)
                if path.endswith('.csv'):
                    data = pd.read_csv(path)
                    print(path)
                    # data['Date'] = pd.to_datetime(data['Date'])
                    fileName = file[:-4]
                    # time series
                    if 'Close/Last' in data.columns.values:
                        timeSeries.append([fileName, getDataValues(data, 'Close/Last', date)])
                    # daily increasing rate
                    if 'DailyIncreasingRate' in data.columns.values:
                        dailyIncreasingRate.append([fileName, getDataValues(data, 'DailyIncreasingRate', date)])
                    # daily fluc range
                    if 'DailyFlucRange' in data.columns.values:
                        dailyFlucRange.append([fileName, getDataValues(data, 'DailyFlucRange', date)])
                    # daily fluc rate
                    if 'DailyFlucRate' in data.columns.values:
                        dailyFlucRate.append([fileName, getDataValues(data, 'DailyFlucRate', date)])
                    # open / last-close rate
                    if 'OpenLastCloseRate' in data.columns.values:
                        openLastCloseRate.append([fileName, getDataValues(data, 'OpenLastCloseRate', date)])
        # plot data
        if timeSeries:
            plotData(timeSeries, directory, 'TimeSeries', 3, 0)
        if dailyIncreasingRate:
            plotData(dailyIncreasingRate, directory, 'DailyIncreasingRate', 3, 0)
        if dailyFlucRange:
            plotData(dailyFlucRange, directory, 'DailyFlucRange', 3, 0)
        if dailyFlucRate:
            plotData(dailyFlucRate, directory, 'DailyFlucRate', 3, 0)
        if plotData:
            plotData(openLastCloseRate, directory, 'OpenLastCloseRate', 3, 0)


def plotCOVID(plotType: '1: US Confirmed, 2: World Confirmed, 3: US Deaths, 4: World Deaths' = 2):
    # load file
    covidDF_confirmed = pd.read_csv(covidDP_confirmed)
    covidDF_deaths = pd.read_csv(covidDP_deaths)
    date = covidDF_confirmed['Date'].tolist()
    # load data
    data = covidDF_confirmed['World'].values
    label = 'World Confirmed'
    if plotType == 1:
        data = covidDF_confirmed['US'].values
        label = 'US Confirmed'
    elif plotType == 3:
        data = covidDF_deaths['US'].values
        label = 'US Deaths'
    elif plotType == 4:
        data = covidDF_deaths['World'].values
        label = 'World Deaths'
    # plot data
    data = data.reshape(-1, 1)
    minmax_scaler = pprs.MinMaxScaler()
    fit_data = minmax_scaler.fit_transform(data)
    plt.plot(date, fit_data, label=label)


def plotData(data, directory, name,
             covidConfirm: '0: No COVID Confirmed Data, 1: US Confirmed Data, 2: World Confiremd Data, 3: US + World Confirmed Data' = 2,
             covidDeath: '0: No COVID Deaths Data, 1: US Deaths Data, 2: World Deaths Data, 3: US + World Deaths Data' = 0) -> bool:
    plt.figure(figsize=(12, 8))
    print(directory + '-' + name)
    plt.title(directory + '-' + name)
    plotNumber = 0
    # plot COVID
    if covidConfirm == 1:
        plotCOVID(1)
    elif covidConfirm == 2:
        plotCOVID(2)
    elif covidConfirm == 3:
        plotCOVID(1)
        plotCOVID(2)
    if covidDeath == 1:
        plotCOVID(3)
    elif covidDeath == 2:
        plotCOVID(4)
    elif covidDeath == 3:
        plotCOVID(3)
        plotCOVID(4)
    # plot data
    for dat in data:
        data_label = dat[0]
        data_date = dat[1][0]
        data_value = dat[1][1]
        print(data_date)
        print(data_value)
        plt.plot(data_date, data_value, label=data_label, linewidth=1, linestyle='--', marker=markerStyle[plotNumber % 10], markersize=3)
        plt.xticks(rotation=90)
        plt.yticks([])
        plt.legend()
        plotNumber = plotNumber + 1
    directory = directory.replace('/', '_')
    # If not exist, create folder 'result'
    if not os.path.exists('resultNew'):
        os.makedirs('resultNew')
        print('directory result created')
    picName = '../analyzed_data/' + directory + '-' + name + '.png'
    #plt.show()
    plt.savefig(picName)
    plt.close()


if os.path.exists('../analyzed_data/'):
    shutil.rmtree('../analyzed_data/', ignore_errors=True)
os.makedirs('../analyzed_data/')

readMarketCSV()
for filePath in filePaths:
    getDailyChange(filePath)
analyzeMarketCSVByDirectory()
