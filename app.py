import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("dataset.csv")

print("Dataset:")
print(data)

X = data[["age", "fever", "cough", "fatigue"]]
y = data["disease"]

model = DecisionTreeClassifier()
model.fit(X, y)

sample = [[30, 1, 1, 0]]
prediction = model.predict(sample)

print("Predicted disease:", prediction[0])
