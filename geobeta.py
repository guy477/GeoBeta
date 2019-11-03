import yfinance as yf
from pandas_datareader import data as alt
import pandas as pd
import re
import numpy as np

#ticker, time, rolling time, increment, (maybe market ticker)


"""
Ticker: Ticker symbol   
Time Frame: How far back you want to go ------------------------------- 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max                  How far back you want to go will depend on Increment
Increment: How much time you want to increment Time Frame ------------- 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
Rolling Time: How long you want you rolling average to last ----------- Must be a multiple of Increment
Rolling Increment: How much time you want to increment Rolling Time --- Must be a multiple of Increment
"""
# valid time frames:  
# valid rolling:      
# valid intervals:    


data = pd.DataFrame()
while(data.empty):
    print("Ticker:Time Frame:Increment:Rolling Time:Rolling Increment")
    a = input()
    a = re.split(r"[:\s]", a)
    print(a[0].upper())
    data = yf.download(tickers = "^GSPC "+a[0].upper(),
                    period = a[1].lower(),
                    interval = a[2].lower(),
                    group_by = 'ticker',                  
                    auto_adjust = True,          # adjust all OHLC automatically
                    prepost = False,             # download pre/post regular market hours data
                    threads = True)              # use threads for mass downloading? (True/False/Integer)

#print(data)
data = pd.DataFrame(data)
data['^GSPC'] = data['^GSPC'].drop(columns=['Open', 'High', 'Low', 'Volume'])
data[a[0].upper()] = data[a[0].upper()].drop(columns=['Open', 'High', 'Low', 'Volume'])
data=data.dropna(how='all')

print(data.head())

adjret = [[], []]
for i in range(1, data.__len__()):
    adjret[0].append((data[a[0].upper()]['Close'][i] - data[a[0].upper()]['Close'][i-1])/data[a[0].upper()]['Close'][i-1] + 1)
    adjret[1].append((data['^GSPC']['Close'][i] - data['^GSPC']['Close'][i-1])/data['^GSPC']['Close'][i-1] + 1)

geoMean = [[], []]

for i in range(0, len(adjret[0]), int(a[4])):
    t = [0.0, 0.0]
    for j in range(i, i+int(a[3])):
        if(j<len(adjret[0])):
            #print(j, len(adjret[1]))
            t[0] += adjret[0][j]
            t[1] += adjret[1][j]
    geoMean[0].append(t[0]/float(a[3]))
    geoMean[1].append(t[1]/float(a[3]))

t = [np.cov(geoMean[0], geoMean[1]), np.var(geoMean[0])]

print(t)
print(t[0][0][1]/t[1])