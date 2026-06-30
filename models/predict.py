import joblib

from utils.load_data import load_stock
from utils.preprocess import preprocess_data
from utils.indicators import add_indicators

# Load model
model = joblib.load(
    "saved_models/random_forest.pkl"
)

# Load latest stock
df = load_stock("AAPL")

df = preprocess_data(df)

df = add_indicators(df)

df = df.dropna()

# Latest row
latest = df.iloc[-1]

import pandas as pd

features = pd.DataFrame([{
    "Open": latest["Open"],
    "High": latest["High"],
    "Low": latest["Low"],
    "Close": latest["Close"],
    "Volume": latest["Volume"],
    "SMA_20": latest["SMA_20"],
    "SMA_50": latest["SMA_50"],
    "EMA_20": latest["EMA_20"]
}])

prediction = model.predict(features)

print(
    f"\nPredicted Next Day Close Price: "
    f"${prediction[0]:.2f}"
)