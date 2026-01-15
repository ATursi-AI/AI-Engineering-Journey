import pandas as pd
import numpy as np

def clean_google_data():
    # 1. Create data with missing values (None)
    raw_data = {
        'user_id': [101, 102, 103, 104, 105],
        'query_count' : [10, None, 2, 100, None], # Two missing values
        'is_premium': [1, 0, 0, 1, None] # One missing value
    }

    df = pd.DataFrame(raw_data).set_index('user_id')

    print("--- Original Messy Data ---")
    print(df)

    # 2. Find the holes
    # .isnull().sum() counts how many missing values are in each column
    print("\n--- Missing Value Count ---")
    print(df.isnull().sum())

    return df
clean_google_data()

