import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from utils.load_data import load_stock
from utils.preprocess import preprocess_data
from utils.indicators import add_indicators


# Load data
df = load_stock("AAPL")

# Clean
df = preprocess_data(df)

# Features
df = add_indicators(df)

# Remove NaN created by indicators
df = df.dropna()

# Create target
df["Target"] = df["Close"].shift(-1)

df = df.dropna()

# Features
features = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "SMA_20",
    "SMA_50",
    "EMA_20"
]

X = df[features]

y = df["Target"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Metrics
mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

print("MAE :", mae)
print("RMSE:", rmse)
print("R2  :", r2)

# Save model
joblib.dump(
    model,
    "saved_models/random_forest.pkl"
)

print("\nModel Saved Successfully!")