# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 16:53:16 2019

@author: pbonnin
"""


#%%

import os
import pandas as pd
import time
from fuzzywuzzy import process

pd.options.display.max_columns = 20

#%%

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = []
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles        
 
 
dirName = 'R:/Cinemax Research/Ad Sales/Ad-Spend\Monthly Exports'
    
# Get the list of all files in directory tree at given path
listOfFiles = getListOfFiles(dirName)
    
# Get the list of all files in directory tree at given path
listOfFiles = []
for (dirpath, dirnames, filenames) in os.walk(dirName):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

# a function to get country and month from the filename
def parse_dir(filename):
    fields = filename.replace('.csv','').split('\\')
    region = fields[-3]
    year = fields[-2]
    month = fields[-1].replace(year,'')
    date = month.title() + ' ' + year
    return(region, date)


## A function to match the names 
def match(list_a, list_b, a_name='Main', b_name='Matcher', score=95, print_nonmatch=False, export_nonmatch=False):
    
    # some lists to compile information
    matched_list = []
    non_matches = []
    team_name = []
    similarity_score = []
    
    # go through the main list and get the best match (only scores above the given number or 95 by default)
    for i in list_a:
        matched_list.append(process.extractOne(i, list_b, score_cutoff=score))
    
    # fuzzy wuzzy likes to output a tuple with the match and the similarity score, append none if there is nothing in the row    
    for tup in matched_list:
        if tup==None:
            team_name.append(None)
            similarity_score.append(None)
        else:
            team_name.append(tup[0])
            similarity_score.append(tup[1])
    
    # Compile into a dataframe
    matched = pd.DataFrame(list(zip(list_a,matched_list,team_name,similarity_score)),columns= [a_name,str(b_name+"_(raw)"),str(b_name),str(b_name+"_Similarity")])
    matched = matched.set_index(a_name)
    
    # Compiling this name here makes it easier to index the DF ti print out a mtaching statement
    b_raw = str(str(b_name)+"_(raw)")
    print('\n',sum(matched[b_raw].value_counts()),"/ "+str(len(list_a)),"("+str(round(sum(matched[b_raw].value_counts())/len(list_a),2)*100)+"%)",'matches','\n')
    
    # compile non-matches in case the user wants to see them
    non_matches = matched.reset_index()
    non_matches = list(non_matches.loc[non_matches[str(b_name+"_Similarity")].isna(),a_name])
    matched = matched.loc[matched[str(b_name+"_Similarity")].notna(),]
            
     # print the non-matches if the parameter is given
    if print_nonmatch == True:
        print("--->",str(len(non_matches))+" non-matching item(s):")
        for i in non_matches:
            print(i)
    
    if export_nonmatch == True:
        return(matched,non_matches)
    else:
        return(matched)


#%%
    
# Remove all the files that are not csv's
    
accept = []
reject = []

for elem in listOfFiles:
    if elem.endswith('.csv'):
        accept.append(elem)
    else:
        reject.append(elem)

#%% Field dictionary
        
keys = ['SECTOR',
             'BRAND',
             'PRODUCT',
             'ADVERTISER (2)',
             'CHANNEL',
             'TYPE OF SPOT',
             'AGENCY',
             'Sum(COSTO MONEDA LOCAL TOTAL)',
             'Sum(US$)',
             'Sum(# SPOTS)',
             'MARKET',
             'MONTH/YEAR',
             'Sum(LOCAL CURRENCY)',
             'ADVERTISER',
             'SUM(LOCAL CURRENCY)',
             'SUM(USD $)',
             'SUM(# SPOTS)',
             'Sum(US CURRENCY)',
             'Sum(NUMBER OF SPOTS)']
        
values = ['SECTOR',
             'BRAND',
             'PRODUCT',
             'ADVERTISER',
             'CHANNEL',
             'TYPE OF SPOT',
             'AGENCY',
             'SUM(LOCAL CURRENCY)',
             'SUM(US$)',
             'SUM(# SPOTS)',
             'MARKET',
             'MONTH/YEAR',
             'SUM(LOCAL CURRENCY)',
             'ADVERTISER',
             'SUM(LOCAL CURRENCY)',
             'SUM(US$)',
             'SUM(# SPOTS)',
             'SUM(US$)',
             'SUM(# SPOTS)']

dictionary = dict(zip(keys, values))  

#%%
start_time = time.time()

df_list = []

for filename in accept:
    try:
        df = pd.read_csv(filename,encoding='latin1')
    except:
        df = pd.read_csv(filename,encoding='utf-16', sep ='\t')
    region, date = parse_dir(filename)
    df['MARKET'] = region
    df['MONTH/YEAR'] = date
    df.rename(columns = dictionary, inplace = True)
    df_list.append(df)

current_adspend = pd.concat(df_list, sort=False)

current_adspend = current_adspend.loc[current_adspend['SECTOR']!='Grand total',]

output = '//svrgsursp5/FTP/DOMO/Data/Current_Adspend.csv'
current_adspend.to_csv(path_or_buf=output, sep=',')

print('Time: %s seconds' % (time.time() - start_time),'\n',sep='')

#%%

avertisers = pd.read_csv('//svrgsursp5/FTP/DOMO/Data/Advertisers.csv',encoding='latin1')
channels = pd.read_csv('//svrgsursp5/FTP/DOMO/Data/Channels.csv',encoding='latin1')
sectors = pd.read_csv('//svrgsursp5/FTP/DOMO/Data/Sectors.csv',encoding='latin1')


compare_advertiser = list(avertisers.loc[avertisers['Advertiser '].notna(),'Advertiser '].unique())
compare_channel = list(channels.loc[channels['CHANNEL'].notna(),'CHANNEL'].unique())
compare_sector = list(sectors.loc[sectors['Sector'].notna(),'Sector'].unique())

current_channels_nm = list(channels.loc[channels['CHANNEL (CLEAN)'].notna(),'CHANNEL (CLEAN)'].unique())

#%%

current_advertisers = list(current_adspend['ADVERTISER'].unique())
current_channels = list(current_adspend['CHANNEL'].unique())
current_sectors = list(current_adspend['SECTOR'].unique())

present_periods = list(current_adspend['MONTH/YEAR'].unique())

#%% Check if there are new values

def check_advertiser():
    new_advertisers = []
    for i in current_advertisers:
        if i not in compare_advertiser:
            new_advertisers.append(i)
        else:
            continue
    
    if len(new_advertisers) == 0:
        print('All advertisers are accounted for')
    else:
        print(str(len(new_advertisers)),'new advertisers found','\n')
        return([i for i in new_advertisers if str(i) != 'nan'])

        
def check_channel():
    new_channels = []
    for i in current_channels:
        if i not in compare_channel:
            new_channels.append(i)
        else:
            continue
    
    if len(new_channels) == 0:
        print('All channels are accounted for')
    else:
        print(str(len(new_channels)),'new channels found','\n')
        return([i for i in new_channels if str(i) != 'nan'])

        
def check_sector():
    new_sectors = []
    for i in current_sectors:
        if i not in compare_sector:
            new_sectors.append(i)
        else:
            continue
    
    if len(new_sectors) == 0:
        print('All sectors are accounted for')
    else:
        print(str(len(new_sectors)),'new sectors found','\n')
        return([i for i in new_sectors if str(i) != 'nan'])



def avail_channels(check = current_channels_nm):
    check = sorted([i.upper() for i in check])
    while True:
        name = input('Type the normalized channel name (you can type DISPLAY to show available names): ')
        if name.upper() in check:
            break
        elif name.lower() == 'display':
            print(check)
            continue
        elif name.lower() == 'new':
            while True:
                name = input('Type the new channel name (you can type DISPLAY to show available names): ')
                if name == 'display':
                    print(check)
                    continue
                else:
                    break
            break
        elif name.lower() == 'quit':
            break
        else:
            print('Invalid or non-available channel (you can type NEW if channel does not match the DISPLAY list)',sep='')
            continue
    return(name.upper())
    

def normalizer(input_statement):
    while True:
        get = input(input_statement)
        if get.upper() == 'Y':
            break
        elif get.upper() == 'N':
            break
        else:
            print('Please enter only Y or N')
            continue
    return(get.upper())

#%%
        
new_advertisers = check_advertiser()

new_channels = check_channel()

new_sector = check_sector()


#%%

def identify_channels(score=80):
    fuzzy_match, no_match = match(new_channels,current_channels_nm, score=score,export_nonmatch=True)
    
    fuzzy_match = fuzzy_match.loc[fuzzy_match['Matcher_Similarity'].notna(),].reset_index()
    
    # evaluate channel matches
    original = []
    confirmed = []
    group = []

    for i in range(len(fuzzy_match)):
        if fuzzy_match.iloc[i,3] >= 95:
            original.append(fuzzy_match.iloc[i,0])
            confirmed.append(fuzzy_match.iloc[i,2])
        else:
            input_statement = 'Confirm match: '+fuzzy_match.iloc[i,0]+'--> '+fuzzy_match.iloc[i,2]+' (Y/N): '
            if normalizer(input_statement) == 'Y':
                original.append(fuzzy_match.iloc[i,0])
                confirmed.append(fuzzy_match.iloc[i,2])
            else:
                original.append(fuzzy_match.iloc[i,0])
                confirmed.append(avail_channels())

    if len(no_match) > 0:
        if normalizer('There are '+str(len(no_match))+' channel(s) with no match. Would you like to identify them now? (Y/N): ') == 'Y':
            for channel, i in zip(no_match, [i for i in range(len(no_match))]):
                original.append(channel)
                print('\n','For ::: ',channel,' :::',sep='')
                confirmed.append(avail_channels())

    for name in confirmed:
        try:
            group.append(list(channels.loc[channels['CHANNEL (CLEAN)']==name,'CHANNEL (GROUP)'])[0])
        except:
            group.append('No match')
        
    return(pd.DataFrame(list(zip(original,confirmed,group)),columns=['CHANNEL','CHANNEL (CLEAN)','CHANNEL (GROUP)']))
        

def insert_newchannels():
    norm_channels =  identify_channels()
    if len(norm_channels) > 0:
        norm_channels.to_csv('//svrgsursp5/FTP/DOMO/Data/Channels.csv', mode='a', header=False, index=False)
    else:
        print('No new channels to append')

#%%
        
identify_channels()

#%%
        
def identify_sectors(score=80):
    fuzzy_match, no_match = match(new_channels,current_channels_nm, score=score,export_nonmatch=True)
    
    fuzzy_match = fuzzy_match.loc[fuzzy_match['Matcher_Similarity'].notna(),].reset_index()
    
    # evaluate channel matches
    original = []
    confirmed = []
    group = []

    for i in range(len(fuzzy_match)):
        if fuzzy_match.iloc[i,3] >= 95:
            original.append(fuzzy_match.iloc[i,0])
            confirmed.append(fuzzy_match.iloc[i,2])
        else:
            input_statement = 'Confirm match: '+fuzzy_match.iloc[i,0]+'--> '+fuzzy_match.iloc[i,2]+' (Y/N): '
            if normalizer(input_statement) == 'Y':
                original.append(fuzzy_match.iloc[i,0])
                confirmed.append(fuzzy_match.iloc[i,2])
            else:
                original.append(fuzzy_match.iloc[i,0])
                confirmed.append(avail_channels())

    if len(no_match) > 0:
        if normalizer('There are '+str(len(no_match))+' channel(s) with no match. Would you like to identify them now? (Y/N): ') == 'Y':
            for channel, i in zip(no_match, [i for i in range(len(no_match))]):
                original.append(channel)
                print('\n','For ::: ',channel,' :::',sep='')
                confirmed.append(avail_channels())

    for name in confirmed:
        try:
            group.append(list(channels.loc[channels['CHANNEL (CLEAN)']==name,'CHANNEL (GROUP)'])[0])
        except:
            group.append('No match')
        
    return(pd.DataFrame(list(zip(original,confirmed,group)),columns=['CHANNEL','CHANNEL (CLEAN)','CHANNEL (GROUP)']))
        

def insert_newsectors():
    norm_channels =  identify_channels()
    if len(norm_channels) > 0:
        norm_channels.to_csv('//svrgsursp5/FTP/DOMO/Data/Channels.csv', mode='a', header=False, index=False)
    else:
        print('No new channels to append')
        
