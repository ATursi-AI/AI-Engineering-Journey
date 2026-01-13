import pandas as pd

# 1. We create a tiny "Database" of customer info
raw_data = {
    'User_ID': [101, 102, 103, 104, 105],
    'Purchase_Amount': [12.50, 45.00, 120.10, 5.99, 50.00],
    'Is_Premium': [False, True, True, False, True]
}

# 2. Turn this into a "DataFrame" (The AI Engineer's standars tool)
df = pd.DataFrame(raw_data)

# 3. Only look at the first 3 rows (to save space)
print("--- Viewing the Top of the Dataset ---")
print(df.head(3))

# 4. Calculate a quick statistics for the AI
print(f"\nAverage Purchase: ${df['Purchase_Amount']. mean()}")

