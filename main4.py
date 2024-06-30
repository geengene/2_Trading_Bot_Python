import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fast')

nvda = yf.download("NVDA")
nvda = nvda.Close.to_frame()
nvda["d_returns"] = np.log(nvda.div(nvda.shift(1)))# daily returns
nvda.dropna(inplace=True)

print(nvda.d_returns.sum()) #if $1 invested since start

print(np.exp(nvda.d_returns.sum()))

nvda["cumm_returns"] = nvda.d_returns.cumsum().apply(np.exp)


nvda.d_returns.mean()*252 #annual average returns
nvda.d_returns.std()*np.sqrt(252)# annual standard deviation

#calculate drawdowns
nvda["cummmax"] = nvda.cumm_returns.cummax()
nvda[["cummmax","cumm_returns"]].plot(figsize=(12,8), title="NVDIA buy and hold+cummmax", fontsize=12)

nvda["drawdown"] = nvda["cummmax"] - nvda["cumm_returns"]
print(nvda.drawdown.max())
print(nvda.drawdown.idxmax())
print(nvda.loc[(nvda.index=='2022-10-14')])
print(nvda.loc[(nvda.index<='2022-10-14')])
nvda["drawdown%"] = (nvda["cummmax"] - nvda["cumm_returns"])/nvda["cummmax"]
print(nvda["drawdown%"].max())
print(nvda["drawdown%"].idxmax())

print(nvda)
#plt.show()