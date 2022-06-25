#!/usr/bin/env python
# coding: utf-8

# In[81]:


#Import data and remove duplicate data
import pandas as pd
data = pd.read_csv(r'shenzhenSCD.csv',encoding = 'gb2312').dropna()
data = data.drop_duplicates()
data


# In[82]:


#Remove bus data
data1 = data[data['deal_type'] == '地铁入站']
data2 = data[data['deal_type'] == '地铁出站']
t_1 = pd.DataFrame(data1)
t_2 = pd.DataFrame(data2)
data = pd.concat([t_1,t_2])
data


# In[83]:


r = data['deal_date'].iloc[0]
#Separate date and time
data['date'] = data['deal_date'].apply(lambda r:r[:(r.find(' ')+1)])
data['time'] = data['deal_date'].apply(lambda r:r[(r.find(' ')+1):])
data


# In[84]:


#subway data on August 31
data1 = data[data['date'] == '2018-08-31 ']
data1 = data1.sort_values(by = ['card_no','time'])
data1


# In[85]:


#subway data on September 1
data2 = data[data['date'] == '2018-09-01 ']
data2 = data2.sort_values(by = ['card_no','time'])
data2


# In[86]:


#Remove some useless columns
data2 = data2[['card_no','date','time','deal_value','deal_money','company_name','station']]
data2


# In[87]:


#Pan table up one row
for col in data2.columns:
    data2[col+'1'] = data2[col].shift(-1)
    print(col)
data2


# In[88]:


#Remove data that card_no ID is not equal to card_no1 ID
data2 = data2[data2['card_no'] == data2['card_no1']]
data2


# In[89]:


#Found data with inbound amount 0 and outbound amount not 0
data2 = data2[(data2['deal_money'] == 0)&(data2['deal_money1'] > 0)]
data2


# In[90]:


#Change the order of columns
data2 = data2[['card_no','date','time','company_name','station','time1','company_name1','station1','deal_value1','deal_money1']]
data2


# In[91]:


#Change column name
data2.columns = ['ID','date','stime','sline','sstation','etime','eline','estation','deal_value','deal_money']
data2


# In[92]:


#Find travel hours
data2['hour'] = data2['stime'].apply(lambda r:r[:(r.find(':'))])
data2


# In[93]:


#Because I don't know how to use code to process the Chinese in the table on the Jupiter notebook, 
#I export the above table, and then in Excel, I change some Chinese in sstation and estation so that they can correspond to the Chinese in station_gps.
data2 = pd.read_csv(r'data2_od.csv',encoding = 'GB18030')
data2


# In[94]:


#Check how many people travel per hour according to card ID
data2.groupby(['hour'])['ID'].count().rename('Travel aggregation').reset_index()


# In[95]:


#Check how many people depart from sstation to estation in each time period according to the card ID
od = data2.groupby(['hour','sstation','estation'])['ID'].count().rename('Travel aggregation').reset_index()
od


# In[96]:


#Import GPS data of Shenzhen subway Station
station_gps = pd.read_excel(r'stop.xlsx')
station_gps = station_gps.drop_duplicates(subset = ['st_name'])
station_gps


# In[97]:


station_gps =station_gps[['st_name','wgs84_lng','wgs84_lat']]
station_gps


# In[98]:


#Add GPS data of sstation and estation
data = od
station_gps.columns = ['sstation','slon','slat']
data = pd.merge(data,station_gps)
station_gps.columns = ['estation','elon','elat']
data = pd.merge(data,station_gps)
data


# In[ ]:




