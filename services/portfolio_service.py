from services.prediction_service import predict_stock


def calculate_portfolio(rows):
    """
    Enrich portfolio rows with live market data.
    """

    portfolio = []

    total_investment = 0
    total_current = 0

    for row in rows:

        try:
            prediction = predict_stock(row["stock_symbol"])

            current_price = prediction["current_price"]

            investment = row["quantity"] * row["buy_price"]

            current_value = row["quantity"] * current_price

            profit = current_value - investment

            return_percent = (
                (profit / investment) * 100
                if investment > 0
                else 0
            )

            portfolio.append({

                "id": row["id"],

                "symbol": row["stock_symbol"],

                "quantity": row["quantity"],

                "buy_price": row["buy_price"],

                "current_price": round(current_price, 2),

                "investment": round(investment, 2),

                "current_value": round(current_value, 2),

                "profit": round(profit, 2),

                "return_percent": round(return_percent, 2)

            })

            total_investment += investment

            total_current += current_value

        except Exception:

            continue

    summary = {

        "investment": round(total_investment, 2),

        "current_value": round(total_current, 2),

        "profit": round(total_current - total_investment, 2),

        "return_percent": round(

            ((total_current - total_investment)

             / total_investment * 100)

            if total_investment > 0 else 0,

            2

        )

    }

    return portfolio, summary