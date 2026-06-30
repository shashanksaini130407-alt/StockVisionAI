import numpy as np


def generate_ai_analysis(df, prediction):

    latest = df.iloc[-1]

    current_price = float(latest["Close"])

    change_percent = (
        (prediction - current_price)
        / current_price
    ) * 100

    volatility = float(
        df["Daily_Return"].std() * 100
    )

    # ------------------------
    # Risk Level
    # ------------------------

    if volatility < 1:
        risk = "Low"

    elif volatility < 3:
        risk = "Medium"

    else:
        risk = "High"

    # ------------------------
    # Trend
    # ------------------------

    trend = (
        "Bullish"
        if latest["SMA_20"] > latest["SMA_50"]
        else "Bearish"
    )

    # ------------------------
    # Signal
    # ------------------------

    signal = (
        "BUY"
        if prediction > current_price
        else "SELL"
    )

    # ------------------------
    # Target Price
    # ------------------------

    target_price = round(prediction, 2)

    # ------------------------
    # Stop Loss
    # ------------------------

    if signal == "BUY":
        stop_loss = round(current_price * 0.97, 2)

    else:
        stop_loss = round(current_price * 1.03, 2)

    # ------------------------
    # AI Confidence
    # ------------------------

    price_difference = abs(prediction - current_price)

    price_difference_percent = (
        price_difference / current_price
    ) * 100

    confidence = 100

    confidence -= volatility * 4

    confidence -= price_difference_percent * 2

    if trend == "Bullish" and signal == "BUY":
        confidence += 5

    if trend == "Bearish" and signal == "SELL":
        confidence += 5

    confidence = max(50, min(99, confidence))

    # ------------------------
    # Recommendation
    # ------------------------

    if signal == "BUY":

        if confidence >= 90:
            recommendation = "Strong Buy"

        elif confidence >= 80:
            recommendation = "Buy"

        else:
            recommendation = "Watch"

    else:

        if confidence >= 90:
            recommendation = "Strong Sell"

        elif confidence >= 80:
            recommendation = "Sell"

        else:
            recommendation = "Hold"

    # ------------------------
    # AI Reasons
    # ------------------------

    reasons = []

    if latest["Close"] > latest["EMA_20"]:
        reasons.append("Price is trading above EMA 20.")

    else:
        reasons.append("Price is trading below EMA 20.")

    if latest["SMA_20"] > latest["SMA_50"]:
        reasons.append(
            "Short-term trend is stronger than long-term trend."
        )

    else:
        reasons.append(
            "Long-term trend remains dominant."
        )

    if signal == "BUY":
        reasons.append(
            f"Model predicts an upside of {change_percent:.2f}%."
        )

    else:
        reasons.append(
            f"Model predicts a downside of {abs(change_percent):.2f}%."
        )

    reasons.append(
        f"Estimated confidence: {confidence:.1f}%."
    )

    # ------------------------
    # Trading Advice
    # ------------------------

    if recommendation == "Strong Buy":

        advice = (
            "Momentum and prediction are aligned. "
            "Suitable for accumulation with proper risk management."
        )

    elif recommendation == "Buy":

        advice = (
            "Positive outlook. Consider entering gradually."
        )

    elif recommendation == "Watch":

        advice = (
            "Mixed signals. Wait for confirmation before entering."
        )

    elif recommendation == "Sell":

        advice = (
            "Weak outlook. Consider booking profits or reducing exposure."
        )

    else:

        advice = (
            "High downside risk. Avoid new long positions until trend improves."
        )

    # =========================================
    # Prediction Analytics
    # =========================================

    risk_score = max(
        0,
        round(100 - volatility * 10)
    )

    trend_strength = (
        "Strong"
        if abs(change_percent) > 2
        else "Moderate"
        if abs(change_percent) > 1
        else "Weak"
    )

    momentum = (

        "Bullish"

        if latest["Close"] > latest["EMA_20"]

        else "Bearish"

    )

    volume_status = (

        "High"

        if latest["Volume"] > df["Volume"].mean()

        else "Normal"

    )

    market_sentiment = (

        "Positive"

        if signal == "BUY"

        else "Negative"

    )

    # ------------------------
    # Return
    # ------------------------

    return {

        "current_price": round(current_price, 2),

        "change_percent": round(change_percent, 2),

        "trend": trend,

        "volatility": round(volatility, 2),

        "risk_score": risk_score,

        "trend_strength": trend_strength,

        "momentum": momentum,

        "volume_status": volume_status,

        "market_sentiment": market_sentiment,

        "risk": risk,

        "signal": signal,

        "confidence": round(confidence, 1),

        "target_price": target_price,

        "stop_loss": stop_loss,

        "recommendation": recommendation,

        "reasons": reasons,

        "advice": advice
    }