import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_candlestick_chart(df):

    fig = make_subplots(

        rows=2,
        cols=1,

        shared_xaxes=True,

        vertical_spacing=0.03,

        row_heights=[0.75, 0.25],

        subplot_titles=("Stock Price", "Volume")

    )

    # ==========================
    # Candlestick
    # ==========================

    fig.add_trace(

        go.Candlestick(

            x=df["Date"],

            open=df["Open"],

            high=df["High"],

            low=df["Low"],

            close=df["Close"],

            name="Candlestick",

            increasing_line_color="#22C55E",

            decreasing_line_color="#EF4444"

        ),

        row=1,
        col=1

    )

    # ==========================
    # SMA20
    # ==========================

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["SMA_20"],

            mode="lines",

            line=dict(color="#2563EB", width=2),

            name="SMA 20"

        ),

        row=1,
        col=1

    )

    # ==========================
    # SMA50
    # ==========================

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["SMA_50"],

            mode="lines",

            line=dict(color="#F59E0B", width=2),

            name="SMA 50"

        ),

        row=1,
        col=1

    )

    # ==========================
    # EMA20
    # ==========================

    fig.add_trace(

        go.Scatter(

            x=df["Date"],

            y=df["EMA_20"],

            mode="lines",

            line=dict(

                color="#8B5CF6",

                width=2,

                dash="dot"

            ),

            name="EMA 20"

        ),

        row=1,
        col=1

    )

    # ==========================
    # Volume
    # ==========================

    colors = []

    for open_price, close_price in zip(df["Open"], df["Close"]):

        if close_price >= open_price:

            colors.append("#22C55E")

        else:

            colors.append("#EF4444")

    fig.add_trace(

        go.Bar(

            x=df["Date"],

            y=df["Volume"],

            marker_color=colors,

            name="Volume"

        ),

        row=2,
        col=1

    )

    # ==========================
    # Layout
    # ==========================

    fig.update_layout(

        height=850,

        template="plotly_white",

        hovermode="x unified",

        dragmode="zoom",

        showlegend=True,

        legend=dict(

            orientation="h",

            y=1.06,

            x=0

        ),

        margin=dict(

            l=20,

            r=20,

            t=70,

            b=20

        )

    )

    # ==========================
    # Remove Range Slider
    # ==========================

    fig.update_layout(

        xaxis_rangeslider_visible=False

    )

    # ==========================
    # Grid
    # ==========================

    fig.update_xaxes(

        showgrid=True,

        gridcolor="#ECECEC"

    )

    fig.update_yaxes(

        showgrid=True,

        gridcolor="#ECECEC"

    )

    # ==========================
    # Range Selector
    # ==========================

    fig.update_xaxes(

        rangeselector=dict(

            buttons=[

                dict(

                    count=1,

                    label="1M",

                    step="month",

                    stepmode="backward"

                ),

                dict(

                    count=3,

                    label="3M",

                    step="month",

                    stepmode="backward"

                ),

                dict(

                    count=6,

                    label="6M",

                    step="month",

                    stepmode="backward"

                ),

                dict(

                    count=1,

                    label="1Y",

                    step="year",

                    stepmode="backward"

                ),

                dict(

                    step="all",

                    label="ALL"

                )

            ]

        )

    )

    return fig.to_html(

        full_html=False,

        config={

            "displaylogo": False,

            "responsive": True,

            "scrollZoom": True,

            "modeBarButtonsToRemove": [

                "lasso2d",

                "select2d"

            ]

        }

    )