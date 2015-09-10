# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:13:47 2015

@author: pdougherty

This script was used to create the master CSV file found in this repository. As the US Census Bureau updates its Housing Vacancies and Homeownership survey, it may be used to reformat the data for plotting and use.
If you read the associated CSV into pandas, only the plotHomeownership(msa) function will be relevant.

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
    
def plotHomeownerRates(df, msa, us=True, save=False, filepath=''):
    '''
    params:
        - df: dataframe of metropolitan regions
        - msa: list-like, names of principal cities within metro areas
        - us: if us==True, plot US homeownership rate
        - save: save the plot
        - filepath: if save is passed, a filepath, name, and extension must be specified
    '''

    fig, ax=plt.subplots()
    for m in msa:
        ax.plot(df[df.MSA==m].period, df[df.MSA==m].Rate, label=m)
    if us==True:
    us = pd.read_csv('https://raw.githubusercontent.com/pjdougherty/Homeownership/master/us%20and%20regions_homeownership.csv')
    us = us[us.Area=='United States']
    ax.plot(us[us.Year>=2005].dt, us[us.Year>=2005].Rate, label='US', c='#363737', alpha=0.3)
    
    labels = ax.get_yticks().tolist()
    labels = [str(l)+'%' for l in labels]
    ax.set_yticklabels(labels)
    
    plt.ylabel('Percent of Residents')
    plt.legend(loc=0)
    
    plt.title('Homeownership Rate')
    
    if save==True:
	if filepath=='':
            print 'Filepath must be specified with name and extension.'
        else:
            plt.savefig(filepath, bbox_inches='tight', dpi=600, alpha=True)
    
    return fig

''' Read in and transform the raw Census Bureau data '''
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

