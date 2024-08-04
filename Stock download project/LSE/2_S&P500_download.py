# Import packages
import yfinance as yf
import pandas as pd
import os

os.chdir("D:/nse_download/ftse_sp_download")
path='D:/nse_download/ftse_sp_download/'

# Read and print the stock tickers that make up S&P500
SP_500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
#print(SP_500.head())
#print(SP_500.Symbol)
#string = '.L'
#SP_500_list = [x + string for x in SP_500.Ticker.to_list()]
SP_500_list = SP_500.Symbol.to_list()

# Read and print the stock tickers that make up FTSE100
#FTSE_100 = pd.read_html('https://en.wikipedia.org/wiki/FTSE_100_Index')[4]
#print(FTSE_100.head())
#print(FTSE_100.Ticker)
#string = '.L'
#FTSE_100_list = [x + string for x in FTSE_100.Ticker.to_list()]

# Read and print the stock tickers that make up FTSE250
#FTSE_250 = pd.read_html('https://en.wikipedia.org/wiki/FTSE_250_Index')[3]
#print(FTSE_250.head())
#print(FTSE_250.Ticker)
#string = '.L'
#FTSE_250_list = [x + string for x in FTSE_250.Ticker.to_list()]

#symbols = SP_500_list + FTSE_100_list + FTSE_250_list
symbols = SP_500_list
#print(symbols)

#data = yf.download(symbols, start='2022-12-01', end  ='2022-12-06')
#data = yf.download(symbols, start='2024-06-01')
#print(data.head())
#df = data.stack().reset_index().rename(index=str, columns={"level_1": "Symbol"}).sort_values(['Symbol','Date'])
#df.set_index('Date', inplace=True)
#print(df.head())
#df.to_csv(path+"sp500_download.csv", index=False, encoding='utf-8-sig')

#similar to LSE_Download
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
stock_data_df.to_csv(path+"sp500_download.csv", index=True, encoding='utf-8-sig')
