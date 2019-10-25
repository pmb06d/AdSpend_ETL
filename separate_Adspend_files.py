# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 10:31:09 2019

@author: pbonnin
"""


def avail_years():
    import os
    directory = 'R:/Cinemax Research/Ad Sales/Ad-Spend/Raw'
    file_list = os.listdir(directory)
    accept = [file for file in file_list if file.endswith('.csv')]
    return(list(set([file[:7][3:7].strip() for file in accept])))
        
def avail_months():
    import os
    directory = 'R:/Cinemax Research/Ad Sales/Ad-Spend/Raw'
    file_list = os.listdir(directory)
    accept = [file for file in file_list if file.endswith('.csv')]
    return(list(set([file[:3].strip() for file in accept])))
  
    
def get_year():
    check = avail_years()
    while True:
        year = input('\n'+'Enter the year:')
        if len(year) == 4:
            if year in check:
                try:
                    int(year)
                    break
                except:
                    print('\n','Please enter a number')
            else:
                print('\n','Year not available','\n',sep='')                
        else:
            print('\n','Please enter a 4 digit number','\n',sep='')
    return(int(year))
    

def get_month():
    # a list of months to check againt
    #check = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    check = avail_months()
    
    while True:
        month = input('\n'+'Enter the first three letters of the month:')
        if len(month) == 3:
            if month.upper() in check:
                break
            else:
                print('\n','Invalid or non-available month','\n',sep='')
        else:
            print('\n','Please enter only the first three letters of the month','\n',sep='')
    return(month.upper())


def main(month,year):

    import pandas as pd
    import time
    
    start_time = time.time()
    
    month = str(month).upper()
    year = int(year)
    
    #month = 'MAY'
    #year = 2019
    
    current_month = month.upper()+str(year)
    
    file = 'R:/Cinemax Research/Ad Sales/Ad-Spend/Raw/'+current_month+'.csv'
    
    master_df = pd.read_csv(file,encoding='utf-16', sep ='\t')
    
    market_list = list(master_df['Market'].unique())
    
    current_month2 = month.capitalize()+' '+str(year)
    
    master_df['MONTH/YEAR'] = current_month2
    
    columns = ['Market',
               'MONTH/YEAR',
             'Sector',
             'Brand',
             'Product',
             'Advertiser',
             'Channel',
             'Type of Spot',
             'Agency',
             'Sum(Local Currency)',
             'Sum(USD $)',
             'Sum(# Spots)']
             
             
    columns_expt = ['Sector',
                 'Brand',
                 'Product',
                 'Advertiser',
                 'Channel',
                 'Type of Spot',
                 'Agency',
                 'Sum(Local Currency)',
                 'Sum(USD $)',
                 'Sum(# Spots)']
    
    
    master_df = master_df.loc[:,columns]
    
    for market in market_list:
        output = 'R:/Cinemax Research/Ad Sales/Ad-Spend/Monthly Exports/'+market+'/'+str(year)+'/'+current_month+'.csv'
        temp_df = master_df.loc[master_df['Market']==market,columns_expt]
        temp_df.columns = temp_df.columns.str.upper()
        temp_df.to_csv(path_or_buf=output,index=False, sep=',')
    
    master_df['Market'] = master_df['Market'].str.upper()
    output2 = 'R:/Cinemax Research/Ad Sales/Ad-Spend/Raw/Processed/'+current_month+'_v2.csv'
    master_df.to_csv(path_or_buf=output2,index=False, sep=',')
    
    print('\n','Your ouput is ready: ',output2,sep='')
    print('Time: %s seconds' % (time.time() - start_time),'\n',sep='')

if __name__== "__main__":
  main(get_month(),get_year())