from sklearn.linear_m
import numpy as np

#1 Inputs: [Rooms, Square Footage]
X = np.array([
    [1, 500],
    [2, 1000],
    [3, 1500],`1/`
    [4, 2000]   
])

#2 Answers: Price in thousands ($100K, $200K, etc.)
y = np.array([100, 200, 300, 400])

model = LinearRegression()
model.fit(X,y)

# Predict price for a house with 5 rooms and 2500 sq ft
new_house = np.array([[5, 2500]])
prediction = model.predict(new_house)

print(f"Predicted House Price: ${prediction[0]}k")
