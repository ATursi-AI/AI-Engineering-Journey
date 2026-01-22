import pandas as pd

# We'll use the same data style
raw_data = {
    'User_ID': [101, 102, 103, 104, 105],
    'Purchase_Amount': [12.50, 45.00, 120.10, 5.99, 50.00],
    'Is_Premium': [False, True, True, False, True]
}
df = pd.DataFrame(raw_data)

# THE BIG STEP: Filter for only Premium Users
premium_only = df[df['Is_Premium'] == True]

print("--- Premium Customers Only ---")
print(premium_only)
