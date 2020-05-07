import pandas as pd
import numpy as np
import platform as pf
import os
import xlrd

filePaths = []


def readMarketCSV():
    rootPath = "../data/market"
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

    newPath = '../result/market/' + filePath.strip('\n').split("/")[-1][:-4] + '.analyzed.csv'
    print(newPath)
    # print(df)
    df.to_csv(newPath, index=False, header=True)


readMarketCSV()
for filePath in filePaths:
    getDailyChange(filePath)
