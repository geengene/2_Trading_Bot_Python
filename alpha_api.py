import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

API_key = "Z21EYFELCDFWYR8U"
ts = TimeSeries(key=API_key, output_format='pandas')

data, meta = ts.get_intraday("AAPL", interval='5min', outputsize='full')
print(meta)
print(data.info())
print(data.head())
data['4. close'].plot(figsize=(12,8),  fontsize=12)
plt.show()

#Renaming columns and add separate date and time columns
columns = ['open', 'high', 'low', 'close', 'volume']
data.columns = columns

data['TradeDate'] = data.index.date
data['Time'] = data.index.time
print(data.loc['2024-06-18'])
market = data.between_time('09:30:00', '16:00:00').copy()
market.sort_index(inplace=True)
print(market.info())
print(market.groupby('TradeDate').agg({'low':'min', 'high': 'max'}))
print(market.loc[market.groupby('TradeDate')['low'].idxmin()])




