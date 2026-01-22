stock_prices = [150, 22, "ERROR", 300]

for price in stock_prices:
    try:
        if price > 100:
            print(f"Buy: {price}")
        else:
            print(f"Wait: {price}")
    except Exception as e:
        print(f"Skipping bad data point: {price}. Reason: {e}")