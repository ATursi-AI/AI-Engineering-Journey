import joblib
import pandas as pd

# 1. Load the "Frozen Brain"
# This takes milliseconds compared to training from scratch
model = joblib.load('premium_predictor_model.pkl')

def run_ai_prediction():
    print("--- Google Premium Predictor Live ---")

    # 2. Simulate a new user coming into the app
    # Let's say the user just hit 120 queries
    user_input = pd.DataFrame([[120]], columns=['query_count'])

    # 3. Use the loaded model
    prediction = model.predict(user_input)

    result = "PREMIUM" if prediction[0] ==1 else "STANDARD"
    print(f"Customer Status: {result}")

if __name__ == "__main__":
    run_ai_prediction()