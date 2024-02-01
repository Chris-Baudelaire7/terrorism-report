from dash import Input, Output, callback, State, html
import dash_echarts
import plotly.express as px
import plotly.graph_objects as go
from data_preparation import *
from utils import *
import json
import plotly.figure_factory as ff
import numpy as np
from plotly.subplots import make_subplots
import datetime as dt
from statsmodels.nonparametric.smoothers_lowess import lowess


@callback(
    Output("terrorist-killed", "figure"),
    Input("range-slider", "value"),
    Input("group", "value"),
    Input("attack", "value"),
    Input("target", "value"),
    Input("weapon", "value"),
)
def timeseries_terrorist_killed(range_date, group, attack, target, weapon):
    df = data_date_filter(range_date)
    data = data_filter(df, group, attack, target, weapon)

    data_nkiller = data.groupby("year", as_index=False)[["nkillter"]].sum()
    data_nkiller["cumsum"] = data_nkiller["nkillter"].cumsum()

    fig = px.bar(data_nkiller, x="year", y="nkillter",
                 color="nkillter", color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)

    fig.add_scatter(
        x=data_nkiller["year"], y=data_nkiller["cumsum"],
        yaxis="y2", name="Somme cumulée",
        line=dict(width=2, color='whitesmoke'),
    )

    fig.update_layout(
        **update_layout_simple,
        bargap=.1,
        showlegend=False,
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(title="Nombre de terroriste tuées", showgrid=False),
        yaxis2=dict(
            title="Somme cumulée", showgrid=False,
            anchor="free",
            overlaying="y",
            side="right",
            position=1
        ),

        font=dict(family="serif", color="black"),
        height=450,
        title={
            "text": (
                f"<b>Evolution du nombre de terroriste<br>tués lors d'une attaque</b><br />"
                f"<sup style='color:silver'>Évolution de 1970 à 2017"
            ),
            "font": {"family": "serif", "size": 30, "color": "black"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    legend(fig)

    return fig
