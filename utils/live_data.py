import yfinance as yf


def load_live_stock(symbol):

    stock = yf.Ticker(symbol)

    df = stock.history(

        period="2y",

        interval="1d"

    )

    if df.empty:

        raise Exception(

            f"{symbol} not found."

        )

    df.reset_index(inplace=True)

    return df