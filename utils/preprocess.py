import pandas as pd


def preprocess_data(df):

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date")

    df = df.dropna()

    df.reset_index(drop=True, inplace=True)

    return df