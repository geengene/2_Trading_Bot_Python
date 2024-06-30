import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fast')


tickers = ["AAPL", "SPY", "QQQ","NVDA", "META","GOOGL"]
stocks = yf.download(tickers, start="2013-01-01", end="2024-01-01")

close = stocks.loc[:,"Close"].copy() # copies the Close column to the variable
normclose = close.div(close.iloc[0]).mul(100) # normalise all initial close values to start at 100
normclose.plot(figsize=(15, 8), fontsize=12)
plt.legend(fontsize=12)


ret = close.pct_change().dropna()
print(ret)
summary = ret.describe().T.loc[:,["mean","std"]]# .T inverts x and y axis, .loc[:,["mean","std"]] shows just the 2 columns
print(summary)
summary["mean"] = summary["mean"]*252
summary["std"] = summary["std"]*np.sqrt(252)
print(summary) #annual mean and std reveals risk returns

summary.plot.scatter(x="std", y="mean", figsize=(12,8), s=50, fontsize=15)
for i in summary.index:
    plt.annotate(i, xy=(summary.loc[i,"std"]+0.002, summary.loc[i,"mean"]+0.002), size=15)
plt.xlabel("Annual risk(std)", fontsize=15) 
plt.ylabel("Annual return(mean)", fontsize=15) 
plt.title("Risk/return", fontsize=25)

#correlation and covariance
plt.figure(figsize=(12,8))
sns.set_theme(font_scale=1.4)
sns.heatmap(ret.corr(), cmap="Reds",annot=True, annot_kws={"size":15}, vmax=0.6)

#simple returns and log returns
df = pd.DataFrame(index=[2016, 2017, 2018], data=[100, 50, 95], columns=["Price"])
print(df)
simplereturns = df.pct_change().dropna()
print(simplereturns)
print(simplereturns.mean())
print(100*1.2*1.2) # mean returns are misleading
logreturns = np.log(df/df.shift(1)).dropna()
print(logreturns)
print(logreturns.mean())
print(100*np.exp(logreturns.mean()*2)) # https://gregorygundersen.com/blog/2022/02/06/log-returns/



plt.show()