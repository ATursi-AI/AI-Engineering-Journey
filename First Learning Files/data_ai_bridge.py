import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import logging

# 1. Setup Data
raw_data = {
    'user_id': [101, 102, 103, 104, 105, 106],
    'query_count': [10, 50, 2, 100, 5, 80],
    'is_premium': [1, 0, 0, 1, 0, 1]  # 1 = Premium, 0 = Standard
}

df = pd.DataFrame(raw_data).set_index('user_id')

# 2. Feature Selection (X = Input, y = Answer)
# We use [[ ]] to keep x as a table/DataFrame
X = df[['query_count']]
y = df['is_premium']

# 3. The "Google" Model: Training
model = DecisionTreeClassifier()
model.fit(X, y)

# 4. Prediction: Use a DataFrame so the AI sees the 'Feature Name'
# Instead of [[75]], columns=[query_count'])
new_data = pd.DataFrame([[75]], columns=['query_count'])  
prediction = model.predict(new_data)

status = "Premium" if prediction[0] == 1 else "Standard"
print(f"AI Analysis: User with 75 queries is likely {status}")

# 5. Evaluation: How well did the AI learn?
# .score compares the AI's guesses for X against the real answers in y
accuracy = model.score(X, y)

print(f"--- Google Model Quality Report ---")
print(f"Training Accuracy: {accuracy * 100}%")

if accuracy == 1.0:
    print("Status: model is 100% accurate on this data.")
else:
    print(f"Status: Model is making mistakes. Needs more data.")

import joblib
 # 6. Save the model to a file
model_filename = 'premium_predictor_model.pkl'
joblib.dump(model, model_filename)

print(f"--- Asset Management ---")
print(f"Model saved succesfully as: {model}")
  