# PPHA 30538
# Fall 2023
# Final Project

# mhvuong
# My Vuong

import os
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

PATH = r'/Users/macbook/Documents/GitHub/final-project-my-vuong/'

def load_wv_data():
    df_wv_flood_attnd = pd.read_csv(os.path.join(PATH, 'Data/', 'wv_flood_attnd.csv'))
    return df_wv_flood_attnd


# Source:https://stackoverflow.com/questions/46664082/
# python-how-to-save-statsmodels-results-as-image-file
def plot_model_summary(results, fname):
    fig, ax = plt.subplots(figsize=(10, 8.5))
    
    formula = results.model.formula
    ax.text(0.01, 0.95, formula, fontfamily='monospace', fontsize=12, transform=ax.transAxes)
    
    
    summary_text = results.summary().as_text()
    ax.text(0.01, 0.05, summary_text, fontfamily='monospace', fontsize=12)
    ax.axis('off')
    
    fig.subplots_adjust(top=0.85, bottom=0.05)
    fig.savefig(os.path.join(PATH, 'Images/Regressions/', fname),
                dpi=300,
                bbox_inches='tight')
    
    
df_wv = load_wv_data()

full_model = smf.ols(formula='attnd_rate ~ flood_count + prcp', data=df_wv).fit()
plot_model_summary(full_model, 'full_model_summary.png')

fe_model = smf.ols(formula='attnd_rate ~ flood_count + prcp + county', data=df_wv).fit()
plot_model_summary(fe_model, 'fe_model.png')

flood_model = smf.ols(formula='attnd_rate ~ flood_count + county', data=df_wv).fit()
plot_model_summary(flood_model, 'flood_model_summary.png')

prcp_model = smf.ols(formula='attnd_rate ~ prcp + county', data=df_wv).fit()
plot_model_summary(prcp_model, 'prcp_model_summary.png')

interact_model = smf.ols(formula='attnd_rate ~ prcp + flood_count + prcp:flood_count + county', 
                         data=df_wv).fit()
plot_model_summary(interact_model, 'interaction_model_summary.png')

