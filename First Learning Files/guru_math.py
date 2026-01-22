import numpy as np

# let's simulate 10,000 stocks and 100 days of ptice
# This creates a matrix of 10,000 rows and 100 columns
stock_matrix = np.random.uniform(10, 500, (10000, 100))

# The Guru Axis Magic
# axis=1 tells NumPy to calculate across the COLUMNS (for each row/stock)
average_per_stock = np.mean(stock_matrix, axis=1)

print("--- NumPy Axis Results ___")
print(f"Number of averages calculated: {len(average_per_stock)}")
print(f"Average of Stock #1: ${average_per_stock[0]:.2f}")
print(f"Average of Stock #2: ${average_per_stock[1]:.2f}")



