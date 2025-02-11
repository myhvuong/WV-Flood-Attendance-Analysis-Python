# myhvuong
# My Vuong

### PLOTTING

import geopandas
import matplotlib.pyplot as plt
import os
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from shiny import App, render, ui


PATH = r'/Users/macbook/Documents/GitHub/final-project-my-vuong/'

def load_shp():
    wv = geopandas.read_file(os.path.join(PATH, 'Data/', 'County_Boundaries_24k_topo.gdb'))
    wv['County_Name'] = wv['County_Name'].str.strip()
    return wv

def load_risk():
    wv_risk = pd.read_csv(os.path.join(PATH, 'Data/', 'wv_risk.csv'))
    
    # Source: https://stackoverflow.com/questions/71907567
    # /valueerror-geodataframe-does-not-support-multiple-columns-using-the-geometry-co
    wv_risk = geopandas.GeoDataFrame(
        wv_risk.loc[:, [c for c in wv_risk.columns if c != 'geometry']],
        geometry=geopandas.GeoSeries.from_wkt(wv_risk['geometry'])
        )
    wv_risk['Risk_Type'] = wv_risk['Risk_Type'].fillna('N/A')
    return wv_risk

def load_wv_data():
    df_wv_flood_attnd = pd.read_csv(os.path.join(PATH, 'Data/', 'wv_flood_attnd.csv'))
    df_wv_flood_attnd['flood_count'] = df_wv_flood_attnd['flood_count'].astype(int)
    
    # Replace 0 with a small value so bars with 0 value can still be displayed
    small_value = 0.04
    df_wv_flood_attnd['flood_count'] = df_wv_flood_attnd['flood_count'].replace(0, small_value)
    return df_wv_flood_attnd

def create_map(county, wv, wv_risk):
    fig, ax = plt.subplots(figsize=(10,10))
    ax = wv.boundary.plot(ax=ax, edgecolor='black', linewidth=1)
    
    # Color in each county by degree of risk level
    colors = {'N/A': 'aliceblue','major': 'darkblue',
              'extreme': 'cornflowerblue','severe': 'slateblue'}
    cmap = ListedColormap([colors[type] for type in wv_risk['Risk_Type'].unique()])
    
    ax = wv_risk.plot(ax=ax, column='Risk_Type', cmap=cmap, legend=True)
    
    # Creating color legend by degree of risk levels
    risk_levels = ['major', 'severe', 'extreme']
    color_legend = ['cornflowerblue', 'slateblue', 'darkblue']
    zipped = zip(risk_levels, color_legend)
    legend_elements = [Patch(color=color, label=risk_level) for risk_level, color in zipped]
    
    ax.legend(handles=legend_elements, 
              loc='lower right', 
              ncol=len(risk_levels))
    
    # Create different border color to highlight selected county
    wv_risk[wv_risk['County_Name'] == county].boundary.plot(ax=ax,
                                                            edgecolor='darkorange',
                                                            linewidth=2)
    
    ax.axis('off')
    ax.set_title('West Virginia Flood Risk by County (Cabell, Grant, Kanawha, Nicholas)',
                 fontsize=16)
    return ax

def create_bar_plot(school_year, df_wv_flood_attnd):
    df = df_wv_flood_attnd[df_wv_flood_attnd['school_year'] == school_year].copy()
    
    ax = sns.barplot(df, x='county', y='flood_count', color='steelblue')
    ax = plt.gca()
    
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.tick_params(axis='x', which='both', bottom=False, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_ylim(0, df_wv_flood_attnd['flood_count'].max() + 1)
    ax.set_xlabel('County', fontsize=12)
    ax.set_ylabel('Flood Count', fontsize=12)
    ax.set_title(f'Number of Flood Incidents by County in the {school_year} school year',
                 fontsize=18)
    return ax


wv = load_shp()
wv_risk = load_risk()

df_wv_flood_attnd = load_wv_data()


app_ui = ui.page_fluid(
    ui.row(
        ui.column(9, ui.em(ui.h5('PPHA 30538 Autumn 2023')),
                  ui.em(ui.h5('Autumn 2023')),
                  ui.em(ui.h5('My Vuong')),
                  ui.row()),
        ui.column(3, ui.output_image(id='logo',height='10%'), align='right')
        ),
    ui.row(ui.h3('Final Project'), align='center'),
    ui.row(ui.h3('West Virginia Flooding Information'), align='center'),
    ui.navset_tab(
        ui.nav('Flood Map', 
               ui.layout_sidebar(
                   ui.sidebar(
                       ui.strong('West Virginia Flood Risk'),
                       ui.input_radio_buttons(id='county',
                                              label='Please select a county:',
                                              choices=['Cabell', 'Grant', 'Kanawha', 'Nicholas'])),
                   ui.output_plot('map', width='100%', height='600px'))),
        ui.nav('Flood Incidents', 
               ui.layout_sidebar(
                   ui.sidebar(
                       ui.strong('West Virginia Flood Incidents'),
                       ui.input_select(id='school_year',
                                       label='Please select a school year:',
                                       choices=['2003-2004', '2004-2005', '2005-2006', '2006-2007', '2007-2008',
                                                '2008-2009', '2009-2010', '2010-2011', '2011-2012', '2012-2013',
                                                '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018',
                                                '2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023'])),
                   ui.column(8, ui.output_plot('barplot'), offset=2))),
    )
)


def server(input, output, session):
    @output
    @render.image
    def logo():
        ofile = os.path.join(PATH, 'Images/', 'harris logo.png')
        return {'src':ofile, 'contentType':'image/png'}
    
    @output
    @render.plot
    def map():
        map = create_map(input.county().upper(), wv, wv_risk)
        return map
    
    @output
    @render.plot
    def barplot():
        barplot = create_bar_plot(input.school_year(), df_wv_flood_attnd)
        return barplot

app = App(app_ui, server)


