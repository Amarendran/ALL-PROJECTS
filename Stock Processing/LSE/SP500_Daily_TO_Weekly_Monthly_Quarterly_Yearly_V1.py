# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 13:10:19 2019

Converting teh daily bhav to weekly monthly quarterly yearly
Create Weekly, monthly,Quarter & Yearly stock

reference website
https://www.techtrekking.com/how-to-convert-daily-time-series-data-into-weekly-and-monthly-using-pandas-and-python/

@author: eamalok
"""

import os
import glob
import pandas as pd
import numpy as np
#import datetime
import time

starttime=time.time()

#Defining rolling function
def get_rolling(group, freq, testa,funct):
    if funct == 'mean':
        return group.rolling(freq, on='TIMESTAMP',min_periods=1)[testa].mean()
    elif funct == "max":
        return group.rolling(freq, on='TIMESTAMP',min_periods=1)[testa].max()
    elif funct == 'min':
        return group.rolling(freq, on='TIMESTAMP',min_periods=1)[testa].min()
    elif funct == 'sum':
        return group.rolling(freq, on='TIMESTAMP',min_periods=1)[testa].sum()
    elif funct == 'std':
        return group.rolling(freq, on='TIMESTAMP',min_periods=1)[testa].std()
    elif funct == 'count':
        return group.rolling(freq, on='TIMESTAMP',min_periods=1)[testa].count()
    else :
        return 0

##Main code
#os.chdir("C:/nse_download/history/download/run3")
#path='C:/Users/eamalok/Desktop/POWER  BI/Python coding/jupyter_test/'
os.chdir("D:/nse_download/download")
path='D:/nse_download/Weekly/'
path_readcsv='D:/nse_download/ftse_sp_download/'
path2='D:/nse_download/Parsed_Output/'
#os.getcwd()

combined_csv=pd.read_csv(path_readcsv+"sp500_download.csv")
#combined_csv=pd.read_csv(path+"sp500_download.csv")
print(combined_csv)
#combined_csv=combined_csv.iloc[:,:-1]
combined_csv['TIMESTAMP'] = pd.to_datetime(combined_csv['TIMESTAMP'])
combined_csv = combined_csv.sort_values(by='TIMESTAMP', ascending=True)
combined_csv=combined_csv.reset_index(drop=True)

#Logic for aggregation
logic = {'TIMESTAMP': 'first',
         'OPEN'  : 'first',
         'HIGH'  : 'max',
         'LOW'   : 'min',
         'CLOSE' : 'last',
         'PREVCLOSE': 'first',
         'TOTTRDQTY': 'sum'}


combined_csv['Year'] = combined_csv['TIMESTAMP'].apply(lambda x: str(x.year))
combined_csv['quarter'] = combined_csv['TIMESTAMP'].apply(lambda x: str(x.year)+"_"+str("{0:0=2d}".format(x.quarter)))
combined_csv['Month'] = combined_csv['TIMESTAMP'].apply(lambda x: str(x.year)+"_"+str("{0:0=2d}".format(x.month)))
#combined_csv['Week_Number'] = combined_csv['TIMESTAMP'].apply(lambda x: str(x.year)+"_"+str("{0:0=2d}".format(x.weekofyear)))
combined_csv["YearWeek"] = combined_csv['TIMESTAMP'].apply(lambda x: x.strftime("%W")) #%W for monday start week, %U for sunday start week
combined_csv["YearWeekITU"] = combined_csv['TIMESTAMP'].apply(lambda x: x.weekofyear)

print("STP1")
combined_csv['YearForWeekNo']=np.where(combined_csv['YearWeek'].astype(int)>combined_csv['YearWeekITU'], combined_csv['Year'].astype(int)+1, np.where((combined_csv['YearWeek'].astype(int)+15)<combined_csv['YearWeekITU'], combined_csv['Year'].astype(int)-1,combined_csv['Year']))
print("STP2")
combined_csv['Week_Number'] = combined_csv['YearForWeekNo'].astype(str)+"_"+combined_csv["YearWeekITU"].astype(str).str.zfill(2)
a=combined_csv
print("STP3")
combined_csv.drop(columns=['YearWeek','YearWeekITU','YearForWeekNo'],inplace=True)

#combined_csv['TIMESTAMP'].dt.week
#combined_csv['TIMESTAMP'].dt.month
#combined_csv['TIMESTAMP'].dt.year

#REF:df = df.groupby(['Year','Week_Number']).agg({'Open Price':'first', 'High Price':'max', 'Low Price':'min', 'Close Price':'last','Total Traded Quantity':'sum'})
combined_csv_Week = combined_csv.groupby(['SYMBOL','Week_Number']).agg(logic)
print("STP2")
combined_csv_Month = combined_csv.groupby(['SYMBOL','Month']).agg(logic)
combined_csv_quarter = combined_csv.groupby(['SYMBOL','quarter']).agg(logic)
combined_csv_Year = combined_csv.groupby(['SYMBOL','Year']).agg(logic)
combined_csv_Week=combined_csv_Week.reset_index()
combined_csv_Month=combined_csv_Month.reset_index()
combined_csv_quarter=combined_csv_quarter.reset_index()
combined_csv_Year=combined_csv_Year.reset_index()

Week_Range=combined_csv['Week_Number'].iloc[0]+"_to_"+combined_csv['Week_Number'].iloc[-1]
Month_Range=combined_csv['Month'].iloc[0]+"_to_"+combined_csv['Month'].iloc[-1]
Quarter_Range=combined_csv['quarter'].iloc[0]+"_to_"+combined_csv['quarter'].iloc[-1]
Year_Range=combined_csv['Year'].iloc[0]+"_to_"+combined_csv['Year'].iloc[-1]

#combined_csv_Week.to_csv(path+"sp500_combined_csv_Week_"+Week_Range+".csv", index=False, encoding='utf-8-sig')
#combined_csv_Month.to_csv(path+"sp500_combined_csv_Month_"+Month_Range+".csv", index=False, encoding='utf-8-sig')
#combined_csv_quarter.to_csv(path+"sp500_combined_csv_Quarter_"+Quarter_Range+".csv", index=False, encoding='utf-8-sig')
#combined_csv_Year.to_csv(path+"sp500_combined_csv_Year_"+Year_Range+".csv", index=False, encoding='utf-8-sig')

combined_csv_Week.to_csv(path2+"sp500_combined_csv_Week.csv", index=False, encoding='utf-8-sig')
combined_csv_Month.to_csv(path2+"sp500_combined_csv_Month.csv", index=False, encoding='utf-8-sig')


Endtime=time.time()

print("Starttime:",starttime,"\n","Endtime:",Endtime,"\n","DeltatimeSec:",Endtime-starttime,"\n","DeltatimeMin:",(Endtime-starttime)/60)

#combined_csv[combined_csv['SYMBOL']=="3MINDIA"].to_csv(path+"combined_3M_TEST_csv_Year_V2_"+Year_Range+".csv", index=False, encoding='utf-8-sig')
