# myhvuong
# My Vuong

### TEXT PROCESSING

from bs4 import BeautifulSoup
import requests
import re
import os

PATH = r'/Users/macbook/Documents/GitHub/final-project-my-vuong/Data/'

def extract_data(url, indices):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    html_str = str(soup)

    pattern = r'u003cstrong\\u003e(.*?)\\u003c'
    matches = re.findall(pattern, html_str)
    row = [matches[i] for i in indices]
    return row

def create_table(extracted_list):
    for sub_county_list in extracted_list:
        sub_county_list[0] = sub_county_list[0].replace(',', '')
        
    data_list = [','.join(sub_county_list) for sub_county_list in extracted_list]
    
    header = 'num_properties,perc_properties,county,risk_type'
    
    data_list.insert(0, header)
    doc = '\n'.join(data_list)
    
    file_path = os.path.join(PATH, 'risk_type.csv')
    with open(file_path, 'w') as ofile:
        ofile.write(doc)
        

urls = ['https://riskfactor.com/county/cabell-county/54011_fsid/flood',
        'https://riskfactor.com/county/grant-county-wv/54023_fsid/flood',
        'https://riskfactor.com/county/kanawha-county-wv/54039_fsid/flood',
        'https://riskfactor.com/county/nicholas-county-wv/54067_fsid/flood']

indices = [1, 4, 5 ,6]
        
extracted_list = [extract_data(url, indices) for url in urls]
create_table(extracted_list)



