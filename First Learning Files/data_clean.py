import pandas as pd
import numpy as np # We need this for "NaN" (Not a Number)

# Dataset with a "Missing" price for user 202
dirty_data = {
    'User_ID' : [201, 202, 203],
    'Price' : [10.00, np.nan, 30.00]
}
df = pd.DataFrame(dirty_data)

print("--- Data with Missing Value ___")
print(df)

print("--- Data with Missing Value ___")
print(df)

#FIX: FILL the missing price with the average of the others
df_fixed = df.fillna(20.00)

print("\n--- Fixed Data ___")
print(df_fixed)




