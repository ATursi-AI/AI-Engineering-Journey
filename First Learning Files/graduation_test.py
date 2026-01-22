# 1. THE DATA (The "Pantry")
model_scores = [0.98, 0.72, 0.45]

# 2. THE SAFETY WRAPPER (The "Insurance Policy")
try:
    # 3. THE LOOP (The "Factory Belt")
    for score in model_scores:

        # 4. THE DECISION LOGIC (The "Filter")
        if score > 0.90:
            print(f"Model {score}: DEPLOY TO PRODUCTION")

        elif score >= 0.70:
            print(f"Model {score}: NEEDS RETRAINING")

        else:
            print(f"Model {score}: REJECTED")

# 5. THE EMERGENCY EXIT
except Exception as e:
    print(f"Safety Alert: An unexpected error occured: {e}")
    