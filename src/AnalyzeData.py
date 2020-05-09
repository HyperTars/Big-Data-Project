import pandas as pd
import numpy as np
import os
import shutil
import datetime as dt


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


def getLastDay(path, lastDay):
    df = pd.read_csv(path)
    df.sort_values('Date', inplace=True, ascending=False)
    if df['Date'][0] < lastDay:
        return df['Date'][0]
    return lastDay


def trimLastDay(df, lastDay):
    return df[(df['Date'] <= lastDay)]


def analyzeMarketData(filePath, lastDay):
    df = pd.read_csv(filePath)
    df = trimLastDay(df, lastDay)
    #################
    # Daily Changes #
    #################
    df.sort_values('Date', inplace=True, ascending=False)
    df = df.reset_index(drop=True)
    df['LastClose'] = df['Close/Last'].shift(-1)

    # Daily Rise 日涨跌
    if 'DailyRise' in df.columns.values:
        df = df.drop('DailyRise', axis=1)
    if 'Close/Last' in df.columns.values:
        df['DailyRise'] = df['Close/Last'].diff(-1)

    # Daily Rise Rate 日涨跌率
    if 'DailyRiseRate' in df.columns.values:
        df = df.drop('DailyRiseRate', axis=1)
    if 'DailyRise' in df.columns.values:
        df['DailyRiseRate'] = (df['DailyRise'] / df['LastClose'])

    # Daily Return 日累计收益
    if 'DailyReturn' in df.columns.values:
        df = df.drop('DailyReturn', axis=1)
    if 'Close/Last' in df.columns.values:
        df['DailyReturn'] = (df['Close/Last'].pct_change(1) + 1).cumprod()

    # Daily Rise Log 日涨跌log
    if 'DailyRiseLog' in df.columns.values:
        df = df.drop('DailyRiseLog', axis=1)
        df['DailyRiseLog'] = (df['Close/Last'].apply(np.log) - df['LastClose'].apply(np.log))

    # Daily Ripple Range / 日波动范围
    if 'DailyRippleRange' in df.columns.values:
        df = df.drop('DailyRippleRange', axis=1)
    if 'High' in df.columns.values:
        df['DailyRippleRange'] = df['High'] - df['Low']

    # Daily Ripple Radio (VIX) / 日波动率
    if 'DailyRippleRadio' in df.columns.values:
        df = df.drop('DailyRippleRadio', axis=1)
    if 'High' in df.columns.values:
        df['DailyRippleRadio'] = df['High'] / df['Low']

    # Daily K / 日震荡幅度
    if 'DailyK' in df.columns.values:
        df = df.drop('DailyK', axis=1)
    if 'DailyRippleRange' in df.columns.values:
        df['DailyK'] = df['DailyRippleRange'] / df['LastClose']

    #################
    # Period Trends #
    #################
    df.sort_values('Date', inplace=True, ascending=True)
    df = df.reset_index(drop=True)

    # Moving Average / 移动平均线 (趋势) -> 最好放到 PlotData.py 里，过滤完日期后再求移动平均线
    MA_WindowSize = [5, 15, 30]
    if 'Close/Last' in df.columns.values:
        for i in MA_WindowSize:
            if 'MA' + str(i) in df.columns.values:
                df = df.drop('MA' + str(i), axis=1)
            df['MA' + str(i)] = df['Close/Last'].rolling(i).mean()
    '''
    # Test
    dfe = df[(df['Date'] > '2020-01-21')]
    dfe.sort_values('Date', inplace=True, ascending=True)
    dfe = dfe.reset_index(drop=True)
    dfe['MA15'] = dfe['Close/Last'].rolling(15).mean()
    dfe['MA30'] = dfe['Close/Last'].rolling(30).mean()
    dfe[['Close/Last', 'MA5', 'MA15', 'MA30']].plot(subplots=False, figsize=(12, 6), grid=True)
    plt.show()
    '''

    # Exponentially Weighted Moving-Average / 指数加权移动平均值 (趋势)
    EWMA_SPAN = 5
    if 'EWMA' in df.columns.values:
        df = df.drop('EWMA', axis=1)
    if 'Close/Last' in df.columns.values:
        df['EWMA'] = df['Close/Last'].ewm(span=EWMA_SPAN, ignore_na=True, adjust=True).mean()

    # Moving Average Convergence / Divergence 异同移动平均线 (振荡指标)
    if 'MACD' in df.columns.values:
        df = df.drop('MACD')
    if 'Close/Last' in df.columns.values:
        MCDA_short = 5
        MCDA_mid = 15
        MCDA_long = 30
        sema = df['Close/Last'].ewm(span=MCDA_short).mean()
        lema = df['Close/Last'].ewm(span=MCDA_long).mean()
        df.fillna(0, inplace=True)
        ema_dif = sema - lema
        dea = ema_dif.ewm(span=MCDA_mid).mean()
        df['MACD'] = 2 * ema_dif - dea

    # KDJ Index / 随机指标 (趋势)
    if 'K' in df.columns.values:
        df = df.drop('K')
    if 'D' in df.columns.values:
        df = df.drop('D')
    if 'J' in df.columns.values:
        df = df.drop('J')
    if 'High' in df.columns.values:
        low_list = df['Low'].rolling(9, min_periods=9).min()
        low_list.fillna(value=df['Low'].expanding().min(), inplace=True)
        high_list = df['High'].rolling(9, min_periods=9).max()
        high_list.fillna(value=df['High'].expanding().max(), inplace=True)
        rsv = (df['Close/Last'] - low_list) / (high_list - low_list) * 100
        df['K'] = pd.DataFrame(rsv).ewm(com=2).mean()
        df['D'] = df['K'].ewm(com=2).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']

    # Relative Strength Index / 相对强弱指标 (价值回归)
    '''
    N日RSI = N日内收盘涨幅的平均值/(N日内收盘涨幅均值+N日内收盘跌幅均值) ×100
    由上面算式可知RSI指标的技术含义，即以向上的力量与向下的力量进行比较，若向上的力量较大，则计算出来的指标上升；若向下的力量较大，则指标下降，由此测算出市场走势的强弱。
    市场上一般的规则：（快速RSI指14日的RSI，慢速RSI指6日的RSI）
    1. RSI 金叉：快速 RSI 从下往上突破慢速 RSI 时,认为是买进机会。
    2. RSI 死叉：快速 RSI 从上往下跌破慢速 RSI 时,认为是卖出机会
    3. 慢速RSI<20 为超卖状态,为买进机会。
    4. 慢速RSI>80 为超买状态,为卖出机会。
    '''
    if 'DailyRise' in df.columns.values:
        RSI_WINDOW = 14
        df['rsi_gain'] = np.select([df['DailyRise'] > 0, df['DailyRise'].isna()], [df['DailyRise'], np.nan], default=0)
        df['rsi_loss'] = np.select([df['DailyRise'] < 0, df['DailyRise'].isna()], [-df['DailyRise'], np.nan], default=0)
        df['avg_gain'] = np.nan
        df['avg_loss'] = np.nan
        df['avg_gain'][RSI_WINDOW] = df['rsi_gain'].rolling(window=RSI_WINDOW).mean().dropna().iloc[0]
        df['avg_loss'][RSI_WINDOW] = df['rsi_loss'].rolling(window=RSI_WINDOW).mean().dropna().iloc[0]
        for i in range(RSI_WINDOW + 1, df.shape[0]):
            df['avg_gain'].iloc[i] = (df['avg_gain'].iloc[i - 1] * (RSI_WINDOW - 1) + df['rsi_gain'].iloc[i]) / RSI_WINDOW
            df['avg_loss'].iloc[i] = (df['avg_loss'].iloc[i - 1] * (RSI_WINDOW - 1) + df['rsi_loss'].iloc[i]) / RSI_WINDOW
        # calculate rs and rsi
        df['rs'] = df['avg_gain'] / df['avg_loss']
        df['rsi'] = 100 - (100 / (1 + df['rs']))
        df = df.drop('rsi_gain', axis=1)
        df = df.drop('rsi_loss', axis=1)
        df = df.drop('avg_loss', axis=1)
        df = df.drop('avg_gain', axis=1)

    # Mean Absolute Deviation
    if 'Close/Last' in df.columns.values:
        df['MAD'] = df['Close/Last'].rolling(window=5).apply(lambda x: np.fabs(x - x.mean()).mean())

    df.sort_values('Date', inplace=True, ascending=False)
    df = df.reset_index(drop=True)
    print(getNewPath(filePath))
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
lastDay = dt.datetime.now().strftime('%Y-%m-%d')
# readStockHistoryCSV()

for filePath in filePaths:
    lastDay = getLastDay(filePath, lastDay)

for filePath in filePaths:
    analyzeMarketData(filePath, lastDay)

COVID_CONFIRMED = '../clean_data/covid-19/time_series_covid19_confirmed_global.csv'
COVID_DEATHS = '../clean_data/covid-19/time_series_covid19_deaths_global.csv'
trimLastDay(pd.read_csv(COVID_CONFIRMED), lastDay).to_csv(getNewPath(COVID_CONFIRMED), index=False, header=True)
trimLastDay(pd.read_csv(COVID_DEATHS), lastDay).to_csv(getNewPath(COVID_DEATHS), index=False, header=True)
