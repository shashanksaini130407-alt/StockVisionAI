import pandas as pd
import os


def load_stock(symbol):
    """
    Load stock CSV file
    """

    file_path = os.path.join(
        "dataset",
        "stocks",
        f"{symbol}.csv"
    )

    df = pd.read_csv(file_path)

    return df