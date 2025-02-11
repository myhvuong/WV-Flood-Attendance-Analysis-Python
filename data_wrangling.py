# PPHA 30538
# Fall 2023
# Final Project

# mhvuong
# My Vuong


import os
import glob
import pandas as pd
import urllib.request, json 


PATH = r'/Users/macbook/Documents/GitHub/final-project-my-vuong/Data/'

### 1. DATA WRANGLING

## WORKING WITH PRECIPITATION DATA

def process_data(df_station):
    df_station = df_station[['DATE', 'PRCP']].copy()
    
    # Create a column that is 4 months later to more easily 
    # filter data that falls within a school year (September through May)
    df_station['LATERDATE'] = pd.to_datetime(df_station['DATE']) + pd.DateOffset(months=4)
    
    
    df_station['LATERDATE'] = pd.to_datetime(df_station['LATERDATE'])
    
    ### We need to filter months within a school year. Month 1-9 in the df would 
    # be Sep through May in real life
    df_station = df_station[df_station['LATERDATE'].dt.month.between(1, 9)]
    
    # We should now have data that falls within Sep 2005 and May 2023
    # Year 2006 in the df would represent school year 2005-2006
    df_station = df_station[df_station['LATERDATE'].dt.year.between(2004, 2023)] 
    
    
    df_station = df_station.drop('DATE', axis=1)
    
    # Get total annual precipitation for that station
    df_result = df_station.groupby(df_station['LATERDATE'].dt.year)['PRCP'].sum().reset_index()
    return df_result

def get_prcp_df(counties):
    county_data = {}
    
    for county in counties:
        county_path = os.path.join(PATH, 'Precipitation', county)

        # Get a list of csv file paths in a given county directory
        # Use glob library instead of os.listdir() b/c problems with .DS_Store files
        files = glob.glob(os.path.join(county_path, '*.csv'))
        
        # Need to initial an empty list to contain station dfs for each county
        county_data[county] = []
    
        for file_path in files:
            df_station = pd.read_csv(file_path, low_memory=False)
            df_station = process_data(df_station)
            county_data[county].append(df_station)
            
    dict_counties = {
        county: pd.concat(data).assign(COUNTY=county)
        for county, data in county_data.items()
    }


    df_prcp = pd.concat(dict_counties.values())
    df_prcp = df_prcp.groupby(['LATERDATE', 'COUNTY'])['PRCP'].mean().reset_index()
    df_prcp = df_prcp.rename(columns={'LATERDATE': 'year',
                                      'COUNTY': 'county',
                                      'PRCP': 'prcp'})
    return df_prcp



## WORKING WITH ATTENDANCE DATA

def get_attnd_df(counties):
    attnd_data = {}
    
    for county in counties:
        county_path = os.path.join(PATH, 'Attendance', county)
        files = glob.glob(os.path.join(county_path, '*.csv'))
        attnd_data[county] = []
        
        for file_path in files:
            df_partial_attnd = pd.read_csv(file_path, low_memory=False)
            attnd_data[county].append(df_partial_attnd)
            
    dict_attnd = {county: pd.concat(data).assign(COUNTY=county) for county, data in attnd_data.items()}
    
    df_attnd = pd.concat(dict_attnd.values())
    df_attnd = df_attnd.rename(columns={'School Year': 'school_year',
                             'Attnd %': 'attnd_rate',
                             'COUNTY': 'county'})
    
    df_attnd['year'] = df_attnd['school_year'].str.extract(r'(\d{4})')
    df_attnd = df_attnd[df_attnd['year'].astype(int).isin(range(2003, 2023))]
    df_attnd = df_attnd.drop('year', axis=1)
    
    df_attnd['attnd_rate'] = df_attnd['attnd_rate'].str.strip('%').astype(float)
    return df_attnd



## WORKING WITH FLOOD INCIDENTS DATA

