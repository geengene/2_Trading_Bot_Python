import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fast')

tickers = ["AAPL", "SPY", "QQQ","NVDA", "META","GOOGL"]
stocks = yf.download(tickers, start="2013-01-01", end="2024-01-01")

stocks.to_csv("stocks.csv")
stocks = pd.read_csv("stocks.csv", header=[0,1], index_col=[0], parse_dates=[0])
stocks.columns = stocks.columns.to_flat_index()# converts multi index to tuple
stocks.columns = pd.MultiIndex.from_tuples(stocks.columns) # reverts tuple back to multi index
stocks.describe()

close = stocks.loc[:,"Close"].copy() # copies the close column to the variable
print(close)
print(close.iloc[0])
normclose = close.div(close.iloc[0]).mul(100) # normalise all initial close values to start at 100
print(normclose)

normclose.plot(figsize=(15, 8), fontsize=12)
plt.legend(fontsize=12)

aapl = close.AAPL.copy().to_frame()# convert data to dataframe
print(aapl)
print(aapl.shift(periods=1))
aapl["lag1"] = aapl.shift(periods=1) # creates a new column called lag1 containing aapl close data shifted by a period of 1
aapl["diff"] = aapl.AAPL.sub(aapl.lag1) # to compare difference in change between dates.
aapl["%change"] = aapl.AAPL.div(aapl.lag1).sub(1).mul(100)
aapl["diff2"] = aapl.AAPL.diff(periods=1)
aapl["%change2"] = aapl.AAPL.pct_change(periods=1).mul(100)

del aapl["diff"]
del aapl['%change']
del aapl['diff2']
del aapl['lag1']
aapl.rename(columns = {"%change2": 'change'}, inplace = True)
print(aapl)

print(aapl.AAPL.resample('ME').last()) # ME is last day of every month, BME is last business day of every month
print(aapl.AAPL.resample('BME').last().pct_change(periods=1).mul(100))
del aapl['change']
print(aapl)
ret = aapl.pct_change().dropna() #
ret.info()

ret.plot(kind="hist", figsize=(12,8), bins=100)
plt.show()

daily_mean_return = ret.mean()
print(daily_mean_return)
var_daily = ret.var()
print(var_daily)
std_daily = np.sqrt(var_daily) #standard deviation(risk metric)
print(std_daily)
annual_mean_return = daily_mean_return*252
annual_var_return = var_daily*252
annual_std_return = np.sqrt(annual_var_return)





