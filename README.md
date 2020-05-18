# Big-Data-Project

## Group Members
Wenzhou Li <wl2154@nyu.edu>

Linyi Yan <ly1333@nyu.edu>

Tingfeng Mai <tm3358@nyu.edu>

## Related Documentation Links
Full Report: https://docs.google.com/document/d/1i3iQkhmNyG4myV1ErU-NR5ze9icRVYVLuITZ561nBX0/edit

Prez PPT: https://1drv.ms/p/s!AqLzalILZz0hu1wSfb9AGRcq7ESc?e=mEjx7a

## Setup Instruction
Raw company history data in `raw_stock_history_0421.zip`, we only keep a zipped file in git because they are too large, you can extract to your local disk before using. These stock data should be extracted and placed in a folder call 'stock-history' (should also be created manually) under '../clean_data'. Other raw data from `raw_data_0422.zip` is already extracted to data/ folder.

Our source code resides in `src/` folder. To start, please enter the folder via the command: `cd src/`

- To clean data, run `CleanData.py`, the results will be saved in `../clean_data/`. To have a better understanding of what we do in this part, you can optionally run `CleanData.ipynb` to observe the better visualized version of cleaning code.
  
- To do quantitative analysis, run `AnalyzeData.py`, the results will be saved in ../analyzed_data/
  
- To plot largest one day drops results, run `PlotData.py`, the results will be saved in `../result/largest_one_day_drops/`

- To plot quantitative analysis, run `PlotData.ipynb`, the results will be saved in `../result/market/`

- To get time series trend data of all indicators, run `time-series-analysis.ipynb`, the results will be saved in `../result/time-series/`

- To perform correlation analysis, run `DataAnalyze.ipynb`, the results will be saved in `../result/correlations/`

- To compare the stock market crash to crashes in some other financial crises years, run `market_drop_analysis/DataAnalyze.ipynb`, the results images can be directly viewed in the ipynb file.
