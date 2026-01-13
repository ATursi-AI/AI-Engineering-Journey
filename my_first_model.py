from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4], [5]])
y = np.array([10, 20, 30, 40, 50])

model = LinearRegression()
model.fit(X, y)

prediction = model.predict([[10]])

print(f"AI Prediction for input 10: {prediction[0]}")