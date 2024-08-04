#import yfinance as yf
#data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")
#import yfinance as yf
#data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

import yfinance as yf
import pandas as pd
import os

os.chdir("D:/nse_download/ftse_sp_download")
path='D:/nse_download/ftse_sp_download/'

#Loading Symbols
#symbols = ['^GSPC','^VIX', '^FTSE', '^N225', '^HSI']
symbols = pd.read_csv(path+"LSE_STOCK_Combined.csv")
#stock_list = pd.read_csv('D:\\nse_download\\ftse_sp_download\\LSE_STOCK_Combined.csv')
symbols = symbols["Code"].to_list()
symbols = [i+".L" for i in symbols]
#print(symbols)
#print("NExt is data")
data = yf.download(symbols, start='2016-01-01')
#data = yf.download(symbols, start='2016-01-01', end  ='2024-06-03')
#print(data.head())

# # Splitting the downloaded data into separate DataFrames
# adj_close_df = data['Adj Close']
# close_df     = data['Close']
# high_df      = data['High']
# low_df       = data['Low']
# open_df      = data['Open']
# volume_df    = data['Volume']
 
# # Printing the separate DataFrames
# print("Adj Close:"); print(adj_close_df.round(2))
# print("\nClose:");   print(close_df.round(2))
# print("\nHigh:");    print(high_df.round(2))
# print("\nLow:");     print(low_df.round(2))
# print("\nOpen:");    print(open_df.round(2))
# print("\nVolume:");  print(volume_df)

# Create a MultiIndex from the columns
data.columns = data.columns.swaplevel(0, 1)
data.sort_index(axis=1, level=0, inplace=True)

#convert all datacolumns as float
cols = data.columns
for col in cols:
    data[col] = data[col].astype(float)

# Split the data based on symbols
symbol_dfs = {}
for symbol in symbols:
    # Create a copy of the DataFrame
    symbol_dfs[symbol] = data[symbol].copy()  
    # Divide 'Volume' column by 1000
    symbol_dfs[symbol]['Volume'] /= 1
    #symbol_dfs[symbol] = symbol_dfs[symbol].round(0)

stock_data_df = pd.concat(symbol_dfs.values(), keys=symbol_dfs.keys())

#if want extract second name
stock_data_df = stock_data_df.rename_axis(['SYMBOL','TIMESTAMP'])
#rename columns
stock_data_df = stock_data_df.rename(columns={'Open': 'OPEN', 'High': 'HIGH', 'Low': 'LOW', 'Close': 'CLOSE', 'Adj Close': 'PREVCLOSE', 'Volume': 'TOTTRDQTY'})

#remove blanks
stock_data_df.dropna(inplace=True)

#updated to capture the index and index rename
stock_data_df.to_csv(path+"ftse_download.csv", index=True, encoding='utf-8-sig')
