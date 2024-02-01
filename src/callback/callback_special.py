import datetime as dt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.nonparametric.smoothers_lowess import lowess
from data_preparation import *
from constants import *
from dash import Input, Output, callback, html, dcc
from calendar import isleap


@callback(
    Output("mean-day", "figure"),
    Input("range-slider", "value"),
    Input("filter-geo", "value"),
    Input("cause", "value"),
    Input("slider", "value"),
)
def func(range_date, geo, metric, slider): 
    year = slider
    data_date = data_date_filter(range_date)
    data_filter = data_geo_filter(data_date, geo)
    
    if metric == "size":
        dframe = data_filter.groupby(["year", "month", "day"],as_index=False).size()
    else:
        dframe = data_filter.groupby(["year", "month", "day"],as_index=False)[["nkill", "nwound","casualties"]].sum()

    dfr = dframe.copy()

    dfr['date'] = pd.to_datetime(dfr[['year', 'month', 'day']], errors='coerce')
    dfr["dayofyear"] = dfr["date"].dt.dayofyear
    dfr["dayofyear"] = dfr["dayofyear"].where(
        ~((dfr["date"].dt.month > 2) & (dfr["date"].dt.is_leap_year)),
        dfr["dayofyear"] - 1,
    )
    dfr.reset_index(drop=True, inplace=True)
    dfr.drop(columns=["year", "month", "day"], inplace=True)


    data = dfr.copy()
    data = (
        data.groupby("dayofyear")[metric]
        .agg(
            [
                ("p05", lambda x: np.nanpercentile(x, 10)),
                ("mean", "mean"),
                ("p95", lambda x: np.nanpercentile(x, 90)),
            ]
        )
        .reset_index()
    )

    for col in ["p05", "mean", "p95"]:
        smoothed_values = lowess(
            data[col],
            data["dayofyear"],
            is_sorted=True,
            # Fraction of data used when estimating each y-value
            # 1/12 roughly equals one month (= a lot of smoothing)
            frac=1 / 12,
        )

        data[col] = smoothed_values[:, 1]

    data[f"{year}"] = dfr[dfr["date"].dt.year == year][metric].reset_index(drop=True)
    data[f"{year}_diff"] = data[f"{year}"] - data["mean"]
    dayofyear = data["dayofyear"]

    if isleap(year):
        dayofyear = data["dayofyear"].where(
            data["dayofyear"] < 60, other=data["dayofyear"] + 1
        )

    data["date"] = dayofyear.apply(
        lambda x: dt.datetime(year, 1, 1) + dt.timedelta(days=x - 1)
    )
    
    above_mean_percentage = (data[data[f"{year}"] > data['mean']].shape[0] / data.shape[0]) * 100
    below_mean_percentage = (data[data[f"{year}"] < data['mean']].shape[0] / data.shape[0]) * 100
    above_percentile_95_percentage = (data[data[f"{year}"] > data['p95']].shape[0] / data.shape[0]) * 100
    
    

    fig = go.Figure()

    fig.add_traces(
        [
            # p95 trace used as upper bound. This is needed to fill the area between
            # the p05 and p95 traces using the "tonexty" fill option
            go.Scatter(
                x=data["date"],
                y=data["p95"],
                name="Percentile area upper bound (p95)",
                # Make line invisible
                line_color="rgba(0,0,0,0)",
                showlegend=False,
                hoverinfo="skip",
            ),
            # Fill area between p05 and p95
            go.Scatter(
                x=data["date"],
                y=data["p05"],
                name="Area between p05 and p95",
                fill="tonexty",
                fillcolor="lightgray",
                line_color="rgba(0,0,0,0)",
                showlegend=False,
                hoverinfo="skip",
            ),
        ]
    )

    colors = get_colorscale(data[f"{year}_diff"])

    # Set opacity to 0.6 for values between p05 and p95, otherwise 1
    opacity = np.where(
        (data[f"{year}"] >= data["p05"]) & (data[f"{year}"] <= data["p95"]), 0.6, 1
    )

    # Invisible trace just to show the correct hover info
    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data[f"{year}"],
            showlegend=False,
            mode="markers",
            name="Hoverinfo current date",
            hovertemplate=("%{y:.1f} °C<extra></extra>"),
            marker={
                "color": colors,  # This color will be shown on hover
                "opacity": 0,  # Hide the marker
            },
        )
    )

    # For each day, add a filled area between the mean and the year's value
    for i in range(len(data) - 1):
        # Define x and y values to draw a polygon between mean and values of today and tomorrow
        date_today = data["date"].iloc[i]
        date_tomorrow = data["date"].iloc[i + 1]
        mean_today = data["mean"].iloc[i]
        mean_tomorrow = data["mean"].iloc[i + 1]
        value_today = data[f"{year}"].iloc[i]
        value_tomorrow = data[f"{year}"].iloc[i + 1]

        # If one day is above and the other below the mean, set the value to the mean
        if (value_today > mean_today) ^ (value_tomorrow > mean_tomorrow):
            value_tomorrow = mean_tomorrow

        fig.add_trace(
            go.Scatter(
                name=f"Daily value {data['date'].iloc[i].strftime('%d.%m.%Y')}",
                x=[date_today, date_today, date_tomorrow, date_tomorrow],
                y=[mean_today, value_today, value_tomorrow, mean_tomorrow],
                line_width=0,
                fill="toself",
                fillcolor=colors[i],
                showlegend=False,
                mode="lines",
                opacity=opacity[i],
                # Hide the trace from hover info
                hoverinfo="skip",
            )
        )
        
    fig.add_traces(
        [
            # p95 trace
            go.Scatter(
                x=data["date"],
                y=data["p95"],
                name="P95",
                line={"color": "orangered", "width": 2, "dash": "dot"},
                showlegend=False,
                hovertemplate=(
                    "%{y:.1f}"
                ),
            ),
            # Mean trace
            go.Scatter(
                x=data["date"],
                y=data["mean"],
                name="Mean",
                line={"color": "black", "width": 2.5},
                showlegend=False,
                hovertemplate=(
                    "%{y:.1f}"
                ),
            ),
            # p05 trace
            go.Scatter(
                x=data["date"],
                y=data["p05"],
                name="P05",
                line={"color": "royalblue", "width": 2, "dash": "dot"},
                showlegend=False,
                hovertemplate=(
                    "%{y:.1f}"
                ),
            ),
        ]
    )

    months_with_days = {
        month: (
            dt.datetime(year, month, 1),
            dt.datetime(
                year, month, 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
            ),
        )
        for month in range(1, 13)
    }

    # Loop over months and add a shape for each month
    for month, days in months_with_days.items():
        # Define background color
        bg_color = "white" if (month % 2) == 0 else "whitesmoke"

        fig.add_shape(
            type="rect",
            yref="paper",
            x0=days[0],
            x1=days[1],
            y0=0,
            y1=1,
            fillcolor=bg_color,
            layer="below",
            line_width=0,
        )


    # Position arrow
    arrow_x = dt.datetime.strptime(f"{year}-03-15", "%Y-%m-%d")
    arrow_y = data[data["date"] == arrow_x]["mean"].values[0]

    # Position text
    text_x = dt.datetime.strptime(f"{year}-04-15", "%Y-%m-%d")
    text_y = data[data["date"] == text_x]["p05"].values[0]

    fig.add_annotation(
        x=arrow_x,
        y=arrow_y,
        xref="x",
        yref="y",
        ax=text_x,
        ay=text_y,
        axref="x",
        ayref="y",
        showarrow=True,
        text="Moyenne jounalière du nombre d'attaque terroristes",
        xanchor="center",
        yanchor="middle",
        arrowwidth=.5,
        arrowcolor="black",
        name="Reference period mean",
    )


    """
    Annotate percentile area
    """
    # Position arrow
    arrow_x = dt.datetime.strptime(f"{year}-08-01", "%Y-%m-%d")
    arrow_y = data[data["date"] == arrow_x]["p95"].values[0] - 0.5

    # Position text
    text_x = dt.datetime.strptime(f"{year}-09-15", "%Y-%m-%d")
    text_y = data[data["date"] == text_x]["p95"].values[0] + 2

    fig.add_annotation(
        x=arrow_x,
        y=arrow_y,
        xref="x",
        yref="y",
        ax=text_x,
        ay=text_y,
        axref="x",
        ayref="y",
        text="Limite (critique) des 90%",
        showarrow=True,
        xanchor="center",
        yanchor="middle",
        arrowwidth=.5,
        arrowcolor="black",
        name="Reference period mean",
    )


    """
    Annotate percentile lines
    """
    for percentile, text in zip(["p05", "p95"], ["10%","90%"]):
        fig.add_annotation(
            x=data["date"].iloc[-1],
            y=data[percentile].iloc[-1],
            text=text,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
        )


    """
    Add data source
    """
    fig.add_annotation(
        xref="paper",
        yref="paper",
        name="Data source",
        x=1,
        y=-0.14,
        xanchor="right",
        showarrow=False,
        text="<b>Data source:</b> <a style='color:red' href='https://www.start.umd.edu/gtd/'>Global Terrorism Index (GTD)</a>,  "
        "<b>Author:</b> Chris Baudelaire .K, https://m3-analytics.com",
        opacity=0.8,
        font_size=12,
    )


    fig.update_layout(
        # # template="plotly_dark",,,
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        height=500,
        font={"family": "Lato", "size": 14},
        hovermode="x",
        margin=dict(l=0, r=0, t=80),
        title={
            "text": (
                f"<b>Repartition du nombre d'attaque terroriste en {year}</b><br />"
                f"<sup style='color:silver'>Comparé aux attaques moyens historique ({range_date[0]} - {range_date[1]})"
            ),
            "font": {"family": "serif", "size": 32, "color": "black"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
        xaxis={
            "showgrid":False,
            "dtick": "M1",  # Tick every month
            "hoverformat": "%e %B",  # Day and month name
            # Set range to include 10 days before and after the year to have some space
            "range": [f"{year-1}-12-20", f"{year+1}-01-10"],
            "showgrid": False,
            "tickformat": "%b",  # Month name
            "ticklabelmode": "period",  # Center tick labels
        },
        yaxis={"showgrid": False},
    )
    
    return fig