def retrieve_json_data(url, fname, do_download=True):
    if not do_download:
        print('Skipping web download. Data is to be loaded from local file.')

    else:
        with urllib.request.urlopen(url) as url:
            fema_data = json.load(url)    
        df_fema = pd.json_normalize(fema_data['DisasterDeclarationsSummaries'])
        
        # Writing data from API call to file to minimize use of web resource
        df_fema.to_csv(os.path.join(PATH, 'FEMA', fname))
        print('Data downloaded and saved to the local file path.')
    
def load_fema_data(fname):
    df_fema = pd.read_csv(os.path.join(PATH, 'FEMA', fname))
    return df_fema

def process_fema_df(df_fema_1st, df_fema_2nd):
    df_fema_total = pd.concat([df_fema_1st, df_fema_2nd])
    df_fema = df_fema_total[df_fema_total['declarationTitle'].str.contains('FLOODING')].copy()
    df_fema['designatedArea'] = df_fema['designatedArea'].replace(' \(County\)', '', regex=True)
    df_fema = df_fema[df_fema['designatedArea'].isin(counties)]
    
    
    df_fema = df_fema[['fyDeclared', 'designatedArea', 'incidentBeginDate', 'incidentEndDate']]
    
    date_columns = ['incidentBeginDate', 'incidentEndDate']
    df_fema[date_columns] = df_fema[date_columns].apply(pd.to_datetime, format='%Y-%m-%d %H:%M:%S')
    df_fema[date_columns] = df_fema[date_columns] + pd.DateOffset(months=4)
    df_fema = df_fema[(df_fema['incidentBeginDate'].dt.month.between(1,9)) |
                      (df_fema['incidentEndDate'].dt.month.between(1,9))]
    
    df_fema = df_fema[df_fema['fyDeclared'].isin(range(2003, 2024))]
    
    
    df_fema['year'] = df_fema['incidentBeginDate'].dt.year
    
    df_fema = df_fema[['year', 'designatedArea']]
    
    final_df_fema = df_fema.groupby(['year', 'designatedArea']).size().reset_index(name='flood_count')
    final_df_fema = final_df_fema.rename(columns={'designatedArea': 'county'})
    return final_df_fema



## GETTING THE FINAL DATAFRAME

def merge_all(df_prcp, df_fema, df_attnd):
    prcp_flood = df_prcp.merge(df_fema, how='left', on=['county', 'year'])
    prcp_flood['flood_count'] = prcp_flood['flood_count'].fillna(0)
    prcp_flood['school_year'] = prcp_flood['year'].apply(lambda x: f'{x - 1}-{x}')
    prcp_flood = prcp_flood.drop('year', axis=1)
    
    df_final = prcp_flood.merge(df_attnd, how='outer', on=['school_year', 'county'])
    return df_final

def export_final_csv(df_final):
    df_final.to_csv(os.path.join(PATH, 'wv_flood_attnd.csv'), index=False)
    


counties = ['Cabell', 'Grant', 'Kanawha', 'Nicholas']

df_prcp = get_prcp_df(counties)

df_attnd = get_attnd_df(counties)

# Need to call twice because only 1,000 records are returned per API endpoint call
# There are 1,232 total records
url_1st_call = 'https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?$filter=state%20eq%20%27WV%27&$inlinecount=allpages&$skip=0'
url_2nd_call = 'https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries?$filter=state%20eq%20%27WV%27&$inlinecount=allpages&$skip=1000'

do_download = False
fema_data_1st = retrieve_json_data(url_1st_call, 'fema_1st_call.csv', do_download)
fema_data_2nd = retrieve_json_data(url_2nd_call, 'fema_2nd_call.csv', do_download)  

df_fema_1st = load_fema_data('fema_1st_call.csv')
df_fema_2nd = load_fema_data('fema_2nd_call.csv')

df_fema = process_fema_df(df_fema_1st, df_fema_2nd)


df_final = merge_all(df_prcp, df_fema, df_attnd)

export_final_csv(df_final)
