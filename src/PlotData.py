import pandas as pd
import numpy as np
import platform as pf
import os
import xlrd
import matplotlib
import shutil
import matplotlib.dates as mdate
from matplotlib import pyplot as plt
from sklearn import preprocessing as pprs
from scipy import stats
from datetime import datetime
from datetime import datetime

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

pd.set_option('max_row', 1000)
pd.set_option('max_column', 10)

covidDP_confirmed = '../analyzed_data/covid-19/time_series_covid19_confirmed_global.csv'
covidDP_deaths = '../analyzed_data/covid-19/time_series_covid19_deaths_global.csv'
directories = ['Commodities/Energies', 'Commodities/Grains', 'Commodities/Meats',
               'Commodities/Metals', 'Commodities/Softs', 'Cryptocurrencies', 'Currencies',
               'Funds_ETFs', 'Index']
directories_index = '../analyzed_data/market/Index'
marketDataFP = '../analyzed_data/market/'
markerStyle = ['.', ',', 'o', 'v', '^', '1', 'p', 'P', '*', '+']

covid_start_date = pd.read_csv(covidDP_confirmed).sort_values('Date', ascending=True).reset_index(drop=True)['Date'][0]
half_year_date = '2019-10-20'

'''
def analyzeMarketCSVByDirectory(column, type, startDate):
    for directory in directories:
        rootPath = marketDataFP + directory
        for root, dirs, files in os.walk(rootPath):
            for file in files:
                path = os.path.join(root, file)
                if path.endswith('.csv'):
                    df = pd.read_csv(path)
                    # re-sort
                    df = df.sort_values('Date', ascending=True)
                    df = df.reset_index(drop=True)
                    df = df[(df['Date'] >= startDate)]
                    # date range
                    if (type == 'lines'):
                        minmax_scaler = pprs.MinMaxScaler()
                        # specified data attribute
                        data_date = df['Date'].tolist()
                        data_value = df[column].values.reshape(-1, 1)
                        data_value = minmax_scaler.fit_transform(data_value)
                    if (type == 'bars'):
                        data_date = df['Date'].tolist()
                        data_value = df[column].values


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
        # plt.plot(data_date, data_value, label=data_label, linewidth=1, linestyle='--', marker=markerStyle[plotNumber % 10], markersize=3)
        plt.bar(data_date, data_value, label=data_label)
        # to be updated: 转成直方图
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
'''

def plotLargestOneDayDrops(df, title):
    dft = df.sort_values('DailyRiseRate', ascending=True).head(20)
    dft.sort_values('DailyRiseRate', inplace=True, ascending=False)
    plt.figure(figsize=(10, 4))
    plt.title(title + ' Largest One Day Drops (since 2010)')
    plt.barh(dft['Date'], dft['DailyRiseRate'])
    plt.xlabel('Daily Rise Rate')
    plt.ylabel('Date')
    if not os.path.exists('../result/largest_one_day_drops/'):
        os.makedirs('../result/largest_one_day_drops/')
    plt.savefig('../result/largest_one_day_drops/' + title + '.png')


# plot largest one day drops for indices
for root, dirs, files in os.walk(directories_index):
    for file in files:
        path = os.path.join(root, file)
        if path.endswith('.csv'):
            df = pd.read_csv(path)
            plotLargestOneDayDrops(df, file[:-4])



'''
analyzeMarketCSVByDirectory()

df = pd.read_csv('../analyzed_data/market/Index/S&P_500.csv')
df = pd.read_csv('../analyzed_data/market/Index/DowJones_IndustrialAvg.csv')
df.sort_values('Date', inplace=True, ascending=True)
df = df.reset_index(drop=True)
dfe = df[(df['Date'] > '2019-10-20')]
dfe.set_index('Date', inplace=True)

dfe['DailyRiseRate'].plot()
r = random.random()
b = random.random()
g = random.random()
sub.set_ylabel('Returns')
sub.grid(which="major", color='k', linestyle='-.', linewidth=0.2)
plt.axvline(x='2020-01-30', color='RoyalBlue', linestyle='dashdot', linewidth=3)
plt.axvline(x='2020-03-11', color='Red', linestyle='dashdot', linewidth=3)
fig = plt.figure(figsize=(12, 8))
sub = fig.add_subplot()
plt.tight_layout()
plt.show()



plt.figure(figsize=(12, 8))
df = df[(df['Date'] > '2020-01-22')]
df = df.sort_values('Date', ascending=True).reset_index(drop=True)
df.set_index('Date', inplace=True)
df['MAD'].plot(kind='bar')
ax = plt.gca()
ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
plt.xticks(pd.date_range(df.index[0], df.index[-1], freq='M'), rotation=45)
ax.plot(df.index, df['MAD'], color='r')
plt.tight_layout()
plt.tick_params(labelsize=8)

Close/Last in lines
DailyRise in Bars
DailyRiseRate in Bars
DailyReturn in  Bars
DailyRippleRange in Bars
DailyRippleRadio in Bars
DailyK in Lines & Bars
MA5 in Lines
MA15 in Lines
MA30 in Lines
EWMA in Lines
MACD in Bars
K in Bars
D in Bars
J in Bars
rs in Bars
rsi in Bars
MAD in Bars
'''