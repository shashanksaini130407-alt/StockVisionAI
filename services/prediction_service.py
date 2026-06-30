import pandas as pd
import joblib
from services.ai_service import generate_ai_analysis
from utils.live_data import load_live_stock
from utils.load_data import load_stock
from services.company_service import get_company_info
from utils.preprocess import preprocess_data
from utils.indicators import add_indicators
from utils.visualization import create_candlestick_chart


# Load model only once
model = joblib.load("saved_models/random_forest.pkl")


def predict_stock(symbol):
    """
    Performs complete stock prediction pipeline.
    Returns a dictionary containing all dashboard data.
    """

    # -----------------------------
    # Load data
    # -----------------------------
    try:

        df = load_live_stock(symbol)

    except Exception:

        df = load_stock(symbol)

    df["Date"] = df["Date"].dt.tz_localize(None)

    # -----------------------------
    # Clean data
    # -----------------------------
    df = preprocess_data(df)

    # -----------------------------
    # Add technical indicators
    # -----------------------------
    df = add_indicators(df)

    df = df.dropna()

    # -----------------------------
    # Create chart
    # -----------------------------
    chart = create_candlestick_chart(df)

    # -----------------------------
    # Latest row
    # -----------------------------
    latest = df.iloc[-1]

    # -----------------------------
    # Features for ML model
    # -----------------------------
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

    # -----------------------------
    # Predict
    # -----------------------------
    prediction = model.predict(features)[0]

    analysis = generate_ai_analysis(
        df,
        prediction
    )

    company = get_company_info(symbol)

    result = {

    "symbol": symbol,

    "prediction": round(prediction,2),

    "chart": chart,

    "sma20": round(latest["SMA_20"],2),

    "sma50": round(latest["SMA_50"],2),

    "volume": int(latest["Volume"]),

    **analysis,

    **company

}

    return result