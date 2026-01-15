import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the data we engineered in the last step
df = pd.read_csv('final_engineered_data.csv')

# 2. Create a Histogram of Query Counts
# This shows us how many users fall into different "activity buckets"
plt.hist(df['query_count'], bins=5, color='skyblue', edgecolor='black')

# 3. Add Labels (The "Google Standard" for clarity)
plt.title('Distribution of User Queries')
plt.xlabel('Number of Queries')
plt.ylabel('Number of Users')

# 4. Save the chart as an image
plt.savefig('user_queries_chart.png')
print("Chart saved successfully as: User_queries_chart.png")

# 5. Show the chart on screen
plt.show()
