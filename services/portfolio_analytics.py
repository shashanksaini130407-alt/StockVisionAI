from collections import defaultdict

import plotly.express as px
import plotly.io as pio


def create_portfolio_chart(rows):

    if not rows:
        return None

    values = defaultdict(float)

    for row in rows:

        values[row["symbol"]] += row["current_value"]

    fig = px.pie(

        names=list(values.keys()),

        values=list(values.values()),

        hole=0.45,

        title="Portfolio Allocation"

    )

    fig.update_layout(

        height=450,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        showlegend=True,

        paper_bgcolor="white",

        plot_bgcolor="white"

    )

    fig.update_traces(

        textposition="inside",

        textinfo="percent+label"

    )

    return pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs=True
    )