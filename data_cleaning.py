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

# --- RUN THE CLEANING ---
# IMPORTANT: Catch the returned dataframe in a variable named 'df'
df = clean_google_data() 

# --- FEATURE ENGINEERING ---
# Now 'df' exists out here and we can add new columns!
days_active = 30
df['queries_per_day'] = df['query_count'] / days_active

# Create a 'high_intent' flag (Yrue/False)
df['high_intent'] = df['queries_per_day'] > 2.0

print("\n--- Feature Engineering Complete ___")
# This prints only the relevant columns to keep the terminal clean
print(df[['query_count', 'queries_per_day', 'high_intent']])
          
          
# --- EXPORET ---
# Now we save the final, engineered version to a CSV
output_filename = 'finaL_engineered_data.csv'
df.to_csv(output_filename)

print(f"\nSuccess! Cleaned and Engineered data saved as: {output_filename}")

# --- ONE-HOT ENCODING ---
# Let's turn our 1/0 premium column into readable labels first
df['user_tier'] = df['is_premium'].map({1.0: 'Premium' , 0.0: 'Standard'})
   
# Now, we use Pandas to create "Dummy" columns
# This turns the 'user_tier' column into 'user_tier_Premium' and 'user_tier_Standard'
df = pd.get_dummies(df, columns=['user_tier'])

print("\n--- One-Hot Encoding Complete ---")
print(df.filter(like='user_tier')) # This shows only the new tier column



