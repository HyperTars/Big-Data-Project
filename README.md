# Impact-of-COVID-19-on-Financial-Market

![](https://img.shields.io/badge/python-3.7-green)

## Project Description
- Our project will focus on several economic indicators which should be considered and by how much the COVID-19 has affected the world’s economy. We will work on the problem: What economic indicators should be considered with the effect of COVID-19?. To be more specific, we will gather a wide range of economic indicators, analyze each indicator’s characteristics and its correlation with COVID-19, then make comparisons to find out those indicators which are most sensitive to COVID-19. We plan to analyze indicators including:
  - Stock market, which involves several indexes and each NASDAQ stock’s historical pricing data
  - Commodities market, which involves metals, energies, grains, meats and softs
  - Cryptocurrencies market
  - Currencies market, or specifically, the exchange rate market
- Since each indicator may vary from others, we expect to witness significant differences between each of them. For example, the stock markets are quite sensitive to the COVID-19 progress and fluctuate rapidly, while the exchange rate market may respond to the COVID-19 slower and remain nonvolatile. These differences will help us better figure out all indicators’ features and by how much they have been impacted by COVID-19.

## Related Documents
- Data Sets: [Datasets-used.csv](datasets-used.csv)

- Full Report: [Big Data Spring 2020.pdf]([BigDataSpring2020.pdf)
  or [Google Docs](https://docs.google.com/document/d/e/2PACX-1vQfVVlkV5pu67TuiVFkcvqsSSyRJqRxd99qZ5FSeqmagk3SliKXBHqkpf4doj1fquu87NbDH5wjKlAQ/pub)

- Prez PPT: [Big Data Prez.pptx](BigDataPrez.pptx)

## Setup Instruction
- Raw company history data in `raw_stock_history_0421.zip`, we only keep a zipped file in git because they are too large, you can extract to your local disk before using. These stock data should be extracted and placed in a folder call 'stock-history' (should also be created manually) under `../clean_data/`. 

- Other raw data from `raw_data_0422.zip` is already extracted to data/ folder.

- Our source codes reside in `src/` folder. To start, please enter the folder via the command: `cd src/`

### Data Cleaning
- To clean data, run `CleanData.py`, the results will be saved in `../clean_data/`. To have a better understanding of what we do in this part, you can optionally run `CleanData.ipynb` to observe the better visualized version of cleaning code.
  
### Data Analysis & Plotting
**QuantitativeAnalysis**
- To do quantitative analysis, run `AnalyzeData.py`, the results will be saved in ../analyzed_data/
- To plot largest one day drops results, run `PlotData.py`, the results will be saved in `../result/largest_one_day_drops/`
- To plot quantitative analysis, run `PlotData.ipynb`, the results will be saved in `../result/market/`

**TimeSeries**
- To get time series trend data of all indicators, run `time-series-analysis.ipynb`, the results will be saved in `../result/time-series/`

**Correlation**
- To perform correlation analysis, run `DataAnalyze.ipynb`, the results will be saved in `../result/correlations/`

**CompareToOtherCrises**
- To compare the stock market crash to crashes in some other financial crises years, run `market_drop_analysis/DataAnalyze.ipynb`, the results images can be directly viewed in the ipynb file.

## Contributing
- Wenzhou Li <wl2154@nyu.edu>

- Linyi Yan <ly1333@nyu.edu>

- Tingfeng Mai <tm3358@nyu.edu>

## Relevant projects
- [NYC Taxi Analysis](https://github.com/HyperTars/NYC-Taxi-Analysis)
  - MapReduce
  - PySpark (RDD and PySpark SQL)
  - OpenRefine (fingerprint & ngram, data cleaning)
