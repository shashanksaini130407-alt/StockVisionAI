import yfinance as yf

def format_market_cap(value):

    if not value:

        return "N/A"

    trillion = 1_000_000_000_000

    billion = 1_000_000_000

    million = 1_000_000

    if value >= trillion:

        return f"${value/trillion:.2f} T"

    elif value >= billion:

        return f"${value/billion:.2f} B"

    elif value >= million:

        return f"${value/million:.2f} M"

    else:

        return str(value)

def get_company_info(symbol):

    stock = yf.Ticker(symbol)

    info = stock.info

    return {

        "company": info.get("longName", symbol),

        "sector": info.get("sector", "Unknown"),

        "industry": info.get("industry", "Unknown"),

        "website": info.get("website", ""),

        "country": info.get("country", "Unknown"),

        "employees": info.get(

            "fullTimeEmployees",

            "N/A"

        ),

        "market_cap": format_market_cap(

            info.get("marketCap")

        ),

        "exchange": info.get(

            "exchange",

            ""

        ),

        "summary": info.get(

            "longBusinessSummary",

            "No company summary available."

        )

    }