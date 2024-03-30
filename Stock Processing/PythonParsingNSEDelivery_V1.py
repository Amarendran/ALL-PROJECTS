# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 14:08:38 2019

@author: eamalok
"""

import os
import glob
import pandas as pd
import numpy as np
import datetime

#Defining rolling function
def get_rolling(group, freq, testa,funct):
    if funct == 'mean':
        return group.rolling(freq, on='Date',min_periods=1)[testa].mean()
    elif funct == "max":
        return group.rolling(freq, on='Date',min_periods=1)[testa].max()
    elif funct == 'min':
        return group.rolling(freq, on='Date',min_periods=1)[testa].min()
    elif funct == 'sum':
        return group.rolling(freq, on='Date',min_periods=1)[testa].sum()
    elif funct == 'std':
        return group.rolling(freq, on='TIMESTAMP',min_periods=1)[testa].std()
    elif funct == 'count':
        return group.rolling(freq, on='Date',min_periods=1)[testa].count()
    else :
        return 0

##Main code
os.chdir("C:/nse_download/download_withdelivery")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

##To save the combined file to Specific folder
path='C:/nse_download/Parsed_Output/'
combined_csv.to_csv(path+"combined_delivery_csv.csv", index=False, encoding='utf-8-sig')

#to save one company
combined_csv[(combined_csv['Name of Security']=='3MINDIA') ].to_csv(path+"3mindia_combined_delivery_csv.csv", index=False, encoding='utf-8-sig')

##read the combined file
#EQDeliveryData=pd.read_csv(path+"combined_delivery_csv.csv")
EQDeliveryData=combined_csv

EQDeliveryData=EQDeliveryData[EQDeliveryData.SERIES=='EQ']

##converting the data into time series and creating the week number and sorting wrt date
EQDeliveryData['Date'] = pd.to_datetime(EQDeliveryData['Date'])
EQDeliveryData['Week_Number'] = EQDeliveryData['Date'].apply(lambda x: str(x.year)+"_"+str("{0:0=2d}".format(x.weekofyear)))
#SData['Week_Number'] = SData['Date'].apply(lambda x: x.weekofyear)
EQDeliveryData = EQDeliveryData.sort_values(by='Date', ascending=True)


#EQDeliveryData[(EQDeliveryData['Name of Security']=='3MINDIA') ].head(300)
#EQDeliveryData[(EQDeliveryData['Name of Security']=='3MINDIA') | (EQDeliveryData['Name of Security']=='ABCAPITAL')].head(300)


##delivery percentage
EQDeliveryData['1DDMA']=EQDeliveryData['% of Deliverable Quantity']
EQDeliveryData["3DDMA_Den"]=EQDeliveryData.groupby("Name of Security",as_index=False,group_keys=False).apply(get_rolling,3,"Quantity Traded","sum")
EQDeliveryData['3DDMA_Num']=EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,3,'Deliverable Quantity','sum')
EQDeliveryData['3DDMA1']=100*EQDeliveryData['3DDMA_Num']/EQDeliveryData['3DDMA_Den']

EQDeliveryData['3DDMA']=100*EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,3,'Deliverable Quantity','sum')/EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,3,'Quantity Traded','sum')
EQDeliveryData['5DDMA']=100*EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,5,'Deliverable Quantity','sum')/EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,5,'Quantity Traded','sum')
EQDeliveryData['8DDMA']=100*EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,8,'Deliverable Quantity','sum')/EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,8,'Quantity Traded','sum')
EQDeliveryData['13DDMA']=100*EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,13,'Deliverable Quantity','sum')/EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,13,'Quantity Traded','sum')
EQDeliveryData['21DDMA']=100*EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,21,'Deliverable Quantity','sum')/EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,21,'Quantity Traded','sum')
EQDeliveryData['50DDMA']=100*EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,50,'Deliverable Quantity','sum')/EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,50,'Quantity Traded','sum')
EQDeliveryData['100DDMA']=100*EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,100,'Deliverable Quantity','sum')/EQDeliveryData.groupby('Name of Security',as_index=False,group_keys=False).apply(get_rolling,100,'Quantity Traded','sum')

##Bulishcriteria
#EQDeliveryData['Bullish_Mov']=np.where(np.logical_and(np.logical_and(EQDeliveryData['1DDMA']>=EQDeliveryData['3DDMA'],EQDeliveryData['3DDMA']>=EQDeliveryData['5DDMA'],EQDeliveryData['5DDMA']>=EQDeliveryData['8DDMA']),np.logical_and(EQDeliveryData['8DDMA']>=EQDeliveryData['13DDMA'],EQDeliveryData['13DDMA']>=EQDeliveryData['21DDMA'],EQDeliveryData['21DDMA']>=EQDeliveryData['50DDMA']),EQDeliveryData['50DDMA']>=EQDeliveryData['100DDMA']), 1, 0)
EQDeliveryData['1DDMA>3DDMA']=np.where(EQDeliveryData['1DDMA']>EQDeliveryData['3DDMA'], 1, 0)
EQDeliveryData['3DDMA>8DDMA']=np.where(EQDeliveryData['3DDMA']>EQDeliveryData['8DDMA'], 1, 0)
EQDeliveryData['8DDMA>13DDMA']=np.where(EQDeliveryData['8DDMA']>EQDeliveryData['13DDMA'], 1, 0)
EQDeliveryData['13DDMA>21DDMA']=np.where(EQDeliveryData['13DDMA']>EQDeliveryData['21DDMA'], 1, 0)
EQDeliveryData['21DDMA>50DDMA']=np.where(EQDeliveryData['21DDMA']>EQDeliveryData['50DDMA'], 1, 0)
EQDeliveryData['50DDMA>100DDMA']=np.where(EQDeliveryData['50DDMA']>EQDeliveryData['100DDMA'], 1, 0)
EQDeliveryData['BulishDelivery']=EQDeliveryData['1DDMA>3DDMA']+EQDeliveryData['3DDMA>8DDMA']+EQDeliveryData['8DDMA>13DDMA']+EQDeliveryData['13DDMA>21DDMA']+EQDeliveryData['21DDMA>50DDMA']+EQDeliveryData['50DDMA>100DDMA']

#Filtering the yesterday data with Bulishdelivery count 6 which is the MAX.
if pd.Timestamp('now').hour>=17:
    dayoffset=0
else :
    dayoffset=-1
RefDate=pd.Timestamp('today').date()+pd.DateOffset(days=dayoffset)

#save the last day data with calculated bulish delivery last 30days
EQDeliveryData[EQDeliveryData.Date > datetime.datetime.now()- pd.to_timedelta("30day")].to_csv(path+"combined_delivery_csv_processed_output_All.csv", index=False, encoding='utf-8-sig')
#EQDeliveryData[(EQDeliveryData['Date']==RefDate)].to_csv(path+"combined_delivery_csv_processed_output.csv", index=False, encoding='utf-8-sig')
#EQDeliveryData[(EQDeliveryData['BulishDelivery']>=5) &  (EQDeliveryData['Date']==RefDate) & (EQDeliveryData['Quantity Traded']>=100000) & (EQDeliveryData['1DDMA']>=40)].to_csv(path+"combined_delivery_csv_processed_output_pivort.csv", index=False, encoding='utf-8-sig')

