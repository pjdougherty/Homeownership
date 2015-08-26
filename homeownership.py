# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:13:47 2015

@author: pdougherty

This script was used to create the master CSV file found in this repository.
If you read the CSV into pandas, only the plotHomeownership(msa) function will be relevant. MSA names passed through should be the first city in the MSA name. For instance, to plot Baltimore-Towson-Columbia, MD MSA homeownership, use msa='Baltimore'.

Data from US Census Bureau's CPS/HVS Housing Vacancies and Homeownership survey and is available for the 75 largest US metros.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
                    
def transformDF(df):
    data = pd.DataFrame(columns=['drop'])  
    for c in list(df.columns.values):
        print c
        if '_Quarter_' in c:
           quarter = c.split('_')[0]
           year = c.split('_')[2]
           qy = pd.DataFrame([quarter]*len(df), columns=['Quarter']).join(pd.DataFrame([year]*len(df), columns=['Year']))
           
           d = df[['Metropolitan Statistical Area', c]].join(qy)
           
           d.rename(columns={c:'Rate', 'Metropolitan Statistical Area':'MSA'}, inplace=True)
           d = d.reset_index(drop=True)
           
           data = data.append(d)
           print len(data)
           
    data = data.reset_index(drop=True)
    data.Quarter = np.where(data.Quarter=='First', 2, data.Quarter)
    data.Quarter = np.where(data.Quarter=='Second', 5, data.Quarter)   
    data.Quarter = np.where(data.Quarter=='Third', 8, data.Quarter)
    data.Quarter = np.where(data.Quarter=='Fourth', 11, data.Quarter)
         
    df = data.join(pd.DataFrame(pd.to_datetime(data.Year.astype(str)+data.Quarter.astype(str), format='%Y%m'), columns=['period']))

    df.drop('drop', axis=1, inplace=True)
            
    return df

def shortNames(df):
    df['MSA'] = df.MSA.str.split(',').str.get(0)
    df['MSA'] = df.MSA.str.split('-').str.get(0)
    
    return df
    
def plotHomeownerRates(msa):
    fig, ax=plt.subplots()
    
    plt.plot(d[d.MSA==msa].period, d[d.MSA==msa].Rate, label=msa)
    
    labels = ax.get_yticks().tolist()
    labels = [str(l)+'%' for l in labels]
    ax.set_yticklabels(labels)
    
    plt.ylabel('Percent of Residents')
    
    plt.title('Homeownership Rate\n{}'.format(msa))
    
    plt.tight_layout()
    plt.show()
    
    return fig
''' Not needed for plotting '''
'''
df = {}
for y in range(2005,2016):
    df[str(y)[2:4]] = pd.read_excel(r'G:\Publications\Annual Regional Report\2015\Homeownership\homeownership_05to15.xlsx',
                                  sheetname='%s' % y, charset='utf8', use_unicode=True)

# Create a composite dataframe
d = df['15']
dz = pd.DataFrame(pd.to_datetime(df['15'].Year.astype(str)+df['15'].Quarter.astype(str), format='%Y%m'), columns=['period'])
d = df['15'].join(dz)
df_list = list(df)
df_list.remove('15')
for i in df_list:
    dz = transformDF(df[i])
    d = d.append(dz)
d.reset_index(drop=True, inplace=True)

# Double check to make sure all of the years are on here
d.Year.value_counts()

d = shortNames(d)
d = d.sort('period')
'''