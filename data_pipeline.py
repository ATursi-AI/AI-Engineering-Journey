import pandas as pd
import logging

# Setup professional logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_user_report():
    """Simulates Loading and processing a Google User dataset."""
    
    #1. Raw Data (In the real world, this comes from a CSV or Database)
    raw_data = {
        'user_id': [101, 102, 103, 104],
        'query_count': [10, 50, 2, 100],
        'is_premium': [True, False, False, True]
    }

    #2. Convert to a DataFrame (The AI's favorite format)
    df = pd.DataFrame(raw_data)

    # NEW LINE: Use 'user_id' as the label for each row
    df = df.set_index('user_id')

    logging.info("DataFrame created successfully.")

    #3. Data Transformation: Calculate a 'Power User' score
    # We define a Power User as someone with more than 40 queries
    df['is_power_user'] = df['query_count'] > 40

    return df

# Run the pipeline
user_df = create_user_report()

print("--- Google User Analytics Report ---")
print(user_df)

#1 Filter: Show only Power Users
power_users = user_df[user_df['is_premium'] == True]

print("\n--- Power User Segment ---")
print(power_users)

print("\n--- Premium User Segment ---")
print(premium_users)

