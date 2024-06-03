import pandas as pd
import numpy as np

# read csv file
home_data = pd.read_csv('all_commodities.csv')

# condition to remove data
condition = home_data['1 Month Change'] == '\xa0'
df_filtered = home_data[~condition]

# save new csv
cleaned_file_path = 'cleaned_commodities.csv'
df_filtered.to_csv(cleaned_file_path, index=False)