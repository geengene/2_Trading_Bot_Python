import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fast')

SPY = yf.download("SPY")
spy = SPY.Close.to_frame()
print(spy)


spy_roll = spy.rolling(window=10)
spy_roll = spy_roll.mean()
print(spy_roll.head(15))
print(spy.rolling(window=10).median())
print(spy.rolling(window=10).max())
print(spy.rolling(window=10, min_periods=5).max())

spy["SMA50"] = spy.rolling(window=50, min_periods=50).mean() #Simple Moving Average https://www.investopedia.com/ask/answers/012815/why-50-simple-moving-average-sma-so-common-traders-and-analysts.asp
print(spy.head(53))
spy["SMA200"] = spy.Close.rolling(window=200, min_periods=200).mean()

spy["EMA100"] = spy.Close.ewm(span=100, min_periods=100).mean()

spy["Day"] = spy.index.day_name()
spy["Quarter"] = spy.index.quarter

#reindexing
all_days = pd.date_range(start="2014-01-01", end="2024-01-01", freq="D")
spy = spy.reindex(all_days)

#fills
spy.ffill(inplace=True)

aapl = yf.download("AAPL", interval="1wk")
print(aapl)

print(spy)


spy.plot(figsize=(12,8), fontsize=15)
plt.legend(loc="upper left", fontsize=15)
plt.show()


