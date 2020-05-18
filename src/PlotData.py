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
