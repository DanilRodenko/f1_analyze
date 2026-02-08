
import pandas as pd
import numpy as np


def overview_dataframe(name, df):
    print(f"\n {name.upper()}")
    print("-" * 50)
    print(f"Shape: {df.shape}")
    print("Columns:", list(df.columns))
    print("DTypes:\n", df.dtypes)
    print("Missing values:\n", df.isnull().sum())
    print(f"Duplicated rows: {df.duplicated().sum()}")
    print("First 2 rows:\n", df.head(2))
    print()