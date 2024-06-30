import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_datareader as pdr
plt.style.use('fast')

nvda = yf.download("NVDA")
data = nvda.Close.to_frame()
sma_s=50
sma_l = 100

data["sma_s"] = data.Close.rolling(sma_s).mean()
data["sma_l"] = data.Close.rolling(sma_l).mean()





data["returnsB&H"] = np.log(data.Close.div(data.Close.shift(1)))

data["position1"] = np.where(data["sma_s"]>data["sma_l"], 1, -1)
data["strategy1"] = data["returnsB&H"]*data.position1.shift(1)
data.loc["2024",["sma_s", "sma_l", "position1"]].plot(figsize=(12,8), title=f"NVDA - SMA{sma_s} | SMA{sma_l}", fontsize=12, secondary_y="position1")#long if sma50>sma100, short vice-versa

print(data[["returnsB&H", "strategy1"]].sum())
print(data[["returnsB&H", "strategy1"]].sum().apply(np.exp))#what $1 will be
print(data[["returnsB&H", "strategy1"]].std()*np.sqrt(252)) #annual std 

data["position2"] = np.where(data["sma_s"]>data["sma_l"], 1, 0)
data["strategy2"] = data["returnsB&H"]*data.position2.shift(1)

print(data[["returnsB&H", "strategy2"]].sum())
print(data[["returnsB&H", "strategy2"]].sum().apply(np.exp))#what $1 will be
print(data[["returnsB&H", "strategy2"]].std()*np.sqrt(252)) #annual std 

print(data[["strategy1", "strategy2"]].sum())
print(data[["strategy1", "strategy2"]].sum().apply(np.exp))# what $1 will be
print(data[["strategy1", "strategy2"]].std()*np.sqrt(252)) #annual std 
#strategy1 has greater returns but higher risk

data.dropna(inplace=True)
print(data)
#plt.show()
