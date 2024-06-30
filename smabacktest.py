import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def test_strategy(stock, start, end, SMA):
    df = yf.download(stock, start=start, end=end)
    data = df.Close.to_frame()
    data["returns"] = np.log(data.Close.div(data.Close.shift(1)))
    data["SMA_S"] = data.Close.rolling(int(SMA[0])).mean()
    data["SMA_L"] = data.Close.rolling(int(SMA[1])).mean()
    data.dropna(inplace=True)
    
    data["position"] = np.where(data["SMA_S"]>data["SMA_L"], 1, -1) 
    data["strategy"] = data["returns"]*data.position.shift(1)
    data.dropna(inplace=True)
    ret = np.exp(data["strategy"].sum())
    std = data["strategy"].std()*np.sqrt(252)
    
    return ret, std

print(test_strategy("TSLA", "2000-01-01", "2024-06-01", (50,200)))   

class SMABacktester():
    def __init__(self, symbol, SMA_S, SMA_L, start, end) -> None:
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end
        self.results = None
        self.get_data()
        
    def get_data(self):
        df = yf.download(self.symbol, start=self.start, end=self.end)
        data = df.Close.to_frame()
        data["returns"] = np.log(data.Close.div(data.Close.shift(1)))
        data["SMA_S"] = data.Close.rolling(self.SMA_S).mean()
        data["SMA_L"] = data.Close.rolling(self.SMA_L).mean()
        data.dropna(inplace=True)
        self.data2 = data
        
        return data
    
    def test_results(self):
        data = self.data2.copy().dropna()
        data["position"] = np.where(data["SMA_S"]>data["SMA_L"], 1, -1) 
        data["strategy"] = data["returns"]*data.position.shift(1)
        data.dropna(inplace=True)
        data["returnsB&H"] = data["returns"].cumsum().apply(np.exp)
        data["returns_strategy"] = data["strategy"].cumsum().apply(np.exp)
        
        perf = data["returns_strategy"].iloc[-1]
        outperf = perf-data["returnsB&H"].iloc[-1]
        self.results = data
        
        ret = np.exp(data["strategy"].sum())
        std = data["strategy"].std()*np.sqrt(252)
        
        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        if self.results is None:
            print("Run the test please")
        else:
            title = f"{self.symbol} | SMA_S={self.SMA_S} | SMA_L={self.SMA_L}"
            self.results[["returnsB&H", "returns_strategy"]].plot(title = title, figsize=(12, 8))
            plt.show()
            
tester = SMABacktester("SPY", 50, 100, "2000-01-01", "2020-01-01")
print(tester.test_results())
tester.plot_results()
    