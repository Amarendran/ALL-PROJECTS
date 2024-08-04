# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:33:44 2020

@author: eamalok

Script to get the F&O Trend Call & Put Summation for a given day

idea to create a "Sum of OI, Delta OI" for option CE, PE and futures in a stock regardless of expiry date

"""


import os
import glob
import pandas as pd
#import numpy as np
#import datetime
import time

starttime=time.time()

##Main code
os.chdir("D:/nse_download/fo_download/run2")  #run2 #2018-2020
path='D:/nse_download/Parsed_Output/'
#os.getcwd()

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames],sort=False)

#drop all unused columns
combined_csv.drop(combined_csv.columns[combined_csv.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
combined_csv.drop(columns=['EXPIRY_DT','STRIKE_PR','OPEN','HIGH','LOW','CLOSE'],inplace=True)

#logic to clean optiontype
if 'OPTIONTYPE' in combined_csv.columns:
    combined_csv["OPTION_TYP"] = combined_csv['OPTION_TYP'].fillna(combined_csv['OPTIONTYPE'])
    combined_csv = combined_csv.drop('OPTIONTYPE', axis=1)
else:
    print("No column with OPTIONTYPE")

#date Cleanup and combinig the data
combined_csv['TIMESTAMP'] = pd.to_datetime(combined_csv['TIMESTAMP'])
combined_csv['Year'] = combined_csv['TIMESTAMP'].apply(lambda x: str(x.year))
combined_csv['FOMode'] = combined_csv['OPTION_TYP']
combined_csv=combined_csv[combined_csv.FOMode=='XX']

#Logic for aggregation for CE,PE & Future with seperate instrument
logic = {'CONTRACTS': 'sum',
         'VAL_INLAKH'  : 'sum',
         'OPEN_INT'  : 'sum',
         'CHG_IN_OI'   : 'sum'}

combined_csv_FO = combined_csv.groupby(['INSTRUMENT','SYMBOL','FOMode','TIMESTAMP','Year']).agg(logic)
combined_csv = combined_csv.groupby(['INSTRUMENT','SYMBOL','OPTION_TYP','TIMESTAMP']).agg(logic)

print("dataframe export")
combined_csv.to_csv(path+"combined_FO_Future_Day_Stock_Index.csv", encoding='utf-8-sig')
combined_csv_FO.to_csv(path+"combined_F&OSeries_Basefile.csv", encoding='utf-8-sig')

Endtime=time.time()

print("Starttime:",starttime,"\n","Endtime:",Endtime,"\n","DeltatimeSec:",Endtime-starttime,"\n","DeltatimeMin:",(Endtime-starttime)/60)
