import os
import pandas as pd

def load_data(df_name):
    df = pd.read_csv(f'../data/raw/{df_name}.csv')
    return df