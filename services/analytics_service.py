from database.db import get_connection
import plotly.express as px
import plotly.io as pio
import pandas as pd

def get_dashboard_stats(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    # Total predictions
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE user_id=?
    """, (user_id,))
    total_predictions = cursor.fetchone()[0]

    # BUY signals
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE user_id=?
        AND signal='BUY'
    """, (user_id,))
    buy_count = cursor.fetchone()[0]

    # SELL signals
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE user_id=?
        AND signal='SELL'
    """, (user_id,))
    sell_count = cursor.fetchone()[0]

    # Average expected gain
    cursor.execute("""
        SELECT AVG(change_percent)
        FROM predictions
        WHERE user_id=?
    """, (user_id,))

    avg_change = cursor.fetchone()[0]

    if avg_change is None:
        avg_change = 0

    # Watchlist count
    cursor.execute("""
        SELECT COUNT(*)
        FROM watchlist
        WHERE user_id=?
    """, (user_id,))

    watchlist_count = cursor.fetchone()[0]

    conn.close()

    return {

        "total_predictions": total_predictions,

        "buy_count": buy_count,

        "sell_count": sell_count,

        "avg_change": round(avg_change, 2),

        "watchlist_count": watchlist_count

    }

def get_prediction_charts(user_id):

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            stock_symbol,
            predicted_price,
            current_price,
            change_percent,
            signal,
            prediction_time
        FROM predictions
        WHERE user_id=?
        ORDER BY prediction_time
        """,
        conn,
        params=(user_id,)
    )

    conn.close()

    if df.empty:

        return {

            "pie_chart": None,
            "line_chart": None,
            "bar_chart": None

        }

    # ===========================
    # BUY vs SELL Pie Chart
    # ===========================

    pie = px.pie(

        df,

        names="signal",

        title="BUY vs SELL Distribution",

        hole=0.45

    )

    pie.update_layout(

        transition_duration=800

    )

    pie_chart = pio.to_html(

        pie,

        full_html=False,

        include_plotlyjs="cdn"

    )

    # ===========================
    # Prediction Timeline
    # ===========================

    line = px.line(

        df,

        x="prediction_time",

        y="predicted_price",

        color="stock_symbol",

        markers=True,

        title="Predicted Prices Over Time"

    )

    line.update_layout(

        transition_duration=800

    )

    line_chart = pio.to_html(

        line,

        full_html=False,

        include_plotlyjs=False

    )

    # ===========================
    # Expected Change
    # ===========================

    bar = px.bar(

        df,

        x="stock_symbol",

        y="change_percent",

        color="signal",

        title="Expected Change (%)"

    )

    bar.update_layout(

        transition_duration=800

    )

    bar_chart = pio.to_html(

        bar,

        full_html=False,

        include_plotlyjs=False

    )

    return {

        "pie_chart": pie_chart,

        "line_chart": line_chart,

        "bar_chart": bar_chart

    }