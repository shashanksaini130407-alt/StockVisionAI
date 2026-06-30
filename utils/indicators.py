def add_indicators(df):

    # SMA 20
    df["SMA_20"] = (
        df["Close"]
        .rolling(window=20)
        .mean()
    )

    # SMA 50
    df["SMA_50"] = (
        df["Close"]
        .rolling(window=50)
        .mean()
    )

    # EMA 20
    df["EMA_20"] = (
        df["Close"]
        .ewm(span=20)
        .mean()
    )

    # Daily Return
    df["Daily_Return"] = (
        df["Close"]
        .pct_change()
    )

    return df