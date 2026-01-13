import pandas as pd

# Load the file we just created, the .csv file
# This is how I will handle Billions of rows later !
df = pd.read_csv('customers.csv')

print("--- Data Loaded from CSV File ---")
print(df)

# Quick check: How many rows and columns?
print(f"\nDataset Shape: {df.shape}")