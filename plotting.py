# myhvuong
# My Vuong

### STATIC PLOTS

import os
import pandas as pd
import seaborn as sns
import geopandas
import matplotlib.pyplot as plt

PATH = r'/Users/macbook/Documents/GitHub/final-project-my-vuong/'

def load_shp():
    wv = geopandas.read_file(os.path.join(PATH, 'Data/', 'County_Boundaries_24k_topo.gdb'))
    wv['County_Name'] = wv['County_Name'].str.strip()
    return wv


def load_risk_type():
    df_risk = pd.read_csv(os.path.join(PATH, 'Data/', 'risk_type.csv'))
    df_risk = df_risk.rename(columns={'county': 'County_Name',
                                      'risk_type': 'Risk_Type'})
    
    df_risk['County_Name'] = df_risk['County_Name'].str.replace(' County', '')
    df_risk['County_Name'] = df_risk['County_Name'].str.upper()
    
    df_risk['Risk_Type'] = df_risk['Risk_Type'].str.split().str[0]
    
    df_risk = df_risk[['County_Name', 'Risk_Type']]
    return df_risk


def export_map_df(wv, df_risk):
    df_merged = wv.merge(df_risk, how='left', on='County_Name')
    df_merged['Risk_Type'] = df_merged['Risk_Type'].fillna('N/A')
    df_merged.to_csv(os.path.join(PATH, 'Data/', 'wv_risk.csv'))
    return df_merged


### Static plots
def load_wv_data():
    df_wv_flood_attnd = pd.read_csv(os.path.join(PATH, 'Data/', 'wv_flood_attnd.csv'))
    return df_wv_flood_attnd


def create_static_plot(y_variable, df_wv_flood_attnd):
    df_attnd = df_wv_flood_attnd[['county', 'school_year', y_variable]]
    
    fig, axs = plt.subplots(2, 2)
    (ax1, ax2), (ax3, ax4) = axs
    counties = ['Cabell', 'Grant', 'Kanawha', 'Nicholas']
    
    for ax,county in zip(axs.ravel(),counties):
        sns.lineplot(x='school_year', y=y_variable, 
                     data=df_attnd[df_attnd['county']== county],
                     ax=ax)
        
        ax.set_xticks(df_attnd['school_year'].unique()[::3])
        ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right', fontsize=8)
        
        ax.tick_params(axis='y', labelsize=9)
        
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.text(0.5, 1.05, county, ha='center', va='center', transform=ax.transAxes)
        
        if county in ['Cabell','Grant']:
            ax.xaxis.set_tick_params(labelbottom=False)
            
    fig.supxlabel('School Year')     
    plt.subplots_adjust(bottom=0.22)
    
    if y_variable == 'attnd_rate':
        fig.supylabel('Attendance Rate (%)')
        fig.suptitle('Attendance Rate Trend from 2003 to 2023 by County', y=0.99) 
        fig.savefig(os.path.join(PATH, 'Images/Plots', 'attnd_rate'))
    else:
        fig.supylabel('Precipitation (mm)')
        fig.suptitle('Average Precipitation Trend from 2003 to 2023 by County', y=0.99) 
        fig.tight_layout(pad=0.6)
        fig.savefig(os.path.join(PATH, 'Images/Plots', 'prcp'))
    
    return ax

# Exporting dataframe for interactive map
wv = load_shp()
df_risk = load_risk_type()
export_map_df(wv, df_risk)

df_wv_flood_attnd = load_wv_data()
create_static_plot('attnd_rate', df_wv_flood_attnd)
create_static_plot('prcp', df_wv_flood_attnd)
