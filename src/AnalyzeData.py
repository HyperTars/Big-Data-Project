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


def readMarketCSV():
    rootPath = '../clean_data/market'
    for root, dirs, files in os.walk(rootPath):
        if 'Stock' not in root:
            for file in files:
                path = os.path.join(root, file)
                if path.endswith('.csv'):
                    filePaths.append(path)
    print('### Load market files completed ###')


def readStockHistoryCSV():
    rootPath = '../clean_data/market/Stock/history'
    for root, dirs, files in os.walk(rootPath):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith('.csv'):
                stockPaths.append(path)
    print('### Load Stock Hisotry files completed ###')


def getNewPath(path):
    return '../analyzed_data' + path[13:]


def analyzeMarketData(filePath):
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
    print(df.head(2))
    print('\n')
    df.to_csv(getNewPath(filePath), index=False, header=True)


if os.path.exists('../analyzed_data/'):
    shutil.rmtree('../analyzed_data/', ignore_errors=True)
os.makedirs('../analyzed_data/')
os.makedirs('../analyzed_data/covid-19')
os.makedirs('../analyzed_data/employment')
os.makedirs('../analyzed_data/general')
os.makedirs('../analyzed_data/market/Commodities/Energies')
os.makedirs('../analyzed_data/market/Commodities/Grains')
os.makedirs('../analyzed_data/market/Commodities/Meats')
os.makedirs('../analyzed_data/market/Commodities/Metals')
os.makedirs('../analyzed_data/market/Commodities/Softs')
os.makedirs('../analyzed_data/market/Cryptocurrencies')
os.makedirs('../analyzed_data/market/Currencies')
os.makedirs('../analyzed_data/market/Funds_ETFs')
os.makedirs('../analyzed_data/market/Index')
os.makedirs('../analyzed_data/market/Stock/history')

filePaths = []
stockPaths = []
readMarketCSV()
# readStockHistoryCSV()

for filePath in filePaths:
    analyzeMarketData(filePath)
