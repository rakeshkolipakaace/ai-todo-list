import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os

# Dummy dataset (Replace with real data if available)
data = pd.DataFrame({
    "urgency": [1, 2, 0, 3, 1, 0, 2],
    "days_left": [2, 1, 10, 0, 5, 8, 3],
    "completion_time": [3, 2, 7, 1, 4, 6, 2]  # Days taken to complete task
})

X = data[["urgency", "days_left"]]
y = data["completion_time"]

# Train ML model
model = LinearRegression()
model.fit(X, y)

# Ensure models folder exists
os.makedirs("models", exist_ok=True)

# Save the trained model
joblib.dump(model, "models/task_completion_model.pkl")
print("✅ Model saved successfully in 'models/' folder!")
